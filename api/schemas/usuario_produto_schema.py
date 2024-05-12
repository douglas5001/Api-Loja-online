from api import ma
from ..models import produto_model
from marshmallow import fields

class AdicionarQuantidadeProdutoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = produto_model.Produto
        load_instance = True
        fields = ("id_usuario", "id_produto", "quantidade_produto")

    id_usuario = fields.Integer(required=True)
    id_produto = fields.Integer(required=True)
    quantidade_produto = fields.Integer(required=True)
