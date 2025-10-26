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
            id_aluno_enviado = data.get('id_aluno')
            nota_enviada = data.get('nota')
            id_atividade_enviada = data.get('id_atividade')

            if not id_aluno_enviado or nota_enviada is None or not id_atividade_enviada:
                return jsonify({'erro': 'Dados inválidos ou faltando (nota, id_aluno, id_atividade).'}), 400

            response = requests.get(url)
            response.raise_for_status()
            alunos = response.json()
            recebido = False
            for i in alunos:
                if str(i.get('id')) == str(id_aluno_enviado):
                    recebido = True
                    break
            if not recebido:
                return jsonify({'erro': f'O aluno com ID {id_aluno_enviado} não existe.'}), 404
            
            nota = Notas(
                nota = nota_enviada,
                id_aluno = id_aluno_enviado,
                id_atividade = id_atividade_enviada
            )
            db.session.add(nota)
            db.session.commit()
            return jsonify({'mensagem': 'nota adicionada com sucesso!'}), 201
        
        except (KeyError, TypeError):
            return jsonify({'erro': 'Dados inválidos ou faltando.'}), 400
        except requests.exceptions.RequestException as e:
            return jsonify({'erro': f'Falha ao consultar alunos: {str(e)}'}), 500
        
    @staticmethod
    def atualizar(id):
        nota = Notas.query.get_or_404(id)
        data = request.get_json()
        try:
            if 'id_aluno' in data:
                id_aluno_novo = data.get('id_aluno')
                
                response = requests.get(url)
                response.raise_for_status()
                alunos = response.json()
                recebido = False
                for i in alunos:
                    if str(i.get('id')) == str(id_aluno_novo):
                        recebido = True
                        break
                if not recebido:
                    return jsonify({'erro': f'O aluno com ID {id_aluno_novo} não existe.'}), 404
            
            nota.nota = data.get('nota', nota.nota)
            nota.id_aluno = data.get('id_aluno', nota.id_aluno)
            nota.id_atividade = data.get('id_atividade', nota.id_atividade)

            db.session.commit()
            return jsonify({'mensagem':'Nota atualizada com sucesso!'})
        
        except (KeyError, TypeError):
            return jsonify({'erro': 'Dados inválidos ou faltando.'}), 400
        except requests.exceptions.RequestException as e:
            return jsonify({'erro': f'Falha ao consultar alunos: {str(e)}'}), 500
                
    @staticmethod
    def deletar(id):
       nota = Notas.query.get_or_404(id)
       db.session.delete(nota)
       db.session.commit()
       return jsonify({'mensagem':'Nota deletada com sucesso!'})

           
        