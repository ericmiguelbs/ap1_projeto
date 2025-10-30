from flask import request, jsonify
from model.db import db
from model.notas import Notas
import requests
from datetime import date
# A importação do Swagger e a inicialização (Swagger(app))
# devem estar no seu arquivo principal (app.py), não aqui.

url = 'http://api_gerenciamento:5000/lista_aluno'

class notasController:

    @staticmethod
    def listar():
        """
        Lista todas as notas cadastradas.
        ---
        tags:
          - Notas
        responses:
          200:
            description: Uma lista de todas as notas.
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: ID da nota.
                  nota:
                    type: number
                    format: float
                    description: O valor da nota.
                  id_aluno:
                    type: integer
                    description: ID do aluno vinculado à nota.
                  id_atividade:
                    type: integer
                    description: ID da atividade vinculada à nota.
        """
        notas = Notas.query.all()
        return jsonify([
            {
                'id': n.id,
                'nota': n.nota,
                'id_aluno': n.id_aluno,
                'id_atividade':n.id_atividade,
            } for n in notas
        ])

    @staticmethod
    def criar():
        """
        Cria uma nova nota para um aluno.
        Valida se o 'id_aluno' existe consultando um serviço externo.
        ---
        tags:
          - Notas
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                nota:
                  type: number
                  format: float
                  description: O valor da nota (ex 8.5).
                id_aluno:
                  type: integer
                  description: O ID do aluno (será validado).
                id_atividade:
                  type: integer
                  description: O ID da atividade.
              required:
                - nota
                - id_aluno
                - id_atividade
        responses:
          201:
            description: Nota criada com sucesso.
          400:
            description: Dados inválidos ou faltando no JSON enviado.
          404:
            description: O 'id_aluno' enviado não foi encontrado no serviço externo.
          500:
            description: Falha ao consultar o serviço externo de alunos.
        """
        data = request.get_json()
        try:
            id_aluno_enviado = data.get('id_aluno')
            nota_enviada = data.get('nota')
            id_atividade_enviada = data.get('id_atividade')

            if not id_aluno_enviado or nota_enviada is None or not id_atividade_enviada:
                return jsonify({'erro': 'Dados inválidos ou faltando (nota, id_aluno, id_atividade).'}), 400

            response = requests.get(url)
            response.raise_for_status()
            alunos = response.json()
            recebido = False
            for i in alunos:
                if str(i.get('id')) == str(id_aluno_enviado):
                    recebido = True
                    break
            if not recebido:
                return jsonify({'erro': f'O aluno com ID {id_aluno_enviado} não existe.'}), 404
            
            nota = Notas(
                nota = nota_enviada,
                id_aluno = id_aluno_enviado,
                id_atividade = id_atividade_enviada
            )
            db.session.add(nota)
            db.session.commit()
            return jsonify({'mensagem': 'nota adicionada com sucesso!'}), 201
        
        except (KeyError, TypeError):
            return jsonify({'erro': 'Dados inválidos ou faltando.'}), 400
        except requests.exceptions.RequestException as e:
            return jsonify({'erro': f'Falha ao consultar alunos: {str(e)}'}), 500
        
    @staticmethod
    def atualizar(id):
        """
        Atualiza uma nota existente pelo seu ID.
        Campos enviados no JSON irão sobrescrever os valores existentes.
        Se 'id_aluno' for enviado, ele será validado no serviço externo.
        ---
        tags:
          - Notas
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: O ID da nota a ser atualizada.
          - name: body
            in: body
            required: true
            schema:
              type: object
              description: Campos para atualizar (pelo menos um é esperado).
              properties:
                nota:
                  type: number
                  format: float
                id_aluno:
                  type: integer
                id_atividade:
                  type: integer
        responses:
          200:
            description: Nota atualizada com sucesso.
          400:
            description: Dados inválidos no JSON enviado.
          404:
            description: A nota (pelo ID) não foi encontrada, ou o novo 'id_aluno' não foi encontrado no serviço externo.
          500:
            description: Falha ao consultar o serviço externo de alunos.
        """
        nota = Notas.query.get_or_404(id) # O 404 aqui é automático se a nota não existir
        data = request.get_json()
        try:
            if 'id_aluno' in data:
                id_aluno_novo = data.get('id_aluno')
                
                response = requests.get(url)
                response.raise_for_status()
                alunos = response.json()
                recebido = False
                for i in alunos:
                    if str(i.get('id')) == str(id_aluno_novo):
                        recebido = True
                        break
                if not recebido:
                    return jsonify({'erro': f'O aluno com ID {id_aluno_novo} não existe.'}), 404
            
            nota.nota = data.get('nota', nota.nota)
            nota.id_aluno = data.get('id_aluno', nota.id_aluno)
            nota.id_atividade = data.get('id_atividade', nota.id_atividade)

            db.session.commit()
            return jsonify({'mensagem':'Nota atualizada com sucesso!'})
        
        except (KeyError, TypeError):
            return jsonify({'erro': 'Dados inválidos ou faltando.'}), 400
        except requests.exceptions.RequestException as e:
            return jsonify({'erro': f'Falha ao consultar alunos: {str(e)}'}), 500
                
    @staticmethod
    def deletar(id):
        """
        Deleta uma nota pelo seu ID.
        ---
        tags:
          - Notas
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: O ID da nota a ser deletada.
        responses:
          200:
            description: Nota deletada com sucesso.
          404:
            description: A nota com o 'id' fornecido não foi encontrada.
        """
        nota = Notas.query.get_or_404(id) # 404 automático se não encontrar
        db.session.delete(nota)
        db.session.commit()
        return jsonify({'mensagem':'Nota deletada com sucesso!'})
