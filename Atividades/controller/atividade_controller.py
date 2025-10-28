from flask import request, jsonify
from model.db import db
from model.atividade import Atividade
import requests
from datetime import date
# Lembre-se que o Swagger(app) é inicializado no seu app.py

url_professor = 'http://api_gerenciamento:5000/lista_professor'
url_turma = 'http://api_gerenciamento:5000/lista_turmas'

class atividadeController:

    @staticmethod
    def listar():
        """
        Lista todas as atividades cadastradas.
        ---
        tags:
          - Atividades
        responses:
          200:
            description: Uma lista de todas as atividades.
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: ID da atividade.
                  nome_atividade:
                    type: string
                    description: Nome da atividade.
                  descricao:
                    type: string
                    description: Descrição detalhada da atividade.
                  peso_porcento:
                    type: number
                    format: float
                    description: O peso (percentual) da atividade na nota.
                  data_entrega:
                    type: string
                    format: date
                    description: Data limite para entrega (AAAA-MM-DD).
                  turma_id:
                    type: integer
                    description: ID da turma associada.
                  professor_id:
                    type: integer
                    description: ID do professor associado.
        """
        atividades = Atividade.query.all()
        return jsonify([
            {
                'id': a.id,
                'nome_atividade': a.nome_atividade,
                'descricao': a.descricao,
                'peso_porcento': a.peso_porcento,
                # Converte a data para string no formato ISO para ser "jsonificável"
                'data_entrega': a.data_entrega.isoformat() if a.data_entrega else None, 
                'turma_id': a.id_turma,
                'professor_id': a.id_professor
            } for a in atividades
        ])

    @staticmethod
    def criar():
        """
        Cria uma nova atividade.
        Valida se 'id_professor' e 'id_turma' existem consultando serviços externos.
        ---
        tags:
          - Atividades
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                nome_atividade:
                  type: string
                descricao:
                  type: string
                peso_porcento:
                  type: number
                  format: float
                data_entrega:
                  type: string
                  format: date
                  description: Data no formato AAAA-MM-DD.
                id_turma:
                  type: integer
                id_professor:
                  type: integer
              required:
                - nome_atividade
                - descricao
                - peso_porcento
                - data_entrega
                - id_turma
                - id_professor
        responses:
          201:
            description: Atividade criada com sucesso.
          400:
            description: Dados inválidos ou faltando no JSON enviado.
          404:
            description: O 'id_professor' ou 'id_turma' não foi encontrado nos serviços externos.
          500:
            description: Falha ao consultar os serviços externos de professores ou turmas.
        """
        data = request.get_json()
        try:
            # Validação de Professor
            response_prof = requests.get(url_professor)
            response_prof.raise_for_status()
            professores = response_prof.json()
            professor_encontrado = False
            for p in professores:
                if str(p.get('id')) == str(data.get('id_professor')):
                    professor_encontrado = True
                    break
            if not professor_encontrado:
                return jsonify({'erro': f'O professor com ID {data.get("id_professor")} não existe.'}), 404

            # Validação de Turma
            response_turma = requests.get(url_turma)
            response_turma.raise_for_status()
            turmas = response_turma.json()
            turma_encontrada = False
            for t in turmas:
                if str(t.get('id')) == str(data.get('id_turma')):
                    turma_encontrada = True
                    break
            if not turma_encontrada:
                return jsonify({'erro': f'A turma com ID {data.get("id_turma")} não existe.'}), 404

            # Criação da Atividade
            atividade = Atividade(
                nome_atividade = data['nome_atividade'],
                descricao = data['descricao'],
                peso_porcento = data['peso_porcento'],
                data_entrega = date.fromisoformat(data['data_entrega']), # Converte string AAAA-MM-DD para objeto date
                id_turma = data['id_turma'],
                id_professor = data['id_professor']
            )

            db.session.add(atividade)
            db.session.commit()

            return jsonify({'mensagem': 'Atividade adicionada com sucesso!'}), 201

        except (KeyError, TypeError, ValueError): # ValueError pega o erro do date.fromisoformat
            return jsonify({'erro': 'Dados inválidos ou faltando (verifique o formato da data AAAA-MM-DD).'}), 400
        except requests.exceptions.RequestException as e:
            return jsonify({'erro': f'Falha ao consultar professores ou turmas: {str(e)}'}), 500

    @staticmethod
    def atualizar(id):
        """
        Atualiza uma atividade existente pelo seu ID.
        Campos enviados no JSON irão sobrescrever os valores existentes.
        Se 'id_professor' ou 'id_turma' forem enviados, eles serão validados nos serviços externos.
        ---
        tags:
          - Atividades
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: O ID da atividade a ser atualizada.
          - name: body
            in: body
            required: true
            schema:
              type: object
              description: Campos para atualizar (pelo menos um é esperado).
              properties:
                nome_atividade:
                  type: string
                descricao:
                  type: string
                peso_porcento:
                  type: number
                  format: float
                data_entrega:
                  type: string
                  format: date
                  description: Data no formato AAAA-MM-DD.
                id_turma:
                  type: integer
                id_professor:
                  type: integer
        responses:
          200:
            description: Atividade atualizada com sucesso.
          400:
            description: Dados inválidos ou faltando (verifique o formato da data AAAA-MM-DD).
          404:
            description: A atividade (ID) não foi encontrada, ou o novo 'id_professor'/'id_turma' não existe.
          500:
            description: Falha ao consultar os serviços externos.
        """
        atividade = Atividade.query.get_or_404(id) 
        data = request.get_json()
        try:
            # Valida professor SE ele for enviado na requisição
            if 'id_professor' in data:
                response_prof = requests.get(url_professor)
                response_prof.raise_for_status()
                professores = response_prof.json()
                professor_encontrado = False
                for p in professores:
                    if str(p.get('id')) == str(data.get('id_professor')):
                        professor_encontrado = True
                        break
                if not professor_encontrado:
                    return jsonify({'erro': f'O professor com ID {data.get("id_professor")} não existe.'}), 404
            
            # Valida turma SE ela for enviada na requisição
            if 'id_turma' in data:
                response_turma = requests.get(url_turma)
                response_turma.raise_for_status()
                turmas = response_turma.json()
                turma_encontrada = False
                for t in turmas: 
                    if str(t.get('id')) == str(data.get('id_turma')):
                        turma_encontrada = True
                        break
                if not turma_encontrada:
                    return jsonify({'erro': f'A turma com ID {data.get("id_turma")} não existe.'}), 404
            
            # Atualiza os campos
            atividade.nome_atividade = data.get('nome_atividade', atividade.nome_atividade)
            atividade.descricao = data.get('descricao', atividade.descricao)
            atividade.peso_porcento = data.get('peso_porcento', atividade.peso_porcento)
            atividade.id_turma = data.get('id_turma', atividade.id_turma) 
            atividade.id_professor = data.get('id_professor', atividade.id_professor)
            
            # Atualiza a data SE ela for enviada
            if 'data_entrega' in data:
                atividade.data_entrega = date.fromisoformat(data['data_entrega'])

            db.session.commit()
            return jsonify({'mensagem': 'Atividade atualizada com sucesso!'})
        
        except (KeyError, TypeError, ValueError):
            return jsonify({'erro': 'Dados inválidos ou faltando (verifique o formato da data AAAA-MM-DD).'}), 400
        except requests.exceptions.RequestException as e:
            return jsonify({'erro': f'Falha ao consultar professores ou turmas: {str(e)}'}), 500

    @staticmethod
    def deletar(id):
        """
        Deleta uma atividade pelo seu ID.
        ---
        tags:
          - Atividades
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: O ID da atividade a ser deletada.
        responses:
          200:
            description: Atividade deletada com sucesso.
          404:
            description: A atividade com o 'id' fornecido não foi encontrada.
        """
        atividade = Atividade.query.get_or_404(id)
        db.session.delete(atividade)
        db.session.commit()
        # Corrigindo o pequeno erro de digitação de "deletado" para "deletada"
        return jsonify({'mensagem':'Atividade deletada com sucesso!'})