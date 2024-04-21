from src.models.ejercicio_deporte import EjercicioDeporte
from .db import Base
from sqlalchemy import UUID, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
from src.models.model import Model


class PlanEjercicio(Model, Base):
    __tablename__ = "plan_ejercicio"
    id_ejercicio_deporte = Column(UUID(as_uuid=True), ForeignKey('ejercicio_deporte.id'), primary_key=True)
    orden = Column(Integer)
    id_plan = Column(UUID(as_uuid=True))
    
    ejercicio_deporte: Mapped['EjercicioDeporte'] = relationship("EjercicioDeporte")

    def __init__(self, id_ejercicio_deporte, orden, id_plan):
        Model.__init__(self)
        self.id_ejercicio_deporte = id_ejercicio_deporte
        self.orden = orden
        self.id_plan = id_plan
