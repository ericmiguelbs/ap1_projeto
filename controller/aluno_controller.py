from flask import request, jsonify
from models.db import db
from models.aluno import Aluno
from datetime import datetime

class AlunoController:

    @staticmethod
    def listar():
        """ ... (sua documentação aqui) ... """
        alunos = Aluno.query.all()
        return jsonify([{
            'id': aluno.id,
            'nome': aluno.nome,
            'idade': aluno.idade,
            'turma_id': aluno.turma_id,
            
            # CORREÇÃO: Converte o objeto de data para string no formato ISO (YYYY-MM-DD)
            # O 'if' garante que não dará erro se a data for nula no banco.
            'data_nascimento': aluno.data_nascimento.isoformat() if aluno.data_nascimento else None,
            
            'nota_primeiro_semestre': aluno.nota_primeiro_semestre,
            'nota_segundo_semestre': aluno.nota_segundo_semestre,
            'media_final': aluno.media_final
        } for aluno in alunos])

    @staticmethod
    def criar():
        """ ... (sua documentação aqui) ... """
        data = request.get_json()
        
        # CORREÇÃO: Faltava esta linha para criar a variável convertendo a string em objeto de data.
        data_nascimento_obj = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()

        novo = Aluno(
            nome=data['nome'],
            idade=data['idade'],
            turma_id=data['turma_id'],
            data_nascimento=data_nascimento_obj, # Agora a variável existe e tem o tipo certo.
            nota_primeiro_semestre=data['nota_primeiro_semestre'],
            nota_segundo_semestre=data['nota_segundo_semestre'],
            media_final=data['media_final']
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({'mensagem': 'Aluno adicionado com sucesso !'})

    @staticmethod
    def atualizar(id):
        """ ... (sua documentação aqui) ... """
        aluno = Aluno.query.get_or_404(id) # O 'id=' não é necessário aqui
        data = request.get_json()

        aluno.nome = data.get('nome', aluno.nome)
        aluno.idade = data.get('idade', aluno.idade)
        aluno.turma_id = data.get('turma_id', aluno.turma_id)
        
        # CORREÇÃO: Verifica se a data foi enviada e a converte antes de atribuir.
        if 'data_nascimento' in data and data['data_nascimento']:
            aluno.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()

        aluno.nota_primeiro_semestre = data.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)
        aluno.nota_segundo_semestre = data.get('nota_segundo_semestre', aluno.nota_segundo_semestre)
        aluno.media_final = data.get('media_final', aluno.media_final)

        db.session.commit()
        # CORREÇÃO: Mensagem de sucesso deve ser de atualização.
        return jsonify({"mensagem": "Aluno atualizado com sucesso !"})

    @staticmethod
    def deletar(id):
        """ ... (sua documentação aqui) ... """
        aluno = Aluno.query.get_or_404(id) # O 'id=' não é necessário aqui
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({"mensagem": 'Aluno removido com sucesso !'})