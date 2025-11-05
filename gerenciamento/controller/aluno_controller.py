from flask import request, jsonify
from models.db import db
from models.aluno import Aluno
from models.turma import Turma
from datetime import datetime

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
        alunos = Aluno.query.all()
        return jsonify([{
            'id': aluno.id,
            'nome': aluno.nome,
            'idade': aluno.idade,
            'turma_id': aluno.turma_id,
            'data_nascimento': aluno.data_nascimento.isoformat() if aluno.data_nascimento else None,
            'nota_primeiro_semestre': aluno.nota_primeiro_semestre,
            'nota_segundo_semestre': aluno.nota_segundo_semestre,
            'media_final': aluno.media_final
        } for aluno in alunos])

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
              required:
                - nome
                - idade
                - turma_id
                - data_nascimento
              properties:
                nome:
                  type: string
                  description: Nome do aluno.
                  example: "João Silva"
                idade:
                  type: integer
                  description: Idade do aluno.
                  example: 18
                turma_id:
                  type: integer
                  description: ID da turma do aluno.
                  example: 1
                data_nascimento:
                  type: string
                  format: date
                  description: Data de nascimento do aluno (YYYY-MM-DD).
                  example: "2007-05-15"
                nota_primeiro_semestre:
                  type: number
                  description: Nota do primeiro semestre.
                  example: 8.5
                nota_segundo_semestre:
                  type: number
                  description: Nota do segundo semestre.
                  example: 9.0
                media_final:
                  type: number
                  description: Média final do aluno.
                  example: 8.75
        responses:
          201:
            description: Aluno adicionado com sucesso.
          400:
            description: Dados inválidos.
        """
        data = request.get_json()
        try:
            turma_existente = Turma.query.get(data.get('turma_id'))
            if not turma_existente:
                return jsonify({'erro': f"A turma com id {data.get('turma_id')} não foi encontrado"}), 400
            data_nascimento_obj = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
            
            novo = Aluno(
                nome=data['nome'],
                idade=data['idade'],
                turma_id=data['turma_id'],
                data_nascimento=data_nascimento_obj,
                nota_primeiro_semestre=data['nota_primeiro_semestre'],
                nota_segundo_semestre=data['nota_segundo_semestre'],
                media_final=data['media_final']
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify({'mensagem': 'Aluno adicionado com sucesso!'}), 201
        except (KeyError, TypeError):
            return jsonify({'erro': 'Dados inválidos ou faltando.'}), 400

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
                nome: {type: string}
                idade: {type: integer}
                turma_id: {type: integer}
                data_nascimento: {type: string, format: date}
                nota_primeiro_semestre: {type: number}
                nota_segundo_semestre: {type: number}
                media_final: {type: number}
        responses:
          200:
            description: Aluno atualizado com sucesso.
          404:
            description: Aluno não encontrado.
        """
        aluno = Aluno.query.get(id)
        if not aluno:
            return jsonify({'erro': f"O aluno com id {id} não foi encontrado"}), 404
        data = request.get_json()
        turma_existente = Turma.query.get(data.get('turma_id'))
        if not turma_existente:
            return jsonify({'erro': f"A turma com id {data['turma_id']} não foi encontrado"}), 400 
        aluno.nome = data.get('nome', aluno.nome)
        aluno.idade = data.get('idade', aluno.idade)
        aluno.turma_id = data.get('turma_id', aluno.turma_id)
        
        if 'data_nascimento' in data and data['data_nascimento']:
            aluno.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()

        aluno.nota_primeiro_semestre = data.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)
        aluno.nota_segundo_semestre = data.get('nota_segundo_semestre', aluno.nota_segundo_semestre)
        aluno.media_final = data.get('media_final', aluno.media_final)

        db.session.commit()
        return jsonify({"mensagem": "Aluno atualizado com sucesso!"})

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
          404:
            description: Aluno não encontrado.
        """
        aluno = Aluno.query.get_or_404(id)
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({'mensagem': 'Aluno removido com sucesso!'})
