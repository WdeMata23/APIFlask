from flask import Blueprint, jsonify
from ..Controllers.peliculas_controller import (
    get_pelicula,
    get_peliculas,
    crear_pelicula,
    actualizar_pelicula,
    Eliminar_pelicula,
)
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

peliculas_bp = Blueprint("peliculas", __name__)


@peliculas_bp.route(
    "/peliculas",
)

# Rutas para Películas
@peliculas_bp.route("/peliculas", methods=["GET"])
def get_all_peliculas_route():
    return get_peliculas()


@peliculas_bp.route("/peliculas/<int:pelicula_id>", methods=["GET"])
def get_single_pelicula_route(pelicula_id):
    return get_pelicula(pelicula_id)


@peliculas_bp.route("/peliculas", methods=["POST"])
@jwt_required()
def create_all_peliculas_route():
    return crear_pelicula()


@peliculas_bp.route("/peliculas/<int:pelicula_id>", methods=["PUT"])
@jwt_required()
def actualizar_all_peliculas_route(pelicula_id):
    return actualizar_pelicula(pelicula_id)


@peliculas_bp.route("/peliculas/<int:pelicula_id>", methods=["DELETE"])
@jwt_required()
def Eliminar_all_peliculas_route(pelicula_id):
    return Eliminar_pelicula(pelicula_id)
