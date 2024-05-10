from flask_restful import Resource
from api import api
from ..schemas import categoria_schema
from flask import request, make_response, jsonify
from ..entidades import categoria
from ..services import categoria_service
from ..paginate import paginate
from ..models.categoria_model import Categoria
from flask_jwt_extended import jwt_required

class CategoriaList(Resource):
    #@jwt_required()
    def get(self):
        #ADICIONANDO O SCRIPT DE PAGINACAO
        #categorias = categoria_service.listar_categoriass()
        cs = categoria_schema.CategoriaSchema(many=True)
        #return make_response(cs.jsonify(categorias), 200)
        return paginate(Categoria, cs)

    @jwt_required()
    def post(self):
        pd = categoria_schema.CategoriaSchema()
        validate = pd.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            novo_categoria = categoria.Categoria(nome=nome, descricao=descricao)
            resultado = categoria_service.cadastrar_categoria(novo_categoria)
            x = pd.jsonify(resultado)
            return make_response(x, 201)

class CategoriaDetail(Resource):
    #@jwt_required()
    def get(self, id):
        categoria = categoria_service.listar_categoria_id(id)
        if categoria is None:
            return make_response(jsonify("categoria nao foi encontrada"), 404)
        cs = categoria_schema.CategoriaSchema()
        return make_response(cs.jsonify(categoria), 200)

    @jwt_required()
    def put(self, id):
        categoria_bd = categoria_service.listar_categoria_id(id)
        if categoria_bd is None:
            return make_response(jsonify("categoria nao foi encontrada"), 404)
        cs = categoria_schema.CategoriaSchema()
        validate = cs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            novo_categoria = categoria.Categoria(nome=nome, descricao=descricao)
            categoria_service.atualiza_categoria(categoria_bd, novo_categoria)
            categoria_atualizado = categoria_service.listar_categoria_id(id)
            return make_response(cs.jsonify(categoria_atualizado), 200)

    @jwt_required()
    def delete(self, id):
        categoria_bd = categoria_service.listar_categoria_id(id)
        if categoria_bd is None:
            return make_response(jsonify("categoria nao encontrada"), 404)
        categoria_service.remove_categoria(categoria_bd)
        return make_response("categoria excluido com sucesso", 204)


api.add_resource(CategoriaList, '/categorias')
api.add_resource(CategoriaDetail, '/categorias/<int:id>')