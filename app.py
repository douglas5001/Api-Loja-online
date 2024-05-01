from flask import Flask, request, render_template, jsonify, make_response
from utils.sqlServerConnector import sqlConnector
from utils.sqlServerConnector import extract_data
from utils.config import SELECT_QUERIES

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/produto', methods=['GET'])
def method_main():
    data = extract_data(SELECT_QUERIES['produto'])
    return make_response(
        jsonify(
            mensagem='Lista de produtos',
            dados=data
        )
    )


app.run(port=8000,host='localhost',debug=True)
