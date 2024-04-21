import logging

from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.plan_ejercicio import PlanEjercicio
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class ObtenerPlan(BaseCommand):
    def __init__(self, **info):
        logger.info(
            'Validando informacion para obtener plan de entrenamiento deportivo')

        if str_none_or_empty(info.get('id_plan')):
            logger.error("ID Plan Obligatorio")
            raise BadRequest

        self.id_plan = info.get('id_plan')

    def execute(self):
        logger.info("Buscando plan de entrenamiento deportivo " + self.id_plan)
        plan_ejercicios = PlanEjercicio.query.filter_by(
            id_plan=self.id_plan).all()

        if plan_ejercicios is None or len(plan_ejercicios) == 0:
            logger.error("Plan de entrenamiento no encontrado")
            return []

        logger.info("Plan ejercicios encontrado")
        resp = []

        pe: PlanEjercicio
        for pe in plan_ejercicios:
            tmp = {
                'deporte_id': pe.ejercicio_deporte.deporte.id,
                'deporte_nombre': pe.ejercicio_deporte.deporte.nombre,
                'ejercicio_id': pe.ejercicio_deporte.id,
                'ejercicio_nombre': pe.ejercicio_deporte.nombre,
                'ejercicio_duracion': pe.ejercicio_deporte.duracion,
                'ejercicio_descripcion': pe.ejercicio_deporte.descripcion,
            }
            resp.append(tmp)

        return resp
