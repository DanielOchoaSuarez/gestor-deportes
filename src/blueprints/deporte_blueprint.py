import os
import logging
from flask import Blueprint, jsonify, make_response, request
from src.commands.deportes.obtener_deporte import ObtenerDeporte
from src.commands.deportes.obtener_deportes import ObtenerDeportes
from src.commands.deportes.obtener_plan import ObtenerPlan


logger = logging.getLogger(__name__)
deporte_blueprint = Blueprint('deporte', __name__)


@deporte_blueprint.route('/obtener_deportes', methods=['GET'])
@deporte_blueprint.route('/obtener_deportes/<id_deporte>', methods=['GET'])
def obtener_deportes(id_deporte=None):
    if id_deporte is None:
        result = ObtenerDeportes().execute()
    else:
        result = ObtenerDeporte(id_deporte).execute()
    return make_response(jsonify(result), 200)


@deporte_blueprint.route('/obtener_plan', methods=['POST'])
def obtener_plan():
    body = request.get_json()
    info = {
        'id_plan': body.get('id_plan', None),
    }
    result = ObtenerPlan(**info).execute()
    return make_response(jsonify({'result': result}), 200)
