from flask import Blueprint, jsonify
from ..Controllers.Usuarios_controller import (
    get_usuarios,
    get_usuario,
    crear_usuario,
    ingresar_usuario,
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
    return crear_usuario()


@usuarios_bp.route("/login", methods=["POST"])
def get_ingresar_usuario_route():
    return ingresar_usuario()
