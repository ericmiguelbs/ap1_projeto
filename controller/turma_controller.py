from flask import request, jsonify
from models import db
from models.turma import Turma

class TurmaController:
    @staticmethod
    def listar():
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
        data = request.get_json()
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
        turma = Turma.query.get_or_404(id)
        data = request.get_json()

        turma.descricao = data.get('descricao', turma.descricao)
        turma.professor_id = data.get('professor_id', turma.professor_id)
        turma.ativo = data.get('ativo', turma.ativo)

        db.session.commit()
        return jsonify({'mensagem': 'Turma atualizada com sucesso!'})

    @staticmethod
    def deletar(id):
        turma = Turma.query.get_or_404(id)
        db.session.delete(turma)
        db.session.commit()
        return jsonify({'mensagem': 'Turma deletada com sucesso!'})
