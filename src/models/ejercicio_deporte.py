from marshmallow import Schema, fields
from src.models.deporte import Deporte, DeporteSchema
from .db import Base
from sqlalchemy import UUID, Column, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, relationship
from src.models.model import Model


class EjercicioDeporte(Model, Base):
    __tablename__ = "ejercicio_deporte"
    id_deporte = Column(UUID(as_uuid=True), ForeignKey(
        'deporte.id'), primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    duracion = Column(Integer)
    descripcion = Column(String(250))

    deporte: Mapped['Deporte'] = relationship("Deporte")

    def __init__(self, id_deporte, nombre, duracion, descripcion):
        Model.__init__(self)
        self.id_deporte = id_deporte
        self.nombre = nombre
        self.duracion = duracion
        self.descripcion = descripcion
