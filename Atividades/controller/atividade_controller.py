from flask import request, jsonify
from model.db import db
from model.atividade import Atividade
import requests
from datetime import date

url_professor = 'http://192.168.15.5:5000/listar_professores'
url_turma = 'http://192.168.15.5:5000/lista_turmas'

class atividadeController:

    @staticmethod
    def listar():
        atividades = Atividade.query.all()
        return jsonify([
            {
                'id': a.id,
                'nome_atividade': a.nome_atividade,
                'descricao': a.descricao,
                'peso_porcento': a.peso_porcento,
                'data_entrega': a.data_entrega,
                'turma_id': a.id_turma,
                'professor_id': a.id_professor
            } for a in atividades
        ])

    @staticmethod
    def criar():
        data = request.get_json()
        try:

            response_prof = requests.get(url_professor)
            response_prof.raise_for_status()
            professores = response_prof.json()

            response_turma = requests.get(url_turma)
            response_turma.raise_for_status()
            turmas = response_turma.json()

            professor_encontrado = False
            for p in professores:
                if str(p.get('id')) == str(data.get('id_professor')):
                    professor_encontrado = True
                    break
            if not professor_encontrado:
                return jsonify({'erro': f'O professor com ID {data.get("id_professor")} não existe.'}), 404

            turma_encontrada = False
            for t in turmas:
                if str(t.get('id')) == str(data.get('id_turma')):
                    turma_encontrada = True
                    break
            if not turma_encontrada:
                return jsonify({'erro': f'A turma com ID {data.get("id_turma")} não existe.'}), 404

            atividade = Atividade(
                nome_atividade = data['nome_atividade'],
                descricao = data['descricao'],
                peso_porcento = data['peso_porcento'],
                data_entrega = data.get('data_entrega', date.today()),
                id_turma = data['id_turma'],
                id_professor = data['id_professor']
            )

            db.session.add(atividade)
            db.session.commit()

            return jsonify({'mensagem': 'Atividade adicionada com sucesso!'}), 201

        except (KeyError, TypeError):
            return jsonify({'erro': 'Dados inválidos ou faltando.'}), 400
        except requests.exceptions.RequestException as e:
            return jsonify({'erro': f'Falha ao consultar professores ou turmas: {str(e)}'}), 500
