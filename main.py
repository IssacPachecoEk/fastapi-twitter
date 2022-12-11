from typing import Optional
# pydantic
from pydantic import BaseModel, Field
# fastapi
from fastapi import *
# from fastapi import Body

app = FastAPI()

# model


class Location(BaseModel):
    cuidad: str
    estado: str
    pais: str


class PersonBase(BaseModel):
    nombre: str = Field(
        None,
        min_length=1,
        max_length=10,
        example="Issac")
    apellidos: str = Field(
        ...,
        min_length=1,
        max_length=10,
        example="Pacheco")
    edad: int = Field(
        ...,
        gt=0,
        le=115,
        example=22
    )

# clase que extiende de PersonBase
class PersonPassWord(PersonBase):
    passsword: str = Field(
        None,
        min_length=1,
        max_length=16,
        example="admin123")

class LoginOut(BaseModel):
    usarname: str = Field(...,
    max_length=20, example="lol")
    message: str = Field(default="Login Succesfuly!")

@app.get(
    path="/",
    status_code=status.HTTP_200_OK)
def home():
    return {"Hello": "world"}

# body
@app.post(path="/persona", 
response_model=PersonBase,
status_code=status.HTTP_201_CREATED,
tags=["Personas"],
summary="Crear una persona")
def create_persona(person: PersonPassWord):
    """
    Crear persona

    Este endpoint crear una persona en la base de datos

    Parametros:
    - Request body parameter:
        - **person: PersonBase** -> Un modelo persona con nombre, apellidos y edad.

    Retorna un modelo persona con nombre, apellidos y edad.
    """
    return person


@app.get(path="/persona/detalle",
status_code=status.HTTP_200_OK,
tags=["Personas"],
summary="Mostrar persona",
deprecated=True)
def show_persona(
    nombre: Optional[str] = Query(
        None,
        min_length=1,
        max_length=10,
        title="Nombre de la persona",
        description="Tiene que ser un nombre mayor a 1 y menor a 11 caracteres",
        example="Maria"
    ),
    edad: str = Query(
        ...,
        title="Edad de la persona",
        description="Es obligatorio este campo",
        example=69
    )
):
    """
    Ver persona

    Este endpoint muestra una persona en la base de datos

    Parametros:
    - Request Query parameter:
        - **nombre.
        - **edad.

    Retorna el nombre con la edad
    """
    return {nombre: edad}

personas = [1,2,3]
@app.get(path="/persona/id/{persona_id}",
status_code=status.HTTP_200_OK,
tags=["Personas"],
summary="Obtener una persona")
def get_id(
    persona_id: int = Path(
        ...,
        gt=0,
        title="Id de la persona",
        description="Es obligatorio este campo",
        example=18)
):
    """
    Obtiene una persona

    Este endpoint obtiene una persona en la base de datos mediante la id.

    Parametros:
    - Id

    Retorna una respuesta si existe la persona o no.
    """
    if persona_id not in personas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Esta persona no existe"
        )
    return {persona_id: "existe"}


@app.put(
    path="/persona/put/{persona_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Personas"],
    summary="Actualizar una persona")
def update_persona(
    persona_id: int = Path(
        ...,
        gt=0,
        title="Id de la persona",
        description="Es obligatorio este campo"),
        example=18,
        person: PersonBase = Body(...),
        location: Location = Body(...)
):
    """
    Actualiza persona

    Este endpoint modificar una persona en la base de datos

    Parametros:
    - Id

    Retorna la locacion de la persona.
    """
    results = person.dict()
    results.update(location.dict())
    return results

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
)
def login(usarname: str = Form(...),password: str = Form(...)):
    return LoginOut(usarname=usarname)

@app.post(
    path="/post-image"
)
def post_image(
    image: UploadFile = File(...)  
):  
    return { "filename": image.filename, 
    "format":image.content_type,
    "size": round(len(image.file.read())/1024,ndigits=2)}