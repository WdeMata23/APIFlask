from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

Base = declarative_base()


# Define el modelo de la tabla 'pelicula'
class Pelicula(Base):

    __tablename__ = "pelicula"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    duracion = Column(Integer, nullable=False)
    FechaEstreno = Column(DateTime, nullable=False)
    HoraCreacion = Column(DateTime, default=datetime.now)
    HoraActualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
