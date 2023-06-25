from config.database import Base
#importamos los tipos de datos que vamos a usar
from sqlalchemy import Column, Integer, String, Float

#creamos modelo de clase de pelicula
class Movie(Base):#entidad base de datos
    #creamos tabla de base de datos
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30), nullable=False)
    overview = Column(String(300), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    category = Column(String(30), nullable=False)
