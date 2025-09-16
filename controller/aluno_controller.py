from flask import request, jsonify
from models.db import db
from models.aluno import Aluno


class AlunoController:

    @staticmethod
    def listar():
        """
        Lista todos os alunos cadastrados.
        ---
        tags:
          - Aluno
        responses:
          200:
            description: Uma lista de alunos.
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
                  turma_id:
                    type: integer
                  data_nascimento:
                    type: string
                    format: date
                  nota_primeiro_semestre:
                    type: number
                  nota_segundo_semestre:
                    type: number
                  media_final:
                    type: number
        """
        aluno = Aluno.query.all()
        return jsonify([{
            'id': p.id,
            'nome': p.nome,
            'idade': p.idade,
            'turma_id': p.turma_id,
            'data_nascimento': p.data_nascimento,
            'nota_primeiro_semestre': p.nota_primeiro_semestre,
            'nota_segundo_semestre': p.nota_segundo_semestre,
            'media_final': p.media_final
        } for p in aluno])

    @staticmethod
    def criar():
        """
        Cria um novo aluno.
        ---
        tags:
          - Aluno
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                  description: Nome do aluno.
                idade:
                  type: integer
                  description: Idade do aluno.
                turma_id:
                  type: integer
                  description: ID da turma do aluno.
                data_nascimento:
                  type: string
                  format: date
                  description: Data de nascimento do aluno (YYYY-MM-DD).
                nota_primeiro_semestre:
                  type: number
                  description: Nota do primeiro semestre.
                nota_segundo_semestre:
                  type: number
                  description: Nota do segundo semestre.
                media_final:
                  type: number
                  description: Média final do aluno.
              example:
                nome: "João Silva"
                idade: 18
                turma_id: 1
                data_nascimento: "2007-05-15"
                nota_primeiro_semestre: 8.5
                nota_segundo_semestre: 9.0
                media_final: 8.75
        responses:
          200:
            description: Aluno adicionado com sucesso.
            schema:
              type: object
              properties:
                mensagem:
                  type: string
        """
        data = request.get_json()
        novo = Aluno(
            nome=data['nome'],
            idade=data['idade'],
            turma_id=data['turma_id'],
            data_nascimento=data['data_nascimento'],
            nota_primeiro_semestre=data['nota_primeiro_semestre'],
            nota_segundo_semestre=data['nota_segundo_semestre'],
            media_final=data['media_final']
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({'mensagem': 'Aluno adicionado com sucesso !'})

    @staticmethod
    def atualizar(id):
        """
        Atualiza um aluno existente pelo ID.
        ---
        tags:
          - Aluno
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: ID do aluno a ser atualizado.
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
                turma_id:
                  type: integer
                data_nascimento:
                  type: string
                  format: date
                nota_primeiro_semestre:
                  type: number
                nota_segundo_semestre:
                  type: number
                media_final:
                  type: number
        responses:
          200:
            description: Aluno atualizado com sucesso.
          404:
            description: Aluno não encontrado.
        """
        aluno = Aluno.query.get_or_404(id=id)
        data = request.get_json()

        aluno.nome = data.get('nome', aluno.nome)
        aluno.idade = data.get('idade', aluno.idade)
        aluno.turma_id = data.get('turma_id', aluno.turma_id)
        aluno.data_nascimento = data.get('data_nascimento', aluno.data_nascimento)
        aluno.nota_primeiro_semestre = data.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)
        aluno.nota_segundo_semestre = data.get('nota_segundo_semestre', aluno.nota_segundo_semestre)
        aluno.media_final = data.get('media_final', aluno.media_final)

        db.session.commit()
        return jsonify({"mensagem": "Aluno adicionado com sucesso !"})

    @staticmethod
    def deletar(id):
        """
        Deleta um aluno pelo ID.
        ---
        tags:
          - Aluno
        parameters:
          - name: id
            in: path
            type: integer
            required: true
            description: ID do aluno a ser deletado.
        responses:
          200:
            description: Aluno removido com sucesso.
            schema:
              type: object
              properties:
                mensagem:
                  type: string
          404:
            description: Aluno não encontrado.
        """
        aluno = Aluno.query.get_or_404(id=id)
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({"mensagem": 'Aluno removido com sucesso !'})