from api import ma
from ..models import produto_model
from marshmallow import fields

class ProdutoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = produto_model.Produto
        load_instance = True
        fields = ("id", "nome", "descricao", "data_publicacao", "categoria", "_links")

    nome = fields.String(required=True)
    descricao = fields.String(required=True)
    data_publicacao = fields.Date(required=True)
    categoria = fields.String(required=True)

    _links = ma.Hyperlinks(
        {
            "get":ma.URLFor("prdutodetail", id="<id>"),
            "put":ma.URLFor("produtodetail", id="<id>"),
            "delete":ma.URLFor("produtodetail", id="<id>")
        }
    )