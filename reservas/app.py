import os
from model.reservas import Reserva
from model.db import db
from controller.reservas_controller import reservaController
from flask import Flask
from config import Config
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
swagger = Swagger(app)

with app.app_context():
    db.create_all()

app.add_url_rule('/criar_reserva', view_func=reservaController.criar,methods = ['POST'],endpoint='criar_reserva')

app.add_url_rule('/lista_reserva', view_func = reservaController.listar,methods = ['GET'],endpoint = 'listar_reserva')

app.add_url_rule('/atualiza_reserva/<int:id>', view_func=reservaController.atualizar,methods = ['PUT'],endpoint= 'atualiza_reserva')

app.add_url_rule('/deletar_reserva/<int:id>', view_func=reservaController.deletar,methods = ['DELETE'],endpoint= 'deletar_reserva')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)