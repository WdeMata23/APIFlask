from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from ..database.database import Base


class Usuario(Base):
    __tablename__ = "Usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    edad = Column(Integer, nullable=False)
    Usuario = Column(String(150), nullable=False)
    Contraseña = Column(String(250), nullable=False)
    Rol = Column(String(255), nullable=False)
    Correo = Column(String(255), nullable=False)
    HoraCreacion = Column(DateTime, default=datetime.now)
    HoraActualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
