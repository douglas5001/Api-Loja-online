from ..models import categoria_model
from api import db

def cadastrar_categoria(categoria):
    categoria_bd = categoria_model.Categoria(nome=categoria.nome, descricao=categoria.descricao)
    db.session.add(categoria_bd)
    db.session.commit()
    return categoria_bd

def listar_categoria():
    categorias = categoria_model.Categoria.query.all()
    return categorias

def listar_categoria_id(id):
    categoria = categoria_model.Categoria.query.filter_by(id=id).first()
    return categoria

def atualiza_categoria(categoria_anterior, categoria_novo):
    categoria_anterior.nome = categoria_novo.nome
    categoria_anterior.descricao = categoria_novo.descricao
    db.session.commit()

def remove_categoria(categoria):
    db.session.delete(categoria)
    db.session.commit()