from api import db
from .usuario_model import Usuario
from ..models import categoria_model

usuario_produto = db.Table(
    'usuario_produto',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('produto_id', db.Integer, db.ForeignKey('produto.id'), primary_key=True),
    db.Column('quantidade_produto', db.Integer, default=0)
)

class Produto(db.Model):
    __tablename__ = "produto"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    data_publicacao = db.Column(db.Date, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    imagem = db.Column(db.String(100), nullable=False)
    usuarios = db.relationship(Usuario, secondary="usuario_produto", back_populates="produtos")

    #Criando relacao
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"))
    categoria = db.relationship(categoria_model.Categoria, backref=db.backref("produtos", lazy="dynamic"))