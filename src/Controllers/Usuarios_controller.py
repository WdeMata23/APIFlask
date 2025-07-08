from flask import jsonify, request
from http import HTTPStatus
from ..database.database import SessionLocal
from ..Models.Usuario import Usuario
from datetime import datetime, timedelta
from ..extensions import bcrypt
from flask_jwt_extended import create_access_token


# funcion para listar todos los usuarios
def get_usuarios():
    db = SessionLocal()  # abrir una nueva sesion a BD

    try:
        usuarios = db.query(Usuario).all()
        # convertir los datos de usuario en json
        usuarios_data = [
            {
                "id": user.id,
                "nombre": user.nombre,
                "edad": user.edad,
                "Usuario": user.Usuario,
                "Contraseña": user.Contraseña,
                "Rol": user.Rol,
                "Correo": user.Correo,
                "HoraCreacion": (
                    user.HoraCreacion.isoformat() if user.HoraCreacion else None
                ),
                "HoraActualizacion": (
                    user.HoraActualizacion.isoformat()
                    if user.HoraActualizacion
                    else None
                ),
            }
            for user in usuarios
        ]
        return jsonify(usuarios_data), HTTPStatus.OK
    except Exception as e:
        # manejo de errores en la obtencion de usuarios
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        db.close()  # cierra la session de la BD


# funcion para traer un usuario
def get_usuario(usuario_id):

    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

        if not usuario:
            return jsonify({"message": "Usuario no encontrado"}), HTTPStatus.NOT_FOUND

        # convertir a formato json
        usuario_data = {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "edad": usuario.edad,
            "Usuario": usuario.Usuario,
            "Contraseña": usuario.Contraseña,
            "Rol": usuario.Rol,
            "Correo": usuario.Correo,
            "HoraCreacion": (
                usuario.HoraCreacion.isoformat() if usuario.HoraCreacion else None
            ),
            "HoraActualizacion": (
                usuario.HoraActualizacion.isoformat()
                if usuario.HoraActualizacion
                else None
            ),
        }
        return jsonify(usuario_data), HTTPStatus.OK
    except Exception as e:
        print(f"Error fetching single user: {e}")
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        db.close()  # cierra la session de la BD


# funcion para crear usuario
def registrarse():
    db = SessionLocal()
    try:
        data = request.get_json()
        if not data:
            return (
                jsonify({"message": "No se proporcionaron datos"}),
                HTTPStatus.BAD_REQUEST,
            )

        # Obtener la contraseña para poderlas hashear
        plain_password = data.get("Contraseña")
        if not plain_password:
            return (
                jsonify({"message": "El campo 'Contraseña' es requerido"}),
                HTTPStatus.BAD_REQUEST,
            )

        # Hashear la contraseña
        hashed_password = bcrypt.generate_password_hash(plain_password).decode("utf-8")

        nuevo_usuario = Usuario(
            nombre=data["nombre"],
            edad=data["edad"],
            Usuario=data["Usuario"],
            Contraseña=hashed_password,  # Almacenar el hash
            Rol=data["Rol"],
            Correo=data["Correo"],
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        usuario_response_data = {
            "id": nuevo_usuario.id,
            "nombre": nuevo_usuario.nombre,
            "edad": nuevo_usuario.edad,
            "Usuario": nuevo_usuario.Usuario,
            "Rol": nuevo_usuario.Rol,
            "Correo": nuevo_usuario.Correo,
            "HoraCreacion": (
                nuevo_usuario.HoraCreacion.isoformat()
                if nuevo_usuario.HoraCreacion
                else None
            ),
            "HoraActualizacion": (
                nuevo_usuario.HoraActualizacion.isoformat()
                if nuevo_usuario.HoraActualizacion
                else None
            ),
        }
        return jsonify(usuario_response_data), HTTPStatus.CREATED
    except KeyError as e:
        return (
            jsonify({"message": f"Falta el campo requerido: {e}"}),
            HTTPStatus.BAD_REQUEST,
        )
    except Exception as e:
        db.rollback()
        print(f"Error al crear usuario: {e}")
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        db.close()


def login():
    db = SessionLocal()
    try:
        data = request.get_json()
        username = data.get("Usuario")
        plain_password = data.get("Contraseña")

        if not username or not plain_password:
            return jsonify({"message": "Faltan credenciales"}), HTTPStatus.BAD_REQUEST

        user = db.query(Usuario).filter(Usuario.Usuario == username).first()

        if not user:
            return (
                jsonify({"message": "Credenciales inválidas"}),
                HTTPStatus.UNAUTHORIZED,
            )

        # Comprobar la contraseña usando la instancia de bcrypt
        if not bcrypt.check_password_hash(user.Contraseña, plain_password):
            return (
                jsonify({"message": "Credenciales invalidws"}),
                HTTPStatus.UNAUTHORIZED,
            )

        # Crear el token y asginar el tiempo
        token = create_access_token(
            identity=str(user.id),
            additional_claims={"Usuario": user.Usuario, "Rol": user.Rol},
            expires_delta=timedelta(hours=24),  # tiempo asignado al token 24 horas
        )

        return (
            jsonify(
                message="Inicio de sesión exitoso",
                token=token,
                user_info={
                    "id": user.id,
                    "Usuario": user.Usuario,
                    "Rol": user.Rol,
                    "Correo": user.Correo,
                },
            ),
            HTTPStatus.OK,
        )

    except Exception as e:
        print(f"Error durante el inicio de sesión: {e}")
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        db.close()


def eliminar_usuario(usuario_id):
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(usuario_id == usuario_id).first()
        if not usuario:
            return jsonify({"message": "usuario no encontrado"}), HTTPStatus.NOT_FOUND

        db.delete(usuario)
        db.commit()
        return (
            jsonify({"message": "Usuario eliminado con exitosamente"}),
            HTTPStatus.NO_CONTENT,
        )
    except Exception as e:
        db.rollback()
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        db.close()


def actualizar_usuario(usuario_id):
    db = SessionLocal()

    try:
        usuario = db.query(Usuario).filter(usuario_id == usuario_id).first()
        if not usuario:
            return jsonify({"message": "usuario no encontrado"}), HTTPStatus.NOT_FOUND

        data = request.get_json()
        if not data:
            return HTTPStatus.BAD_REQUEST

        # actualiza unicamente los parametros que fueron proporcionados.
        if "nombre" in data:
            usuario.nombre = data["nombre"]
        if "edad" in data:
            usuario.edad = data["edad"]
        if "Usuario" in data:
            usuario.Usuario = data["Usuario"]
        if "Contraseña" in data:
            usuario.Contraseña = data["Contraseña"]
        if "Rol" in data:
            usuario.Rol = data["Rol"]
        if "Correo" in data:
            usuario.Correo = data["Correo"]

        db.commit()
        db.refresh(usuario)

        usuario_data = {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "edad": usuario.edad,
            "Usuario": usuario.Usuario,
            "Contraseña": usuario.Contraseña,
            "Rol": usuario.Rol,
            "Correo": usuario.Correo,
            "horaActualizacion": (
                usuario.HoraActualizacion.isoformat()
                if usuario.HoraActualizacion
                else None
            ),
        }
        return jsonify(usuario_data), HTTPStatus.OK
    except Exception as e:
        db.rollback()
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        db.close()
