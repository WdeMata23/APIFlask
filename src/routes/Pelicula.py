from flask import Blueprint, jsonify
from Models.PeliculaModel import PeliculaModel

main = Blueprint("movie_blueprint", __name__)


@main.route("/")
def get_movies():
    try:
        pelicula = PeliculaModel.get_pelicula()
        return jsonify(pelicula)
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
