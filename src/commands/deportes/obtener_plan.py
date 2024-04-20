import logging

from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.plan_ejercicio import PlanEjercicio, PlanEjercicioJsonSchema
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
        else:
            logger.info("Plan ejercicios encontrado")
            schema = PlanEjercicioJsonSchema(many=True)
            return schema.dump(plan_ejercicios)
