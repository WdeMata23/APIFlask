from flask import jsonify, request
from http import HTTPStatus
from ..database.database import SessionLocal
from ..Models.Pelicula import Pelicula
from datetime import datetime
