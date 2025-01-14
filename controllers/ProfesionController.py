from fastapi import APIRouter

from core.utils import crear_controlador_crud
from models.Profesion import Profesion
from schemas.ProfesionSch import ProfesionBase, ProfesionResponse

# declaramos como controller
router = APIRouter()


#creamos los endpoints
crear_controlador_crud("profesion",Profesion,ProfesionBase,ProfesionResponse,router)