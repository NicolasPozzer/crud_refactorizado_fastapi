from fastapi import FastAPI
from controllers import ProfesionController
from db.db import Base, engine

app = FastAPI()


# declarar credor de tablas
Base.metadata.create_all(bind=engine)


# declarar controllers
app.include_router(ProfesionController.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
