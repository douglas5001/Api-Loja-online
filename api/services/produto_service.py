import os
from ..models import produto_model
from api import db, app
from config import ALLOWED_EXTENSIONS
import uuid
def cadastrar_produto(produto):
    produto_bd = produto_model.Produto(nome=produto.nome, descricao=produto.descricao, data_publicacao=produto.data_publicacao, categoria=produto.categoria, imagem=produto.imagem)

    db.session.add(produto_bd)
    db.session.commit()
    return produto_bd

def listar_produto():
    produto = produto_model.Produto.query.all()
    return produto

def listar_produto_id(id):
    produto = produto_model.Produto.query.filter_by(id=id).first()
    return produto

def atualiza_produto(produto_anterior, produto_novo):
    produto_anterior.nome = produto_novo.nome
    produto_anterior.descricao = produto_novo.descricao
    produto_anterior.data_publicacao = produto_novo.data_publicacao
    produto_anterior.categoria = produto_novo.categoria
    db.session.commit()

def remove_produto(produto):
    db.session.delete(produto)
    db.session.commit()
    if produto.imagem:
        # Remova o arquivo de imagem associado, se existir
        imagem_path = os.path.join(app.config['UPLOAD_FOLDER'], produto.imagem)
        if os.path.exists(imagem_path):
            os.remove(imagem_path)


def generate_random_filename(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    random_filename = str(uuid.uuid4()) + '.' + ext
    return random_filename

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
