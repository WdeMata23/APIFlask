from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

MOTOR = "mariadb"
parametros = {
    "db": "dbFastAPIDev",
    "user": "usrDev",
    "host": "mcu.calhasdfv17y.us-east-1.rds.amazonaws.com",
}

DB_URL = f"mariadb+pymysql://{parametros['user']}:pa$$word.-@{parametros['host']}/{parametros['db']}"

engine = create_engine(DB_URL, echo=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
