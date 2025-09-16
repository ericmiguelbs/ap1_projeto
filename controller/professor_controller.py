from flask import request, jsonify
from models.db import db
from models.professor import Professor

class ProfessorController:
    
    @staticmethod
    def listar():
        """
        Lista todos os professores cadastrados.
        ---
        tags:
          - Professor
        responses:
          200:
            description: Uma lista de professores.
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  nome:
                    type: string
                  idade:
                    type: integer
                  materia:
                    type: string
                  observacoes:
                    type: string
        """
        professores = Professor.query.all()
        return jsonify([{
            'id': p.id,
            'nome': p.nome,
            'idade': p.idade,
            'materia': p.materia,
            'observacoes': p.observacoes
        } for p in professores])
        
    @staticmethod
    def criar():
        """
        Cria um novo professor.
        ---
        tags:
          - Professor
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                  description: Nome do professor.
                idade:
                  type: integer
                  description: Idade do professor.
                materia:
                  type: string
                  description: Matéria que o professor leciona.
                observacoes:
                  type: string
                  description: Observações adicionais sobre o professor.
              example:
                nome: "Ana Martins"
                idade: 45
                materia: "Matemática"
                observacoes: "Professora experiente"
        responses:
          201:
            description: Professor criado com sucesso.
            schema:
              type: object
              properties:
                mensagem:
                  type: string
        """
        data = request.get_json()
        novo = Professor(
            nome=data['nome'],
            idade=data['idade'],
            materia=data['materia'],
            observacoes=data.get('observacoes')
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({'mensagem': 'Professor criado com sucesso!'}), 201
    
    @staticmethod
    def atualizar(id):
        """
        Atualiza um professor existente pelo ID.
        ---
        tags:
          - Professor
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: ID do professor a ser atualizado.
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                idade:
                  type: integer
                materia:
                  type: string
                observacoes:
                  type: string
        responses:
          200:
            description: Professor atualizado com sucesso.
          404:
            description: Professor não encontrado.
        """
        professor = Professor.query.get_or_404(id)
        data = request.get_json()

        professor.nome = data.get('nome', professor.nome)
        professor.idade = data.get('idade', professor.idade)
        professor.materia = data.get('materia', professor.materia)
        professor.observacoes = data.get('observacoes', professor.observacoes)

        db.session.commit()
        return jsonify({'mensagem': 'Professor atualizado com sucesso!'})

    @staticmethod
    def deletar(id):
        """
        Deleta um professor pelo ID.
        ---
        tags:
          - Professor
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: ID do professor a ser deletado.
        responses:
          200:
            description: Professor deletado com sucesso.
            schema:
              type: object
              properties:
                mensagem:
                  type: string
          404:
            description: Professor não encontrado.
        """
        professor = Professor.query.get_or_404(id)
        db.session.delete(professor)
        db.session.commit()
        return jsonify({'mensagem': 'Professor deletado com sucesso!'})