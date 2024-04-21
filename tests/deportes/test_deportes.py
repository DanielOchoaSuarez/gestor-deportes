import json
import pytest
import logging
import uuid
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.deporte import Deporte
from src.models.ejercicio_deporte import EjercicioDeporte
from src.models.plan_ejercicio import PlanEjercicio


fake = Faker()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def setup_data():
    logger.info("Inicio TestDeportes")

    # Creción deporte
    deporte = {
        'nombre': fake.name(),
    }
    deporte_random = Deporte(**deporte)

    db_session.add(deporte_random)
    db_session.commit()
    logger.info('Deporte creado: ' + deporte_random.nombre)

    # Creación ejercicio deporte
    ejercicio = {
        'nombre': fake.name(),
        'duracion': 30,
        'descripcion': fake.name(),
        'id_deporte': deporte_random.id,
    }
    ejercicio_deporte_random = EjercicioDeporte(**ejercicio)
    db_session.add(ejercicio_deporte_random)
    db_session.commit()
    logger.info('Ejercicio deporte creado: ' + ejercicio_deporte_random.nombre)

    # Creación plan
    plan = {
        'id_plan': uuid.uuid4(),
        'orden': 0,
        'id_ejercicio_deporte': ejercicio_deporte_random.id,
    }
    plan_random = PlanEjercicio(**plan)
    db_session.add(plan_random)
    db_session.commit()
    logger.info('Plan creado: ' + str(plan_random.id))

    yield {
        'deporte': deporte_random,
        'ejercicio_deporte': ejercicio_deporte_random,
        'plan_ejercicio': plan_random,
    }

    logger.info("Fin TestDeportes")
    db_session.delete(plan_random)
    db_session.delete(ejercicio_deporte_random)
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

    def test_obtener_deporte(self, setup_data: dict):
        with app.test_client() as test_client:
            id_deporte = str(setup_data['deporte'].id)
            response = test_client.get(
                '/gestor-deportes/deportes/obtener_deportes/' + id_deporte)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert response_json != None
            assert response_json['id'] == id_deporte

    def test_obtener_plan(self, setup_data: dict):
        with app.test_client() as test_client:
            plan_ejercicio: PlanEjercicio = setup_data['plan_ejercicio']
            req = {
                'id_plan': str(plan_ejercicio.id_plan),
            }

            response = test_client.post(
                '/gestor-deportes/deportes/obtener_plan', json=req)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert response_json != None
            assert response_json['result'] != None
            assert len(response_json['result']) >= 1

    def test_obtener_ejercicios_exitoso(self, setup_data: dict):
        with app.test_client() as test_client:
            ejercicio_deporte: EjercicioDeporte = setup_data['ejercicio_deporte']
            body = {
                'nombre': ejercicio_deporte.nombre,
                'id_deporte': ejercicio_deporte.deporte.id
            }

            response = test_client.post(
                '/gestor-deportes/deportes/obtener_ejercicios', json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 200

    def test_obtener_ejercicios_sin_nombre(self, setup_data: dict):
        with app.test_client() as test_client:
            ejercicio_deporte: EjercicioDeporte = setup_data['ejercicio_deporte']
            body = {
                'id_deporte': ejercicio_deporte.deporte.id
            }

            response = test_client.post(
                '/gestor-deportes/deportes/obtener_ejercicios', json=body)

            assert response.status_code == 400

    def test_obtener_ejercicios_sin_id_deporte(self, setup_data: dict):
        with app.test_client() as test_client:
            ejercicio_deporte: EjercicioDeporte = setup_data['ejercicio_deporte']
            body = {
                'nombre': ejercicio_deporte.nombre,
            }

            response = test_client.post(
                '/gestor-deportes/deportes/obtener_ejercicios', json=body)

            assert response.status_code == 400

    def test_obtener_ejercicios_error_longitud_nombre(self, setup_data: dict):
        with app.test_client() as test_client:
            ejercicio_deporte: EjercicioDeporte = setup_data['ejercicio_deporte']
            body = {
                'nombre': 'a',
                'id_deporte': ejercicio_deporte.deporte.id
            }

            response = test_client.post(
                '/gestor-deportes/deportes/obtener_ejercicios', json=body)

            assert response.status_code == 400

    def test_crear_plan(self, setup_data: dict):
        with app.test_client() as test_client:
            deporte: Deporte = setup_data['deporte']
            ejercicio_deporte: EjercicioDeporte = setup_data['ejercicio_deporte']

            body = {
                'id_plan': str(uuid.uuid4()),
                'id_deporte': deporte.id,
                'nombre': fake.name(),
                'ejercicios': [
                    {
                        'id': ejercicio_deporte.id,
                    }
                ]
            }

            response = test_client.post(
                '/gestor-deportes/deportes/crear_plan', json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert response_json != None
            assert response_json['result'] != None
            assert len(response_json['result']) >= 1

            for plan_ejercicio in response_json['result']:
                PlanEjercicio.query.filter_by(
                    id=plan_ejercicio).delete()
                db_session.commit()

    def test_crear_plan_sin_id_plan(self, setup_data: dict):
        with app.test_client() as test_client:
            deporte: Deporte = setup_data['deporte']
            ejercicio_deporte: EjercicioDeporte = setup_data['ejercicio_deporte']

            body = {
                'id_deporte': deporte.id,
                'nombre': fake.name(),
                'ejercicios': [
                    {
                        'id': ejercicio_deporte.id,
                    }
                ]
            }

            response = test_client.post(
                '/gestor-deportes/deportes/crear_plan', json=body)

            assert response.status_code == 400

    def test_crear_plan_sin_ejercicios(self, setup_data: dict):
        with app.test_client() as test_client:
            deporte: Deporte = setup_data['deporte']

            body = {
                'id_plan': str(uuid.uuid4()),
                'id_deporte': deporte.id,
                'nombre': fake.name(),
                'ejercicios': []
            }

            response = test_client.post(
                '/gestor-deportes/deportes/crear_plan', json=body)

            assert response.status_code == 400

    def test_crear_plan_ejercicios_sin_nombre(self, setup_data: dict):
        with app.test_client() as test_client:
            deporte: Deporte = setup_data['deporte']
            ejercicio_deporte: EjercicioDeporte = setup_data['ejercicio_deporte']

            body = {
                'id_plan': str(uuid.uuid4()),
                'id_deporte': deporte.id,
                'nombre': fake.name(),
                'ejercicios': [
                    {
                        'duracion': 15,
                        'descripcion': fake.name(),
                    }
                ]
            }

            response = test_client.post(
                '/gestor-deportes/deportes/crear_plan', json=body)

            assert response.status_code == 400
