import os
from models.aluno import Aluno
from models.turma import Turma
from models.professor import Professor
from flask import Flask
from config import Config
from controller.turma_controller import TurmaController
from flasgger import Swagger
from controller.aluno_controller import AlunoController
from controller.professor_controller import ProfessorController

from models.db import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
swagger = Swagger(app)

with app.app_context():
    db.create_all()

app.add_url_rule('/lista_aluno', view_func=AlunoController.listar,methods = ['GET'],endpoint='listar_alunos')

app.add_url_rule('/atualiza_aluno', view_func=AlunoController.atualizar,methods = ['PUT'],endpoint='atualiza_aluno')

app.add_url_rule('/deleta_aluno', view_func=AlunoController.deletar,methods = ['DELETE'],endpoint='deleta_aluno')

app.add_url_rule('/criar_aluno', view_func=AlunoController.criar,methods = ['POST'],endpoint='criar_alunos')

app.add_url_rule('/lista_professor', view_func = ProfessorController.listar,methods = ['GET'],endpoint = 'listar_professores')

app.add_url_rule('/adiciona_professor', view_func = ProfessorController.criar,methods = ['POST'],endpoint = 'adiciona_professores')
app.add_url_rule('/deleta_professor', view_func = ProfessorController.deletar,methods = ['DELETE'],endpoint = 'deleta_professores')
app.add_url_rule('/atualiza_professor', view_func = ProfessorController.atualizar,methods = ['PUT'],endpoint = 'atualiza_professores')

app.add_url_rule('/lista_turmas', view_func=TurmaController.listar, methods=['GET'], endpoint='lista_turmas')
app.add_url_rule('/cria_turmas', view_func=TurmaController.criar, methods=['POST'], endpoint='cria_turmas')
app.add_url_rule('/atualiza_turmas/<int:id>', view_func=TurmaController.atualizar, methods=['PUT'], endpoint='atualiza_turmas')
app.add_url_rule('/tdeleta_turmas/<int:id>', view_func=TurmaController.deletar, methods=['DELETE'], endpoint='deleta_turmas')

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug = True)