from flask import Flask, jsonify
from flask_cors import CORS
from database import engine, Base
from .Models.Pelicula import Pelicula
from .routes.peliculas_routes import peliculas_bp


print("Intentando crear las tablas en la base de datos...")
try:
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas exitosamente (o ya existían)!")
except Exception as e:
    print(f"Error al crear las tablas: {e}")

app = Flask(__name__)


CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(peliculas_bp, url_prefix="/api")


@app.route("/")
def index():
    return jsonify({"Hola": "Mundo con Flask"})


if __name__ == "__main__":
    print("Iniciando el servidor Flask en http://127.0.0.1:3000")
    app.run(host="127.0.0.1", port=3000, debug=True)
