import os
from model.db import db
from model.atividade import Atividade
from controller.atividade_controller import atividadeController
from model.notas import Notas
from controller.notas_controller import notasController
from flask import Flask
from config import Config
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
swagger = Swagger(app)

with app.app_context():
    db.create_all()

app.add_url_rule('/criar_atividade', view_func=atividadeController.criar,methods = ['POST'],endpoint='criar_atividade')

app.add_url_rule('/listar_atividade', view_func = atividadeController.listar,methods = ['GET'],endpoint = 'listar_atividade')

app.add_url_rule('/atualizar_atividade/<int:id>', view_func=atividadeController.atualizar,methods= ['PUT'], endpoint='atualizar_atividade')

app.add_url_rule('/deletar_atividade/<int:id>', view_func=atividadeController.deletar,methods = ['DELETE'],endpoint='deletar_atividade')

app.add_url_rule('/criar_notas', view_func=notasController.criar,methods = ['POST'],endpoint='criar_notas')

app.add_url_rule('/listar_notas', view_func = notasController.listar,methods = ['GET'],endpoint = 'listar_notas')

app.add_url_rule('/atualizar_nota/<int:id>', view_func=notasController.atualizar, methods= ['PUT'],endpoint='atualizar_nota')

app.add_url_rule('/deletar_nota/<int:id>', view_func=notasController.deletar, methods = ['DELETE'], endpoint='deletar_nota')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)