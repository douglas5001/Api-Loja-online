import os

from flask_restful import Resource
from api import api, app
from ..schemas import produto_schema
from flask import request, make_response, jsonify
from ..entidades import produto
from ..services import produto_service, categoria_service
from ..paginate import paginate
from ..models.produto_model import Produto
from flask_jwt_extended import jwt_required, get_jwt
from ..decorator import admin_required
from ..services.produto_service import allowed_file, generate_random_filename


class ProdutoList(Resource):

    def get(self):
        pd = produto_schema.ProdutoSchema(many=True)
        return paginate(Produto,pd)

    @admin_required
    def post(self):
        pd = produto_schema.ProdutoSchema()
        validate = pd.validate(request.form)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.form["nome"]
            descricao = request.form["descricao"]
            data_publicacao = request.form["data_publicacao"]
            categoria = request.form["categoria"]
            imagem = request.files['imagem']
            categoria_produto = categoria_service.listar_categoria_id(categoria)
            if categoria_produto is None:
                return make_response(jsonify("categoria nao encontrada"), 404)

            if 'imagem' not in request.files or not allowed_file(imagem.filename):
                return make_response(jsonify("Imagem não enviada ou formato não permitido"), 400)
            random_filename = generate_random_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], random_filename))

            novo_produto = produto.Produto(nome=nome, descricao=descricao, data_publicacao=data_publicacao,
                                           categoria=categoria_produto, imagem=random_filename)
            resultado = produto_service.cadastrar_produto(novo_produto)
            x = pd.jsonify(resultado)
            return make_response(x, 201)


class ProdutoDetail(Resource):

    @jwt_required()
    def get(self, id):
        produto = produto_service.listar_produto_id(id)
        if produto is None:
            return make_response(jsonify("produto nao foi encontrado"), 404)
        pd = produto_schema.ProdutoSchema()
        return make_response(pd.jsonify(produto), 200)

    @admin_required
    def put(self, id):
        produto_bd = produto_service.listar_produto_id(id)
        if produto_bd is None:
            return make_response(jsonify("produto nao foi encontrado"), 404)
        pd = produto_schema.ProdutoSchema()
        validate = pd.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            data_publicacao = request.json["data_publicacao"]
            categoria = request.json["categoria"]
            categoria_produto = categoria_service.listar_categoria_id(categoria)
            if categoria_produto is None:
                return make_response(jsonify("categoria nao encontrada"), 404)
            novo_produto = produto.Produto(nome=nome, descricao=descricao, data_publicacao=data_publicacao, categoria=categoria_produto)
            produto_service.atualiza_produto(produto_bd, novo_produto)
            produto_atualizado = produto_service.listar_produto_id(id)
            return make_response(pd.jsonify(produto_atualizado), 200)

    @admin_required
    def delete(self, id):
        produto_bd = produto_service.listar_produto_id(id)
        if produto_bd is None:
            return make_response(jsonify("produto nao encontrado"), 404)
        produto_service.remove_produto(produto_bd)
        return make_response("produto excluido com sucesso", 204)


api.add_resource(ProdutoList, '/produtos')
api.add_resource(ProdutoDetail, '/produtos/<int:id>')