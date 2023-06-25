# los middlewares son funciones que se ejecutan antes o despues de una peticion
# que permiten poder obtener informacion de la peticion y poder modificar la respuesta
# y obtener errores de estas peticiones
# aqui crearemos un middleware para poder obtener los errores de las peticiones
# a la base de datos
#importamos BaseHtttMiddleware para crear el middleware
from starlette.middleware.base import BaseHTTPMiddleware
# importamos FastApi para poder crear el middleware y tipos de datos
from fastapi import FastAPI , Request, Response 
from fastapi.responses import JSONResponse

# creamos una clase que herede de BaseHTTPMiddleware
class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)   
    # sobreescribimos el metodo dispatch
    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            # si no hay errores en la peticion
            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})