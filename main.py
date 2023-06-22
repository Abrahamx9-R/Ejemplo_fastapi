from fastapi import FastAPI, Body

#creacion de esquenma de datos 
from pydantic import BaseModel
#podemos importar typing para utilizar valores en nuestro esquema que sean opcionales 
from typing import Optional
#un esquema de datos es una clase que hereda de BaseModel y define los atributos que tendra el objeto que se usara en la API
#tambien podemos crear validaciones para ello se importa de nuevo de pydantic Field
from pydantic import Field
#tambien podemos validar los parametros de ruta con Path y Query
from fastapi import Path, Query
#tambien podemos indicar el modelo de respuesta que vamos a tener para ello podemos importar List
from typing import List
#podemos proteger nuestra api generando una llave de acceso para ello creamos una fucion que importaremos
from jwt_manager import create_token
#para poder validar el token podemos hacer uso de httpBearer middleware
from fastapi.security import HTTPBearer
#ademas debemos importar Request y Dependes para poder usar el middleware y HTTPException para poder devolver un error
from fastapi import Request, Depends,HTTPException
#y tambien nuestra funcion de validacion de token
from jwt_manager import validate_token

#existen varios tipos de respuesta que podemos dar con fastapi entre ellas tenemos HTMl, json y plain text para poder usar json y html se importan las siguientes librerias
from fastapi.responses import HTMLResponse, JSONResponse
app = FastAPI()
app.title = "Aplicacion proteco"
app.version = "0.0.1"

#necesitamos crear una clase para poder hacer la validacion de datos
class JWTBearer(HTTPBearer):
    async def __call__(self,request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com" or data['password'] != "1234":
            raise HTTPException(status_code=403, detail="Credenciales invalidas")

#para poder usar la llaver y tener mas protegida nuestra api podemos crear un esquema para usuarios y de esta forma tener mas informacion de quien la esta usando
class User(BaseModel):
    email: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=2, max_length=50)

#creacion de esquema de datos
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="Mi pelicula", min_length=1, max_length=30)
    overview: str 
    year: int = Field( ge=2000, le=2024)
    rating: float = Field(ge=0, le=10)
    category: str = Field( min_length=1, max_length=30)
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Mi resena de la pelicula",
                "year": 2009,
                "rating": 7.8,
                "category": "Categoria de la pelicula"
            }
        }


@app.get("/",tags=["home"])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": 2009,
		"rating": 7.8,
		"category": "Acción"
	},
    {
        "id": 2,
        "title": "Titanic",
        "overview": "Jack (DiCaprio), un joven artista, gana en una partida de cartas un pasaje ...",
        "year": 1997,
        "rating": 7.8,
        "category": "Drama"
    },
    {
        "id": 3,
        "title": "Star Wars: Episodio IX - El ascenso de Skywalker",
        "overview": "La Resistencia sobreviviente se enfrenta a la Primera Orden, y Rey, Finn, ...",
        "year": 2019,
        "rating": 6.7,
        "category": "Acción"
    },
    {
        "id": 4,
        "title": "Avengers: Endgame",
        "overview": "Después de los eventos devastadores de 'Avengers: Infinity War', el universo ...",
        "year": 2019,
        "rating": 8.4,
        "category": "Acción"
    }
]

#podemos crear una ruta para que el usuario pueda logerase y asi poder generar un token para poder acceder a la api

@app.post("/login",tags=["auth"])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "1234":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200,content=token)
    

# tambien podemos devolver codigos de status con el parametro status_code
#para pedir una autentificacion en algun endpoint podemos usar el parametro dependencies
@app.get("/movies",tags=["movies"],response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:    
    return JSONResponse(status_code=200,content = movies)



@app.get("/movies/{movie_id}",tags=["movies"],response_model=Movie)
def get_movie(movie_id: int = Path( gt=0, le=200)) -> Movie:
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return {"error": "Movie not found"}

@app.get("/movies/",tags=["movies"])
def get_movie_by_category(category: str = Query(min_length=1, max_length=30)):
    return [ movie for movie in movies if movie["category"] == category]

@app.post("/movies",tags=["movies"],status_code=201)
def create_movie(id: int=Body(...), title: str=Body(...), overview: str=Body(...), year: int=Body(...), rating: float=Body(...), category: str=Body(...)):
    new_movie = {
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    }
    movies.append(new_movie)
    return new_movie

@app.post("/movies2",tags=["movies"])
def create_movie(movie: Movie):
    movies.append(movie.dict())
    return movies


@app.put("/movies/{movie_id}",tags=["movies"])
def update_movie(movie_id: int, title: str=Body(...), overview: str=Body(...), year: int=Body(...), rating: float=Body(...), category: str=Body(...)):
    for movie in movies:
        if movie["id"] == movie_id:
            movie["title"] = title
            movie["overview"] = overview
            movie["year"] = year
            movie["rating"] = rating
            movie["category"] = category
            return movie
    return JSONResponse(status_code=404,content={"error": "Movie not found"})

@app.put("/movies2/{movie_id}",tags=["movies"])
def update_movie(movie_id: int, movie: Movie):
    for m in movies:
        if m["id"] == movie_id:
            m["title"] = movie.title
            m["overview"] = movie.overview
            m["year"] = movie.year
            m["rating"] = movie.rating
            m["category"] = movie.category
            return m
    return {"error": "Movie not found"}
#tambien podemos implementar el error 404 si no se encuentra algun elemento solicitado
@app.delete("/movies/{movie_id}",tags=["movies"])
def delete_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            movies.remove(movie)
            return {"message": "Movie deleted"}
    return JSONResponse(status_code=404,content={"error": "Movie not found"})







