import logging

from src.commands.base_command import BaseCommand
from src.models.db import db_session
from src.models.deporte import Deporte, DeporteSchema


logger = logging.getLogger(__name__)


class ObtenerDeportes(BaseCommand):
    def __init__(self):
        """
        Constructor de la clase ObtenerDeportes
        """
        pass

    def execute(self):
        logger.info("Obteniendo deportes")

        with db_session() as session:
            deportes = session.query(Deporte).all()

            if deportes is None or len(deportes) == 0:
                return None

            else:
                schema = DeporteSchema(many=True)
                return schema.dump(deportes)
