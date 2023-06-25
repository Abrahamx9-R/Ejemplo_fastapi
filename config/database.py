import os

#existe una nueva alternativa para sqlalchemy del mismo creador llamado sqlmodel
#https://sqlmodel.tiangolo.com/

#para usar sqlalchemy importamos sqlalchemy
#para usar un motor de base de datos importamos create_engine
from sqlalchemy import create_engine
#para crear una sesion importamos sessionmaker
from sqlalchemy.orm.session import sessionmaker
#para manipular la base de datos importamos declarative_base
from sqlalchemy.ext.declarative import declarative_base

# para poder definir la ruta de la base de datos
sqlite_file_name = "../database.sqlite"
base_dir = os.path.dirname(os.path.abspath(__file__))

database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

#creamos el motor de base de datos
engine = create_engine(database_url, echo=True)

#creamos la sesion
Session = sessionmaker(bind=engine)

#creamos la base de datos
Base = declarative_base()