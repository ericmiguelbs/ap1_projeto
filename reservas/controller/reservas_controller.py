from flask import request, jsonify
from model.db import db
from model.reservas import Reserva
import requests
from datetime import date
from requests.exceptions import RequestException, HTTPError, JSONDecodeError, ConnectionError

url = 'http://api_gerenciamento:5000/lista_turmas'
url_reserva = 'http://api_reserva:5001/lista_reserva'

class reservaController:

    @staticmethod
    def listar():
        """
        Lista todas as reservas de salas/laboratórios.
        """
        try:
            reservas = Reserva.query.all()
            return jsonify([
                {
                    'id': t.id,
                    'num_sala': t.num_sala,
                    'lab': t.lab,
                    'data': t.data.isoformat(),
                    'id_turma': t.id_turma
                } for t in reservas
            ])
        except Exception as e:
            return jsonify({'erro': f'Falha ao listar reservas: Erro interno do servidor local. Detalhes: {str(e)}'}), 500

    @staticmethod
    def criar():
        """
        Cria uma nova reserva para uma turma.
        """
        data = request.get_json()
        try:
            reserva_data = {
                'num_sala': data['num_sala'],
                'lab': data['lab'],
                'data': date.fromisoformat(data['data']),
                'id_turma': data['id_turma']
            }
        except (KeyError, TypeError, ValueError):
            return jsonify({'erro': 'Dados inválidos ou faltando (verifique a presença de num_sala, lab, data, id_turma e o formato da data AAAA-MM-DD).'}), 400
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status() 
          
            turmas = response.json()
            
            id_turma_enviada = reserva_data['id_turma']
            recebido = False
            for i in turmas:
                if str(i.get('id')) == str(id_turma_enviada): 
                    recebido = True
                    break
            
            if not recebido:
                return jsonify({'erro': f'A turma com ID {id_turma_enviada} não existe.'}), 404
            reserva = Reserva(
                num_sala = reserva_data['num_sala'],
                lab = reserva_data['lab'],
                data = reserva_data['data'],
                id_turma = reserva_data['id_turma']
            )
            db.session.add(reserva)
            db.session.commit()
            return jsonify({'mensagem': 'reserva adicionada com sucesso!'}), 201
        
        except JSONDecodeError:
            status = response.status_code if 'response' in locals() else 'N/A'
            return jsonify({'erro': f'Falha no serviço de turmas. O servidor {url} retornou o status {status}, mas o conteúdo não é JSON válido.'}), 500
        
        except HTTPError as e:
            return jsonify({'erro': f'Falha na validação da turma: O serviço externo retornou um erro HTTP {e.response.status_code}.'}), 500
        
        except RequestException as e:
            return jsonify({'erro': f'Falha de conexão ao consultar turmas: {str(e)}'}), 500
        
        except Exception as e:
            return jsonify({'erro': f'Erro interno desconhecido ao tentar criar a reserva: {str(e)}'}), 500


    @staticmethod
    def atualizar(id):
        """
        Atualiza uma reserva existente pelo seu ID.
        """
        reserva = Reserva.query.get_or_404(id)
        data = request.get_json()
        
        try:
            response_turma = requests.get(url, timeout=5)
            response_turma.raise_for_status()
            turmas = response_turma.json()
            
            id_turma_enviada = data.get('id_turma', reserva.id_turma) 
            recebido_turma = False
            for i in turmas:
                if str(i.get('id')) == str(id_turma_enviada):
                    recebido_turma = True
                    break
            
            if not recebido_turma:
                return jsonify({'erro': f'Não foi possível atualizar a reserva, a turma com ID {id_turma_enviada} não existe.'}), 404

            response_reserva = requests.get(url_reserva, timeout=5)
            response_reserva.raise_for_status()
            reservas = response_reserva.json()
            
            recebido_reserva = False
            for r in reservas:
                if r.get('id') == id:
                    recebido_reserva = True
                    break
            
            if not recebido_reserva:
                return jsonify({'erro': f'Não foi possível atualizar a reserva, o ID {id} não existe no serviço externo.'}), 404

            reserva.num_sala = data.get('num_sala', reserva.num_sala)
            reserva.lab = data.get('lab', reserva.lab)
            
            if 'data' in data:
                 reserva.data = date.fromisoformat(data['data'])
            
            reserva.id_turma = data.get('id_turma', reserva.id_turma)
            
            db.session.commit()
            return jsonify({'mensagem': 'Reserva atualizada com sucesso!'})
        
        except (KeyError, TypeError, ValueError) as e:
            return jsonify({'erro': f'Dados inválidos ou faltando (verifique o formato da data AAAA-MM-DD e se o JSON está completo): {str(e)}'}), 400
        
        except JSONDecodeError as e:
            return jsonify({'erro': f'Falha ao processar a resposta de um serviço externo. O conteúdo retornado não é JSON válido. Detalhes: {str(e)}'}), 500
        
        except HTTPError as e:
            return jsonify({'erro': f'Falha na validação: Um serviço externo retornou um erro HTTP {e.response.status_code}.'}), 500
        
        except RequestException as e:
            return jsonify({'erro': f'Falha de conexão ao consultar serviços externos: {str(e)}'}), 500
            
    @staticmethod 
    def deletar(id):
        """
        Deleta uma reserva pelo seu ID.
        """
        try:
            reserva = Reserva.query.get_or_404(id)
            db.session.delete(reserva)
            db.session.commit()
            return jsonify({'mensagem': 'Reserva deletada com sucesso!'})
        except Exception as e:
            return jsonify({'erro': f'Falha ao deletar reserva: {str(e)}'}), 500
