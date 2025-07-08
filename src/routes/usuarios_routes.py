from flask import Blueprint, jsonify
from ..Controllers.Usuarios_controller import (
    get_usuarios,
    get_usuario,
    registrarse,
    login,
    eliminar_usuario,
    actualizar_usuario,
)
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

usuarios_bp = Blueprint("Usuarios", __name__)


@usuarios_bp.route(
    "/usuarios",
)

# Rutas para Películas
@usuarios_bp.route("/usuarios", methods=["GET"])
def get_all_usuarios_route():
    return get_usuarios()


@usuarios_bp.route("/usuarios/<int:usuario_id>", methods=["GET"])
def get_single_usuario_route(usuario_id):
    return get_usuario(usuario_id)


@usuarios_bp.route("/usuarios", methods=["POST"])
def get_create_usuario_route():
    return registrarse()


@usuarios_bp.route("/login", methods=["POST"])
def get_ingresar_usuario_route():
    return login()


@usuarios_bp.route("/usuarios/<int:usuario_id>", methods=["DELETE"])
def get_eliminar_usuario_route(usuario_id):
    return eliminar_usuario(usuario_id)


@usuarios_bp.route("/usuarios/<int:usuario_id>", methods=["PUT"])
def get_actualizar_usuario_route(usuario_id):
    return actualizar_usuario(usuario_id)
