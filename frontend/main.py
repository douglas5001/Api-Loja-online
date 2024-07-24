import requests
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory
import urllib.request, json
app = Flask(__name__)


app.secret_key = 'aplicacao_flask'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:bola2020@85.239.239.196/db_lojavirtual'


@app.route('/')
def principal():
    return render_template('produtos.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Lógica de autenticação aqui
        return redirect(url_for('principal'))
    return render_template('login.html')


# Configure o caminho para a pasta de uploads
UPLOAD_FOLDER = '/Users/douglasportella/SENAC/programacao-fullstack/projeto final/loja_de_roupa_Fullstack/api/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    if request.method == 'POST':
        # Código para criação de novo produto
        new_product = {
            "nome": request.form['nome'],
            "descricao": request.form['descricao'],
            "quantidade": request.form['quantidade'],
            "categoria_id": request.form['categoria_id'],
            "data_publicacao": request.form['data_publicacao'],
            "imagem": request.form['imagem']
        }
        response = requests.post('http://localhost:8000/produtos', json=new_product)
        return redirect(url_for('produtos'))

    page = request.args.get('page', 1, type=int)
    per_page = 3
    response = requests.get(f'http://localhost:8000/produtos?page={page}&per_page={per_page}')
    if response.status_code == 200:
        data = response.json()
        todos_cursos = data['results']
    else:
        todos_cursos = []

    return render_template("produtos.html", cursos=todos_cursos, next_page=data.get('next'), prev_page=data.get('prev'))

@app.route('/produtos/delete/<int:id>', methods=['POST'])
def delete_produto(id):
    response = requests.delete(f'http://localhost:8000/produtos/{id}')
    return redirect(url_for('produtos'))

@app.route('/produtos/update/<int:id>', methods=['POST'])
def update_produto(id):
    updated_product = {
        "nome": request.form['nome'],
        "descricao": request.form['descricao'],
        "quantidade": request.form['quantidade'],
        "categoria_id": request.form['categoria_id'],
        "data_publicacao": request.form['data_publicacao'],
        "imagem": request.form['imagem']
    }
    response = requests.put(f'http://localhost:8000/produtos/{id}', json=updated_product)
    return redirect(url_for('produtos'))

if __name__ =="__main__":
    with app.app_context():
        app.run(port=8001,host='localhost', debug=True,)
