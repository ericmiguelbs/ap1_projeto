from flask import request, jsonify
from models import db
from models.professor import Professor

class ProfessorController:
    @staticmethod
    def listar():
        professores = Professor.query.all()
        return jsonify([{
                'id':p.id,
                'nome':p.nome,
                'idade': p.idade,
                'materia': p.materia,
                'observacoes': p.observacoes
            } for p in professores])
        
    @staticmethod
    def criar():
        data = request.get_json()
        novo = Professor(
            nome=data['nome'],
            idade = data['idade'],
            materia=data['materia'],
            observacoes =data.get('observacoes')
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({'mensagem':'Professor criado com sucesso!'}), 201
    
    @staticmethod
    def atualizar(id):
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
        professor = Professor.query.get_or_404(id)
        db.session.delete(professor)
        db.session.commit()
        return jsonify({'mensagem': 'Professor deletado com sucesso!'})