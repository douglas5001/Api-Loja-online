from api import db


class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
