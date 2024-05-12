from api import ma
from ..models import categoria_model
from marshmallow import fields
from ..schemas import produto_schema

class CategoriaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = categoria_model.Categoria
        load_instance = True
        fields = ("id", "nome", "descricao", "produtos")

    nome = fields.String(required=True)
    descricao = fields.String(required=True)
    produtos = fields.List(fields.Nested(produto_schema.ProdutoSchema, only=('id', 'nome')))