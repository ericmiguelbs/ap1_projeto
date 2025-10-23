from model.db import db

class Reserva(db.Model):
    __tablename__ = 'reserva'

    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.Integer, nullable=False)
    lab= db.Column(db.Boolean, nullable=False)
    data = db.Column(db.Date, nullable=False, default=True)
    id_turma= db.Column(db.Integer, nullable = False)
    def __repr__(self):
        return f"<Turma {self.descricao}>"