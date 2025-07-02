from ..database.database import get_connection
from .entities.Pelicula import Pelicula


class PeliculaModel:

    @classmethod
    def get_pelicula(self):
        try:
            connection = get_connection()
            peliculas = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, titulo, duracion, FechaEstreno FROM peliculas ORDER BY titulo ASC"
                )
                resultset = cursor.fetchall()

                for row in resultset:
                    pelicula_obj = Pelicula(row[0], row[1], row[2], row[3])
                    peliculas.append(pelicula_obj)

            connection.close()
            return peliculas
        except Exception as ex:
            raise Exception(ex)
