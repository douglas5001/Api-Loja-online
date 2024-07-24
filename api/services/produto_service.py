import os
from ..models import produto_model, usuario_model
from api import db, app
from config import ALLOWED_EXTENSIONS
import uuid

from ..models.produto_model import usuario_produto


def cadastrar_produto(produto):
    produto_bd = produto_model.Produto(nome=produto.nome, descricao=produto.descricao, data_publicacao=produto.data_publicacao, categoria=produto.categoria, quantidade=produto.quantidade, imagem=produto.imagem)

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
    produto_anterior.quantidade = produto_novo.quantidade
    produto_anterior.categoria = produto_novo.categoria
    produto_anterior.imagem = produto_novo.imagem
    db.session.commit()

def adiciona_quantidade(produto):
    produto_db = produto_model.Produto(produto.quantidade)
    db.session.add(produto_db)
    db.session.commit()
    return produto_db

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

def adicionar_quantidade_produto(id_usuario, id_produto, quantidade_produto):
    try:
        quantidade_produto = int(quantidade_produto)
    except ValueError:
        return False, "A quantidade do produto deve ser um número inteiro."

    usuario = usuario_model.Usuario.query.get(id_usuario)
    produto = produto_model.Produto.query.get(id_produto)
    if not usuario or not produto:
        return False, "Usuário ou produto não encontrado."

    if produto not in usuario.produtos:
        usuario.produtos.append(produto)
        db.session.commit()
    relacao_usuario_produto = db.session.query(usuario_produto).filter_by(usuario_id=id_usuario, produto_id=id_produto).first()
    if relacao_usuario_produto:
        nova_quantidade = relacao_usuario_produto.quantidade_produto + quantidade_produto
        if nova_quantidade >= 0:
            db.session.query(usuario_produto).filter_by(usuario_id=id_usuario, produto_id=id_produto).update({'quantidade_produto': nova_quantidade})
        else:
            return False, "A quantidade do produto não pode ser negativa."
    else:
        nova_relacao = usuario_produto.insert().values(usuario_id=id_usuario, produto_id=id_produto, quantidade_produto=quantidade_produto)
        db.session.execute(nova_relacao)
    produto.quantidade -= quantidade_produto

    db.session.commit()

    return True, "Quantidade do produto atualizada com sucesso."


