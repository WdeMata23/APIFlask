class Pelicula:

    def __init__(self, id, titulo=None, duracion=None, estreno=None):
        self.id = id
        self.titulo = titulo
        self.duracion = duracion
        self.estreno = estreno

    def to_JSON(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "duracion": self.duracion,
            "estreno": self.estreno,
        }
