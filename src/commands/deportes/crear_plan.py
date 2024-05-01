import logging

from sqlalchemy import func

from src.commands.base_command import BaseCommand
from src.errors.errors import ApiError, BadRequest, SportNotFound
from src.models.db import db_session
from src.models.deporte import Deporte
from src.models.ejercicio_deporte import EjercicioDeporte
from src.models.plan_ejercicio import PlanEjercicio
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class CrearPlan(BaseCommand):
    def __init__(self, **info):

        if str_none_or_empty(info['nombre']):
            logger.error("Nombre del plan Obligatorio")
            raise BadRequest

        if str_none_or_empty(info['id_plan']):
            logger.error("Id del plan Obligatorio")
            raise BadRequest

        if str_none_or_empty(info['id_deporte']):
            logger.error("Deporte Obligatorio")
            raise BadRequest

        deporte: Deporte = Deporte.query.filter_by(
            id=info['id_deporte']).first()
        if not deporte:
            logger.error("Deporte no encontrado")
            raise SportNotFound

        ejercicios = self._validar_ejercicios(
            id_deporte=info['id_deporte'], ejercicios=info['ejercicios'])

        self.nombre = info['nombre']
        self.id_plan = info['id_plan']
        self.deporte = deporte
        self.ejercicios = ejercicios

    def _validar_ejercicios(self, id_deporte, ejercicios):
        if len(ejercicios) == 0:
            logger.error("Ejercicios Obligatorios")
            raise BadRequest

        resp = []

        for ejercicio in ejercicios:

            if 'id' in ejercicio:
                ejercicio_registrado = {
                    'id': ejercicio['id'],
                }
                resp.append(ejercicio_registrado)
                continue

            if 'duracion' not in ejercicio or ejercicio['duracion'] <= 0:
                logger.error("Duracion del ejercicio obligatorio")
                raise BadRequest

            if 'descripcion' not in ejercicio:
                logger.error("Descripcion del ejercicio obligatorio")
                raise BadRequest

            if 'nombre' not in ejercicio:
                logger.error("Nombre del ejercicio obligatorio")
                raise BadRequest

            ejercicio_deporte: EjercicioDeporte = EjercicioDeporte.query.filter(
                EjercicioDeporte.id_deporte == id_deporte,
                func.upper(EjercicioDeporte.nombre).like(ejercicio['nombre'].upper())).first()

            if ejercicio_deporte:
                logger.error("Ejercicio ya registrado")
                raise BadRequest

            nuevo_ejercicio = {
                'nombre': ejercicio['nombre'],
                'duracion': ejercicio['duracion'],
                'descripcion': ejercicio['descripcion'],
                'id_deporte': id_deporte,
            }

            resp.append(nuevo_ejercicio)

        return resp

    def execute(self):
        logger.info(f'Creando plan deportivo {self.nombre}')

        resp = []

        for index, ejercicio in enumerate(self.ejercicios):

            try:
                tmp: EjercicioDeporte

                if 'id' in ejercicio:
                    tmp = EjercicioDeporte.query.filter_by(
                        id=ejercicio['id']).first()

                else:
                    tmp = EjercicioDeporte(**ejercicio)
                    db_session.add(tmp)
                    db_session.commit()

                plan_ejercicio = {
                    'id_ejercicio_deporte': tmp.id,
                    'orden': index,
                    'id_plan': self.id_plan,
                }

                plan_ejercicio = PlanEjercicio(**plan_ejercicio)
                db_session.add(plan_ejercicio)
                db_session.commit()
                resp.append(plan_ejercicio.id)
            except Exception as e:
                logger.error(f"Error al crear plan ejercicios {e}", e)
                db_session.rollback()
                raise ApiError

        return resp
