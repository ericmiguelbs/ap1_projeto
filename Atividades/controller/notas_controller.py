from flask import request, jsonify
from model.db import db
from model.notas import Notas
import requests
from datetime import date

url = 'http://192.168.15.5:5000/lista_aluno'

class notasController:

    @staticmethod
    def listar():
        notas = Notas.query.all()
        return jsonify([
            {
                'id': n.id,
                'nota': n.nota,
                'id_aluno': n.id_aluno,
                'id_atividade':n.id_atividade,
            } for n in notas
        ])

    @staticmethod
    def criar():
        data = request.get_json()
        try:
            response = requests.get(url)
            response.raise_for_status()
            alunos = response.json()
            recebido = False
            for i in alunos:
               if i.get('id') == data['id_aluno']:
                  recebido = True
                  break
            if not recebido:
              return jsonify({'erro': f'O aluno com ID {data["id_aluno"]} não existe.'}), 404
            nota = Notas(
                nota = data['nota'],
                id_aluno = data['id_aluno'],
                id_atividade = data['id_atividade']
            )
            db.session.add(nota)
            db.session.commit()
            return jsonify({'mensagem': 'nota adicionada com sucesso!'}), 201
        except (KeyError, TypeError):
          return jsonify({'erro': 'Dados inválidos ou faltando.'}), 400
        
    @staticmethod
    def atualizar(id):
       nota = Notas.query.get_or_404(id)
       data = request.get_json()
       try:
            response = requests.get(url)
            response.raise_for_status()
            alunos = response.json()
            recebido = False
            for i in alunos:
               if i.get('id') == data['id_aluno']:
                  recebido = True
                  break
            if not recebido:
              return jsonify({'erro': f'O aluno com ID {data["id_aluno"]} não existe.'}), 404
        
            nota.nota = data.get('nota', nota.nota)
            nota.id_aluno = data.get('id_aluno', nota.id_aluno)
            nota.id_atividade = data.get('id_atividade', nota.id_atividade)

            db.session.commit()
            return jsonify({'mensagem':'Nota atualizada com sucesso!'})
       except (KeyError, TypeError):
            return jsonify({'erro': 'Dados inválidos ou faltando.'}), 400
          
    @staticmethod
    def deletar(id):
       notas = Notas.query.get_or_404(id)
       db.session.delete(notas)
       db.session.commit()
       return jsonify({'mensagem':'Nota deletada com sucesso!'})

           
        