from datetime import datetime
from flask import Flask, request, render_template, jsonify, make_response
from utils.sqlServerConnector import sqlConnector
from utils.sqlServerConnector import extract_data
from utils.config import GET_QUERIES

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/produto', methods=['GET'])
def get_produto():

    conn = sqlConnector()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT id, name, category, price, marca FROM db_lojavirtual.produto;""")
    data = cursor.fetchall()

    data_list = list()

    for produto in data:
        data_list.append(
        {
            'id': produto[0],
            'category': produto[2],
            'name': produto[1],
            'price': produto[3],
            'marca': produto[4]
        })

    return make_response(
        jsonify(
            mensagem='Lista de produtos',
            data=data_list
        )
    )


@app.route('/produto', methods=['POST'])
def post_produto():
    produto = request.json

    conn = sqlConnector()
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO db_lojavirtual.produto (name, category, price, marca) VALUES ('{produto['name']}', '{produto['category']}', '{produto['price']}', '{produto['marca']}');""")
    conn.commit()
    conn.close()

    return make_response(
        jsonify(
            mensagem='Produto cadastrado com sucesso',
            dados=produto
        )
    )


app.run(port=8000,host='localhost',debug=True)
