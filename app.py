from flask import Flask, jsonify, render_template, make_response, request
from config import mysql

app = Flask(__name__)


@app.route('/')
def method_main():
    return render_template("index.html")

@app.route('/produtos')
def get_product_all():
    try:
        cursor = mysql.cursor(dictionary=True)
        cursor.execute('SELECT * FROM produto')
        produtos = cursor.fetchall()
        return jsonify(produtos)
    except:
        error_message = 'Erro na conexão com o banco de dados.'
        return make_response(jsonify({'error': error_message}), 500)
    
@app.route('/produtos', methods=["POST"])
def create_product():
    try:    
        data = request.get_json()
        cursor = mysql.cursor()
        cursor.execute('INSERT INTO produto (name, category, price, marca) VALUES (%s, %s, %s, %s)',
                       (data['name'], data['category'], data['price'], data['marca']))  # Corrigido
        mysql.commit()
        cursor.close()
        return jsonify({'message': 'Produto criado com sucesso'})
    
    except Exception as e:  # Capturar exceção para obter detalhes do erro
        erro_message = f'Erro no POST de produto: {str(e)}'
        return make_response(jsonify({'erro': erro_message}), 500)  
    
@app.route('/produtos/<int:id>', methods=["DELETE"])
def delete_product(id):
    try:
        cursor = mysql.cursor()
        cursor.execute('DELETE FROM produto WHERE id = %s', (id,))
        mysql.commit()
        cursor.close()
        return jsonify({'message': 'Produto excluído com sucesso'})
    except Exception as e:
        erro_message = f'Erro na exclusão do produto: {str(e)}'
        return make_response(jsonify({'erro': erro_message}), 500)
    
    

if __name__ == '__main__':
    app.run(port=8000, host='localhost', debug=True)
