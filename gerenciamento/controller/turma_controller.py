from flask import request, jsonify
from models.db import db
from models.turma import Turma
from models.professor import Professor

class TurmaController:
    
    @staticmethod
    def listar():
        """
        Lista todas as turmas cadastradas.
        ---
        tags:
          - Turma
        responses:
          200:
            description: Uma lista de turmas.
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  descricao:
                    type: string
                  professor_id:
                    type: integer
                  ativo:
                    type: boolean
        """
        turmas = Turma.query.all()
        return jsonify([
            {
                'id': t.id,
                'descricao': t.descricao,
                'professor_id': t.professor_id,
                'ativo': t.ativo
            } for t in turmas
        ])

    @staticmethod
    def criar():
        """
        Cria uma nova turma.
        ---
        tags:
          - Turma
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                descricao:
                  type: string
                  description: Descrição da turma.
                professor_id:
                  type: integer
                  description: ID do professor responsável pela turma.
                ativo:
                  type: boolean
                  description: Se a turma está ativa ou não.
              example:
                descricao: "Turma de T.I."
                professor_id: 1
                ativo: true
        responses:
          200:
            description: Turma criada com sucesso.
            schema:
              type: object
              properties:
                mensagem:
                  type: string
        """

        data = request.get_json()
        professor_existente = Professor.query.get(data['professor_id'])
        if not professor_existente:
            return jsonify({'erro': f"o professor com o id {data['professor_id']} não existe"})
        nova_turma = Turma(
            descricao=data['descricao'],
            professor_id=data['professor_id'],
            ativo=data['ativo']
        )
        db.session.add(nova_turma)
        db.session.commit()
        return jsonify({'mensagem': 'Turma criada com sucesso!'})

    @staticmethod
    def atualizar(id):
        """
        Atualiza uma turma existente pelo ID.
        ---
        tags:
          - Turma
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: ID da turma a ser atualizada.
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                descricao:
                  type: string
                professor_id:
                  type: integer
                ativo:
                  type: boolean
        responses:
          200:
            description: Turma atualizada com sucesso.
          404:
            description: Turma não encontrada.
        """
        turma = Turma.query.get_or_404(id)
        data = request.get_json()
        professor_existente = Professor.query.get(data['professor_id'])
        if not professor_existente:
            return jsonify({'erro': f"O professor com o id {data['professor_id']} não foi encontrado"})
        turma.descricao = data.get('descricao', turma.descricao)
        turma.professor_id = data.get('professor_id', turma.professor_id)
        turma.ativo = data.get('ativo', turma.ativo)

        db.session.commit()
        return jsonify({'mensagem': 'Turma atualizada com sucesso!'})

    @staticmethod
    def deletar(id):
        """
        Deleta uma turma pelo ID.
        ---
        tags:
          - Turma
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: ID da turma a ser deletada.
        responses:
          200:
            description: Turma deletada com sucesso.
            schema:
              type: object
              properties:
                mensagem:
                  type: string
          404:
            description: Turma não encontrada.
        """
        turma = Turma.query.get_or_404(id)
        db.session.delete(turma)
        db.session.commit()
        return jsonify({'mensagem': 'Turma deletada com sucesso!'})