from api import db
from ..models import categoria_model

class Produto(db.Model):
    __tablename__ = "produto"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    data_publicacao = db.Column(db.Date, nullable=False)

    #Criando relacao
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"))
    categoria = db.relationship(categoria_model.Categoria, backref=db.backref("produtos", lazy="dynamic"))