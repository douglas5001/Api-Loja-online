from api import db
from api.entidades import usuario, produto
from api.models import produto_model

from api.services import usuario_service, produto_service


def cadastro_usuario_produto(user_prod, prod_anterior, prod_novo, user_anterior, user_novo):
    #usuario_db = usuario_service.listar_usuario_id(id_usuario)
    #produto_db = produto_service.listar_produto_id(id_produto)

    novo_usuario_produto = produto_model.usuario_produto(id_produto=user_prod.id_produto, id_usuario=user_prod.id_usuario, quantidade_produto=user_prod.quantidade_produto)
    prod_anterior.quantidade = prod_novo.quantidade

    db.session.add(novo_usuario_produto)
    db.session.commit()
