from flask import jsonify, request
from http import HTTPStatus
from ..database.database import SessionLocal
from ..Models.Pelicula import Pelicula


def get_peliculas():
    """
    Obtiene todas las películas de la base de datos.
    """
    db = SessionLocal()  # Abre una nueva sesión de base de datos
    try:
        peliculas = db.query(Pelicula).all()
        # Convierte los objetos Pelicula a un formato JSON
        peliculas_data = [
            {
                "id": pelicula.id,
                "titulo": pelicula.titulo,
                "duracion": pelicula.duracion,
                "fechaEstreno": (
                    pelicula.fechaEstreno.isoformat() if pelicula.fechaEstreno else None
                ),
                "horaCreacion": (
                    pelicula.horaCreacion.isoformat() if pelicula.horaCreacion else None
                ),
                "horaActualizacion": (
                    pelicula.horaActualizacion.isoformat()
                    if pelicula.horaActualizacion
                    else None
                ),
            }
            for pelicula in peliculas
        ]
        return jsonify(peliculas_data), HTTPStatus.OK
    except Exception as e:
        # Manejo de errores
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        db.close()  # Cierra la sesión de base de datos


def get_pelicula(pelicula_id):
    """
    Obtiene una película por su ID.
    """
    db = SessionLocal()
    try:
        pelicula = db.query(Pelicula).filter(Pelicula.id == pelicula_id).first()
        if not pelicula:
            return jsonify({"message": "Película no encontrada"}), HTTPStatus.NOT_FOUND

        pelicula_data = {
            "id": pelicula.id,
            "titulo": pelicula.titulo,
            "duracion": pelicula.duracion,
            "fechaEstreno": (
                pelicula.fechaEstreno.isoformat() if pelicula.fechaEstreno else None
            ),
            "horaCreacion": (
                pelicula.horaCreacion.isoformat() if pelicula.horaCreacion else None
            ),
            "horaActualizacion": (
                pelicula.horaActualizacion.isoformat()
                if pelicula.horaActualizacion
                else None
            ),
        }
        return jsonify(pelicula_data), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        db.close()
