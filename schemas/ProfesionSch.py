from pydantic import BaseModel

# schema
class ProfesionBase(BaseModel):
    nombre: str
    descripcion: str



# response
class ProfesionResponse(ProfesionBase):
    id: int

    class Config:
        from_attributes = True