from flask import Flask, jsonify, request
from flask_cors import CORS
from .database.database import engine, Base
from .Models import Pelicula, Usuario
from .extensions import bcrypt, jwt


try:
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas exitosamente (o ya existían)!")
except Exception as e:
    print(f"Error al crear las tablas: {e}")

app = Flask(__name__)
CORS(app)

##autenticacion
app.config["SECRET_KEY"] = "La_Union_Secreta_Flask"
app.config["JWT_SECRET_KEY"] = "La_Union_App_JWT_Secreta"
app.config["JWT_TOKEN_LOCATION"] = ["headers"]

bcrypt.init_app(app)  # Inicializa Bcrypt con la instancia de tu app
jwt.init_app(app)  # Inicializa JWTManager con la instancia de tu app

# Las importaciones de Blueprints deben ir DESPUÉS de la inicialización de 'app' y sus extensiones
from .routes.peliculas_routes import peliculas_bp
from .routes.usuarios_routes import usuarios_bp

app.register_blueprint(peliculas_bp, url_prefix="/ilu")
app.register_blueprint(usuarios_bp, url_prefix="/ilu")

if __name__ == "__main__":
    print("Iniciando el servidor Flask en http://127.0.0.1:3000")
    app.run(host="127.0.0.1", port=3000, debug=True)
