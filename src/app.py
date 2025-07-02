from flask import Flask
from config import config
from routes.Pelicula import main as PeliculaBlueprint

app = Flask(__name__)


def pagina_no_encontrata(error):
    return "<h1> pagina no encontrada </h1>", 404


if __name__ == "__main__":
    app.config.from_object(config["development"])

    # Blueprints/rutas
    app.register_blueprint(PeliculaBlueprint, url_prefix="/api/pelicula")

    # error handlers
    app.register_error_handler(404, pagina_no_encontrata)
    app.run()
