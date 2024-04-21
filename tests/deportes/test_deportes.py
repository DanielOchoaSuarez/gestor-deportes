import json
import pytest
import logging
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.deporte import Deporte


fake = Faker()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def setup_data():
    logger.info("Inicio TestDeportes")

    deporte = {
        'nombre': fake.name(),
    }
    deporte_random = Deporte(**deporte)

    db_session.add(deporte_random)
    db_session.commit()
    logger.info('Deporte creado: ' + deporte_random.nombre)
    yield deporte_random
    logger.info("Fin TestDeportes")
    db_session.delete(deporte_random)
    db_session.commit()


@pytest.mark.usefixtures("setup_data")
class TestDeportes():

    def test_obtener_deportes(self):
        with app.test_client() as test_client:
            response = test_client.get(
                '/gestor-deportes/deportes/obtener_deportes')
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert len(response_json) >= 1

    def test_obtener_deporte(self, setup_data: Deporte):
        with app.test_client() as test_client:
            id_deporte = str(setup_data.id)
            response = test_client.get(
                '/gestor-deportes/deportes/obtener_deportes/' + id_deporte)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert response_json != None
            assert response_json['id'] == id_deporte
