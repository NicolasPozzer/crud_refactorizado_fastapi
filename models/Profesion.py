from sqlalchemy import String

from sqlalchemy import Column, Integer

from db.db import Base


class Profesion(Base):
    __tablename__ = 'profesion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=False)
