from flask import Flask, jsonify, request
from flask_cors import CORS
from .database.database import engine, Base
from .Models import Pelicula, Usuario
from .routes.peliculas_routes import peliculas_bp
from flask_jwt_extended import JWTManager, create_access_token, jwt_required


try:
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas exitosamente (o ya existían)!")
except Exception as e:
    print(f"Error al crear las tablas: {e}")

app = Flask(__name__)

app.register_blueprint(peliculas_bp, url_prefix="/api")

##autenticacion
app.config["SECRET_KEY"] = "La_Union"
app.config["JWT_SECRET_KEY"] = "La_Union_App"
app.config["JWT_TOKEN_LOCATION"] = ["headers"]

# JWT Initialization
jwt = JWTManager(app)


@app.route("/")
def index():
    return jsonify({"Hola": "Mundo con Flask prueba de hola mundo"})


if __name__ == "__main__":
    print("Iniciando el servidor Flask en http://127.0.0.1:3000")
    app.run(host="127.0.0.1", port=3000, debug=True)
