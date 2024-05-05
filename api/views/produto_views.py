from flask_restful import Resource
from api import api
from ..schemas import produto_schema
from flask import request, make_response, jsonify
from ..entidades import produto
from ..services import produto_service, categoria_service
from ..paginate import paginate
from ..models.produto_model import Produto
from flask_jwt_extended import jwt_required, get_jwt
from ..decorator import admin_required

class ProdutoList(Resource):

    def get(self):
        pd = produto_schema.ProdutoSchema(many=True)
        return paginate(Produto,pd)

    @admin_required
    def post(self):
        cs = produto_schema.ProdutoSchema()
        validate = cs.validate(request.json)
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
            resultado = produto_service.cadastrar_produto(novo_produto)
            x = cs.jsonify(resultado)
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