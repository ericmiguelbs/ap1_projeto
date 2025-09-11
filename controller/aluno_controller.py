from flask import request, jsonify
from models import db
from models.aluno import Aluno


class AlunoController:
    @staticmethod
    def listar():
        aluno = Aluno.query.all()
        return jsonify([{
                'id':p.id,
                'nome':p.nome,
                'idade':p.idade,
                'turma_id':p.turma_id,
                'data_nascimento': p.data_nascimento,
                'nota_primeiro_semestre': p.nota_primeiro_semestre,
                'nota_segundo_semestre': p.nota_segundo_semestre,
                'media_final': p.media_final
            }for p in aluno])
    
    @staticmethod
    def criar():
        data = request.get_json()
        novo = Aluno(
            nome = data['nome'],
            idade = data['idade'],
            turma_id = data['turma_id'],
            data_nascimento = data['data_nascimento'],
            nota_primeiro_semestre = data['nota_primeiro_semestre'],
            nota_segundo_semestre = data['nota_segundo_semestre'],
            media_final = data['media_final'] 
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({'mensagem': 'Aluno adicionado com sucesso !'})

    @staticmethod
    def atualizar(id):
        aluno = Aluno.query.get_or_404(id = id)
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
        aluno = Aluno.query.get_or_404(id = id)
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({"mensagem": 'Aluno removido com sucesso !'})
    
