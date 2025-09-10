from models import db

class Turma(db.Model):
    __tablename__ = 'turma'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    # Relacionamento com a tabela Professor
    professor = db.relationship('Professor', back_populates='turmas')

    # Relacionamento com a tabela Aluno
    alunos = db.relationship('Aluno', back_populates='turma', lazy=True)

    def __repr__(self):
        return f"<Turma {self.descricao}>"
