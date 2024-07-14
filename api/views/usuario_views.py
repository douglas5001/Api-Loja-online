from flask_restful import Resource
from api import api
from ..schemas import usuario_schema, usuario_produto_schema
from flask import request, make_response, jsonify
from ..entidades import usuario
from ..services import usuario_service, usuario_produto_service


class UsuarioList(Resource):

    def get(self):
        usuarios = usuario_service.listar_usuario()
        us = usuario_schema.UsuarioSchema(many=True)
        return make_response(us.jsonify(usuarios))

    def post(self):
        us = usuario_schema.UsuarioSchema()
        validate = us.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            email = request.json["email"]
            senha = request.json["senha"]
            is_admin = request.json["is_admin"]
            novo_usuario = usuario.Usuario(nome=nome, email=email, senha=senha, is_admin=is_admin)
            resultado = usuario_service.cadastrar_usuario(novo_usuario)
            x = us.jsonify(resultado)
            return make_response(x, 201)

class usuarioObtem_produto(Resource):
    def post(self, id):
        id_user = usuario_service.listar_usuario_id(id)
        if id_user is None:
            make_response('usuario nao existe')
        else:
            user_pd = usuario_produto_schema.AdicionarQuantidadeProdutoSchema()
            validate = user_pd.validate(request.json)
            if validate:
                make_response(jsonify(validate), 400)
            else:
                id_prod = request.json['id']
                if id_prod is None:
                    make_response('produto nao existe')
                else:
                    usuario_bd = usuario.Usuario(produtos=id_prod)
                    novo_usuario = usuario_produto_service(usuario_bd)




api.add_resource(UsuarioList, '/usuarios')
api.add_resource(usuarioObtem_produto, '/user_obtem_produto')
