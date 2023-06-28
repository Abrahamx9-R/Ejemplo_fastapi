#creamos esquemas para tener toda la informacion de cada uno de los modelos
# por separado y bien definida para poder usarla en los servicios y en los routers


from pydantic import BaseModel

class User(BaseModel):
    email:str
    password:str