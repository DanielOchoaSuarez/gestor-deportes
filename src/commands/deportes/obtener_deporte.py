import logging

from src.commands.base_command import BaseCommand
from src.models.db import db_session
from src.models.deporte import Deporte, DeporteSchema


logger = logging.getLogger(__name__)


class ObtenerDeporte(BaseCommand):
    def __init__(self, id_deporte: str):
        self.id_deporte = id_deporte

    def execute(self):
        logger.info("Obteniendo deporte con id " + self.id_deporte)

        with db_session() as session:
            deporte = session.query(Deporte).filter_by(
                id=self.id_deporte).first()

            if deporte is None:
                return None

            else:
                schema = DeporteSchema()
                return schema.dump(deporte)
