from flask import request, jsonify
from model.db import db
from model.reservas import Reserva
import requests
from datetime import date
# A inicialização do Swagger(app) deve estar no seu app.py

url = 'http://192.168.15.5:5000/lista_turmas'
url_reserva = 'http://192.168.15.5:5001/lista_reserva'

class reservaController:

    @staticmethod
    def listar():
        """
        Lista todas as reservas de salas/laboratórios.
        ---
        tags:
          - Reservas
        responses:
          200:
            description: Uma lista de todas as reservas.
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  num_sala:
                    type: integer
                  lab:
                    type: boolean
                  data:
                    type: string
                    format: date
                  id_turma:
                    type: integer
        """
        reservas = Reserva.query.all()
        return jsonify([
            {
                'id': t.id,
                'num_sala': t.num_sala,
                'lab': t.lab,
                'data':t.data.isoformat(), # Correto, já estava assim
                'id_turma': t.id_turma
            } for t in reservas
        ])

    @staticmethod
    def criar():
        """
        Cria uma nova reserva para uma turma.
        Valida se o 'id_turma' existe consultando um serviço externo.
        ---
        tags:
          - Reservas
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                num_sala:
                  type: integer
                  description: Número da sala ou laboratório.
                lab:
                  type: boolean
                  description: 'true' se for um laboratório, 'false' se for sala comum.
                data:
                  type: string
                  format: date
                  description: Data da reserva (AAAA-MM-DD).
                id_turma:
                  type: integer
                  description: ID da turma (será validado externamente).
              required:
                - num_sala
                - lab
                - data
                - id_turma
        responses:
          201:
            description: Reserva criada com sucesso.
          400:
            description: Dados inválidos ou faltando no JSON (verifique formato da data AAAA-MM-DD).
          404:
            description: A 'id_turma' enviada não foi encontrada no serviço externo.
          500:
            description: Falha ao consultar o serviço externo de turmas.
        """
        data = request.get_json()
        try:
            # Valida Turma
            response = requests.get(url)
            response.raise_for_status()
            turmas = response.json()
            recebido = False
            id_turma_enviada = data.get('id_turma') # Usando .get para segurança
            for i in turmas:
               # Comparando como string para segurança, assim como nos outros controllers
               if str(i.get('id')) == str(id_turma_enviada): 
                    recebido = True
                    break
            if not recebido:
                 # Corrigindo o bug (estava {id} e não data['id_turma'])
                return jsonify({'erro': f'A turma com ID {id_turma_enviada} não existe.'}), 404
            
            reserva = Reserva(
                num_sala = data['num_sala'],
                lab = data['lab'],
                data= date.fromisoformat(data['data']),
                id_turma = data['id_turma']
            )
            db.session.add(reserva)
            db.session.commit()
            return jsonify({'mensagem': 'reserva adicionada com sucesso!'}), 201
        
        except (KeyError, TypeError, ValueError): # ValueError para o fromisoformat
            return jsonify({'erro': 'Dados inválidos ou faltando (verifique o formato da data AAAA-MM-DD).'}), 400
        # Adicionando a captura de erro de request, que estava faltando
        except requests.exceptions.RequestException as e:
            return jsonify({'erro': f'Falha ao consultar turmas: {str(e)}'}), 500
        

    @staticmethod
    def atualizar(id):
        """
        Atualiza uma reserva existente pelo seu ID.
        Valida 'id_turma' e 'id' da reserva em serviços externos antes de atualizar.
        ---
        tags:
          - Reservas
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: O ID da reserva a ser atualizada.
          - name: body
            in: body
            required: true
            schema:
              type: object
              description: Campos para atualizar.
              properties:
                num_sala:
                  type: integer
                lab:
                  type: boolean
                data:
                  type: string
                  format: date
                  description: Data no formato AAAA-MM-DD (Obrigatório para atualizar).
                id_turma:
                  type: integer
              required:
                - data # O seu código (sem .get) torna este campo obrigatório
        responses:
          200:
            description: Reserva atualizada com sucesso.
          400:
            description: Dados inválidos (ex: 'data' faltando ou formato incorreto).
          404:
            description: A reserva (ID) não foi encontrada, ou a 'id_turma' não foi encontrada, ou a reserva não existe no serviço externo.
          500:
            description: Falha ao consultar os serviços externos.
        """
        reserva = Reserva.query.get_or_404(id)
        data = request.get_json()
        try:
            # Validação 1: Turma (Serviço Externo)
            response = requests.get(url)
            response.raise_for_status()
            turmas = response.json()
            recebido = False
            id_turma_enviada = data.get('id_turma', reserva.id_turma) # Pega a nova ou mantém a antiga
            for i in turmas:
                if str(i.get('id')) == str(id_turma_enviada):
                    recebido = True
                    break
            if not recebido:
                # Corrigindo o bug (estava {id} e não o id da turma)
                return jsonify({'erro': f'Não foi possível atualizar a reserva, a turma com ID {id_turma_enviada} não existe.'}), 404
            
            # Validação 2: Reserva (Serviço Externo) - Lógica estranha, mas documentando como está
            response_reserva = requests.get(url_reserva)
            response_reserva.raise_for_status()
            reservas = response_reserva.json()
            recebido_reserva = False
            for r in reservas:
                if r.get('id') == id: # Aqui o 'id' do path está correto
                    recebido_reserva = True
                    break
            if not recebido_reserva:
                return jsonify({'erro': f'Não foi possível atualizar a reserva, o ID {id} não existe no serviço externo.'}), 404
                
            # Atualiza os campos
            reserva.num_sala = data.get('num_sala', reserva.num_sala)
            reserva.lab = data.get('lab', reserva.lab)
            # Atenção: 'data' é obrigatório no seu código, pois não usa .get()
            reserva.data = date.fromisoformat(data['data']) 
            reserva.id_turma = data.get('id_turma', reserva.id_turma)
            
            db.session.commit()
            return jsonify({'mensagem': 'Reserva atualizada com sucesso!'})
        
        except (KeyError, TypeError, ValueError): # KeyError se 'data' faltar, ValueError do fromisoformat
            return jsonify({'erro': 'Dados inválidos ou faltando (verifique se o campo "data" está presente no formato AAAA-MM-DD).'}), 400
        # Adicionando a captura de erro de request
        except requests.exceptions.RequestException as e:
            return jsonify({'erro': f'Falha ao consultar serviços externos: {str(e)}'}), 500
            
    # Assumindo que era para ser @staticmethod, como os outros
    @staticmethod 
    def deletar(id):
        """
        Deleta uma reserva pelo seu ID.
        ---
        tags:
          - Reservas
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: O ID da reserva a ser deletada.
        responses:
          200:
            description: Reserva deletada com sucesso.
          404:
            description: A reserva com o 'id' fornecido não foi encontrada.
        """
        reserva = Reserva.query.get_or_404(id)
        db.session.delete(reserva)
        db.session.commit()
        return jsonify({'mensagem': 'Reserva deletada com sucesso!'})