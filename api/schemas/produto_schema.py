from api import ma
from ..models import produto_model
from marshmallow import fields

class ProdutoSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = produto_model.Produto
        load_instance = True
        fields = ("id", "nome", "descricao", "data_publicacao", "categoria_id", "quantidade", "imagem", "_links")

    nome = fields.String(required=True)
    descricao = fields.String(required=True)
    data_publicacao = fields.Date(required=True)
    categoria_id = fields.String(required=True)
    quantidade = fields.Integer(required=True)
    imagem = fields.String(required=False)
    #categoria = fields.List(fields.Nested(categoria_schema.CategoriaSchema, only=('id')))

    _links = ma.Hyperlinks(
        {
            "get":ma.URLFor("produtodetail", id="<id>"),
            "put":ma.URLFor("produtodetail", id="<id>"),
            "delete":ma.URLFor("produtodetail", id="<id>")
        }
    )