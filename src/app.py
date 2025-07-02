from flask import Flask
from config import config
from routes import Movie

app = Flask(__name__)


def pagina_no_encontrata(error):
    return "<h1> pagina no encontrada </h1>", 404


if __name__ == "__main__":
    app.config.from_object(config["development"])

    # Bluprints/rutas
    app.register_blueprint(Movie.main, url_prefix="/api/movie")

    # error handlers
    app.register_error_handler(404, pagina_no_encontrata)
    app.run()
