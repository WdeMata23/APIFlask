from flask import Blueprint, jsonify
from ..Controllers.peliculas_controller import get_pelicula, get_peliculas


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
