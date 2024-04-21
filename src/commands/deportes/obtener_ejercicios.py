import logging

from sqlalchemy import func

from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.deporte import Deporte, DeporteSchema
from src.models.ejercicio_deporte import EjercicioDeporte


logger = logging.getLogger(__name__)


class ObtenerEjercicios(BaseCommand):
    def __init__(self, **info):
        if info['nombre'] is None:
            logger.error("Nombre del ejercicio es obligatorio")
            raise BadRequest

        if len(info['nombre']) < 3:
            logger.error(
                "Nombre del ejercicio debe tener al menos 3 caracteres")
            raise BadRequest

        if info['id_deporte'] is None:
            logger.error("Id del deporte es obligatorio")
            raise BadRequest

        self.nombre = info['nombre']
        self.id_deporte = info['id_deporte']

    def execute(self):
        logger.info("Obteniendo ejercicios que contengan " + self.nombre)

        comodin = f"%{self.nombre}%"
        ejercicios: EjercicioDeporte = EjercicioDeporte.query.filter(
            EjercicioDeporte.id_deporte == self.id_deporte,
            func.upper(EjercicioDeporte.nombre).like(comodin.upper())
        ).all()

        response = []

        for ejercicio in ejercicios:
            logger.info(f"Ejercicio encontrado: {ejercicio.nombre}")
            tmp = {
                'id': ejercicio.id,
                'nombre': ejercicio.nombre,
                'duracion': ejercicio.duracion,
                'descripcion': ejercicio.descripcion
            }
            response.append(tmp)

        return response
