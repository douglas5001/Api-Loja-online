from api import ma
from . import produto_schema, usuario_produto_schema
from .produto_schema import ProdutoSchema
from marshmallow import fields

from ..models import usuario_model, produto_model

class UsuarioSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = usuario_model.Usuario
        load_instance = True
        fields = ("id", "nome", "email", "senha", "is_admin")

    nome = fields.String(required=True)
    email = fields.String(required=True)
    senha = fields.String(required=True)
    is_admin = fields.Boolean(required=True)
