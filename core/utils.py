from fastapi import FastAPI, Depends, HTTPException
from typing import Type, TypeVar, List
from db.db import get_db
from sqlalchemy.orm import Session

from fastapi import APIRouter

# METODOS CRUD REFACTORIZADOS PARA SU USO
# DESDE CUALQUIER COMPONENTE

ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType')
ResponseSchemaType = TypeVar('ResponseSchemaType')

def crear_controlador_crud(
        prefijo: str,
        model: Type[ModelType],
        create_schema: Type[CreateSchemaType],
        response_schema: Type[ResponseSchemaType],
        router: APIRouter,
):
    @router.get(f"/{prefijo}",response_model=List[response_schema])
    def obtener_lista(db: Session = Depends(get_db)):
        return db.query(model).all()

    @router.post(f"/{prefijo}", response_model=response_schema)
    def create_item(item: create_schema, db: Session = Depends(get_db)):
        nuevo_item = model(**item.dict())
        db.add(nuevo_item)
        try:
            db.commit()
            db.refresh(nuevo_item)
        except:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"El {prefijo} ya existe.")

        return nuevo_item

    @router.delete(f"/{prefijo}/{{id}}", response_model=str)
    def eliminar_item(id: int, db: Session = Depends(get_db)):
        item = db.query(model).filter(model.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item eliminada.")
        db.delete(item)
        db.commit()
        return f"item eliminado"

    @router.put(f"/{prefijo}/{{id}}", response_model=response_schema)
    def actualizar_item(id: int, item: create_schema, db: Session = Depends(get_db)):
        item_existente = db.query(model).filter(model.id == id).first()
        if not item_existente:
            raise HTTPException(status_code=404, detail=f"{prefijo.capitalize()} no encontrado.")

        for key, value in item.dict(exclude_unset=True).items():
            setattr(item_existente, key, value)

        try:
            db.commit()
            db.refresh(item_existente)
        except:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"No se pudo actualizar el {prefijo}.")

        return item_existente

    @router.get(f"/{prefijo}/{{id}}", response_model=response_schema)
    def buscar_por_id(id: int, db: Session = Depends(get_db)):
        item = db.query(model).filter(model.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"{prefijo.capitalize()} no encontrado.")
        return item