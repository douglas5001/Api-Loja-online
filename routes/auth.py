from flask import jsonify, Blueprint, request, make_response
from config import mysql
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

auth_blueprint = Blueprint('auth', __name__)

jwt = JWTManager()

@auth_blueprint.route('/login', methods=["GET"])
def get_all_usuarios():
    try:
        cursor = mysql.cursor(dictionary=True)
        cursor.execute('SELECT * from usuario')
        usuarios = cursor.fetchall()
        return jsonify(usuarios)
    except Exception as e:
        erro_message = f'Erro na consulta de usuários: {str(e)}'
        return make_response(jsonify({'erro': erro_message}), 500)


@jwt.user_loader_callback
def load_user(identity):
    cursor = mysql.cursor(dictionary=True)
    cursor.execute('SELECT * FROM usuario WHERE nome = %s', (identity,))
    user = cursor.fetchone()
    return user

@auth_blueprint.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    nome = data.get('nome')
    senha = data.get('senha')

    if not nome or not senha:
        return jsonify({'message': 'Credenciais incompletas'}), 400

    cursor = mysql.cursor(dictionary=True)
    cursor.execute('SELECT senha FROM usuario WHERE nome = %s', (nome,))
    user = cursor.fetchone()
    cursor.close()

    if not user or not check_password_hash(user['senha'], senha):
        return jsonify({'message': 'Credenciais inválidas'}), 401

    access_token = create_access_token(identity=nome)
    return jsonify(access_token=access_token), 200
