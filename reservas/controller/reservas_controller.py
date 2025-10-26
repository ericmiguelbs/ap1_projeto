from flask import request, jsonify
from model.db import db
from model.reservas import Reserva
import requests
from datetime import date

url = 'http://192.168.15.5:5000/lista_turmas'
url_reserva = 'http://192.168.15.5:5001/lista_reserva'

class reservaController:

    @staticmethod
    def listar():
        reservas = Reserva.query.all()
        return jsonify([
            {
                'id': t.id,
                'num_sala': t.num_sala,
                'lab': t.lab,
                'data':t.data.isoformat(),
                'id_turma': t.id_turma
            } for t in reservas
        ])

    @staticmethod
    def criar():
        data = request.get_json()
        try:
            response = requests.get(url)
            response.raise_for_status()
            turmas = response.json()
            recebido = False
            for i in turmas:
               if i.get('id') == data['id_turma']:
                  recebido = True
                  break
            if not recebido:
              return jsonify({'erro': f'A turma com ID {id} não existe.'}), 404
            reserva = Reserva(
                num_sala = data['num_sala'],
                lab = data['lab'],
                data= date.fromisoformat(data['data']),
                id_turma = data['id_turma']
            )
            db.session.add(reserva)
            db.session.commit()
            return jsonify({'mensagem': 'reserva adicionada com sucesso!'}), 201
        except (KeyError, TypeError):
          return jsonify({'erro': 'Dados inválidos ou faltando.'}), 400
        

    @staticmethod
    def atualizar(id):
        reserva = Reserva.query.get_or_404(id)
        data = request.get_json()
        try:
            response = requests.get(url)
            response.raise_for_status()
            turmas = response.json()
            recebido = False
            for i in turmas:
               if i.get('id') == data['id_turma']:
                  recebido = True
                  break
            if not recebido:
              return jsonify({'erro': f'Não foi possível atualizar a reserva, a turma com ID {id} não existe.'}), 404
            response_reserva = requests.get(url_reserva)
            response_reserva.raise_for_status()
            reservas = response_reserva.json()
            recebido_reserva = False
            for r in reservas:
               if r.get('id') == data['id']:
                recebido_reserva = True
                break
            if not recebido_reserva:
               return jsonify({'erro': f'Não foi possível atualizar a reserva, o ID {id} não existe.'}), 404
               
            reserva.num_sala = data.get('num_sala', reserva.num_sala)
            reserva.lab = data.get('lab', reserva.lab)
            reserva.data = date.fromisoformat(data['data'])
            reserva.id_turma = data.get('id_turma', reserva.id_turma)
            db.session.commit()
            return jsonify({'mensagem': 'Reserva atualizada com sucesso!'})
        except (KeyError, TypeError):
          return jsonify({'erro': 'Dados inválidos ou faltando.'}), 400
            


    def deletar(id):
        reserva = Reserva.query.get_or_404(id)
        db.session.delete(reserva)
        db.session.commit()
        return jsonify({'mensagem': 'Reserva deletada com sucesso!'})