from model.db import db

class Atividade(db.Model):
    __tablename__ = 'atividades'

    id = db.Column(db.Integer, primary_key=True)
    nome_atividade = db.Column(db.String, nullable=False)
    descricao= db.Column(db.String, nullable=False)
    peso_porcento = db.Column(db.Integer, nullable=False)
    data_entrega = db.Column(db.Date, nullable=False)
    id_turma= db.Column(db.Integer, nullable = False)
    id_professor = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"<Atividade {self.descricao}>"
