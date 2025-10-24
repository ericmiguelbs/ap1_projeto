from model.db import db

class Notas(db.Model):
    __tablename__ = 'notas'
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    id_aluno = db.Column(db.Integer, nullable=False)
    #Relacionamento com Atividade
    id_atividade = db.relationship('Atividade', backref='notas')

    def __repr__(self):
        return f"<Notas {self.id}>"