from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from ..database.database import Base


class Pelicula(Base):
    __tablename__ = "Pelicula"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    duracion = Column(Integer, nullable=False)
    fechaEstreno = Column(DateTime, nullable=False)
    horaCreacion = Column(DateTime, default=datetime.now)
    horaActualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
