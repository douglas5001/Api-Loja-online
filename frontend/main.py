from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Lógica de autenticação aqui
        return redirect(url_for('principal'))
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(port=8001, host='localhost', debug=True)
