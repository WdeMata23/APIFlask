from flask import jsonify, request
from http import HTTPStatus
from ..database.database import SessionLocal
from ..Models.Pelicula import Pelicula
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt


# funcion para listar todas las peliculas
def get_peliculas():

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


# funcion para listar solo una pelicula por el id
def get_pelicula(pelicula_id):

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


# funcion para crear una pelicula
def crear_pelicula():
    # Obtiene todos los claims del token (incluido el Rol)
    claims = get_jwt()
    user_role = claims.get("Rol")

    if user_role != "Administrador":
        return (
            jsonify({"message": "No tiene autorización para realizar esta acción."}),
            HTTPStatus.FORBIDDEN,
        )
    db = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return (
                jsonify({"message": "No se proporcionaron datos JSON"}),
                HTTPStatus.BAD_REQUEST,
            )

        fecha_estreno_str = data.get("fechaEstreno")
        fecha_estreno = None
        if fecha_estreno_str:
            try:
                fecha_estreno = datetime.fromisoformat(fecha_estreno_str)
                try:
                    fecha_estreno = datetime.strptime(fecha_estreno_str, "%Y-%m-%d")
                except ValueError:
                    return (
                        jsonify(
                            {
                                "message": "Formato de fechaEstreno inválido. Use YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS"
                            }
                        ),
                        HTTPStatus.BAD_REQUEST,
                    )
                nueva_pelicula = Pelicula(
                    titulo=data["titulo"],
                    duracion=data["duracion"],
                    fechaEstreno=fecha_estreno,
                )
                db.add(nueva_pelicula)
                db.commit()
                db.refresh(nueva_pelicula)

                pelicula_data = {
                    "id": nueva_pelicula.id,
                    "titulo": nueva_pelicula.titulo,
                    "duracion": nueva_pelicula.duracion,
                    "fechaEstreno": (
                        nueva_pelicula.fechaEstreno.isoformat()
                        if nueva_pelicula.fechaEstreno
                        else None
                    ),
                    "horaCreacion": (
                        nueva_pelicula.horaCreacion.isoformat()
                        if nueva_pelicula.horaCreacion
                        else None
                    ),
                    "horaActualizacion": (
                        nueva_pelicula.horaActualizacion.isoformat()
                        if nueva_pelicula.horaActualizacion
                        else None
                    ),
                }
                return jsonify(pelicula_data), HTTPStatus.CREATED
            except KeyError as e:
                return (
                    jsonify({"message": f"Falta el campo requerido: {e}"}),
                    HTTPStatus.BAD_REQUEST,
                )
    except Exception as e:
        db.rollback()
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        db.close()


##funcion para actualizar pelicula por id
def actualizar_pelicula(pelicula_id):

    db = SessionLocal()
    try:
        pelicula = db.query(Pelicula).filter(pelicula_id == pelicula_id).first()
        if not pelicula:
            return jsonify({"message": "Pelicula no existe"}), HTTPStatus.NOT_FOUND

        data = request.get_json()
        if not data:
            return HTTPStatus.BAD_REQUEST

        ##ACTUALIZA LOS CAMPOS QUE FUERON PROPORCIONADOS UNICAMENTE
        if "titulo" in data:
            pelicula.titulo = data["titulo"]
        if "duracion" in data:
            pelicula.duracion = data["duracion"]
        if "fechaEstreno" in data:

            fecha_estreno_str = data.get("fechaEstreno")
            if fecha_estreno_str:
                try:
                    fecha_estreno = datetime.fromisoformat(fecha_estreno_str)
                except ValueError:
                    try:
                        fecha_estreno = datetime.strftime(fecha_estreno_str, "%Y-%m-%d")
                    except ValueError:
                        return (
                            jsonify({"message": "Formato de fecha incorrecto"}),
                            HTTPStatus.BAD_REQUEST,
                        )

                    Pelicula.fechaEstreno = fecha_estreno

        db.commit()
        db.refresh(pelicula)

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
        db.rollback()
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        db.close()


# funcion para eliminar pelicula por id
def Eliminar_pelicula(pelicula_id):
    db = SessionLocal()
    try:
        pelicula = db.query(Pelicula).filter(Pelicula.id == pelicula_id).first()
        if not pelicula:
            return jsonify({"message": "Película no encontrada"}), HTTPStatus.NOT_FOUND

        db.delete(pelicula)
        db.commit()
        return (
            jsonify({"message": "Película eliminada exitosamente"}),
            HTTPStatus.NO_CONTENT,
        )
    except Exception as e:
        db.rollback()
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        db.close()
