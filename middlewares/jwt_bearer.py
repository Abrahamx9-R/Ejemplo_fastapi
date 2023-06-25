from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from jwt_manager import validate_token

#necesitamos crear una clase para poder hacer la validacion de datos
class JWTBearer(HTTPBearer):
    async def __call__(self,request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com" or data['password'] != "1234":
            raise HTTPException(status_code=403, detail="Credenciales invalidas")
