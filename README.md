# FASTAPI - Twitter API

## Table of Contents:
- [Descripción](#description)
- [Requirementos](#requirements)
- [Instalacion](#installation)
- [Uso](#run-it-locally)


## Descripción
Este es un proyecto sencillo y basico de la funcionalidad de FastApi.
Incluye:
- Data modeling with pydantic.
- Data validation.
- CRUD of users.
- CRUD of Tweets.
- Data persistance with JSON files (JSON files as database)


## Requirementos:
- Python >= 3.6

## Instalacion

1. Open the console inside the project directory and create a virtual environment.
    ```bash
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ deactivate
    ```

2. Install the app
    ```bash
    (venv) $ pip install -r requirements.txt
    ```

## Run it locally
```
(venv) $ uvicorn main:app --reload
```

## Uso
Once you are running the server open the [Swagger UI App](http://localhost:8000/docs) to checkout the API documentation.
