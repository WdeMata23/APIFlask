from flask import Blueprint, jsonify

peliculas_bp = Blueprint("peliculas", __name__)


@peliculas_bp.route("/peliculas", methods=["GET"])
def get_peliculas():
    # En Flask, usamos jsonify para convertir diccionarios a respuestas JSON.
    return jsonify({"mensaje": "Aquí se devolverán todas las películas"})


@peliculas_bp.route("/peliculas/<int:id>", methods=["GET"])
def get_pelicula(id):

    return jsonify({"mensaje": f"Devolviendo la película con id {id}"})
