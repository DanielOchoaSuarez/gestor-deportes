import os
import logging
from flask import Blueprint, jsonify, make_response, request
from src.commands.deportes.obtener_plan import ObtenerPlan


logger = logging.getLogger(__name__)
deporte_blueprint = Blueprint('deporte', __name__)


@deporte_blueprint.route('/obtener_plan', methods=['POST'])
def obtener_plan():
    body = request.get_json()
    info = {
        'id_plan': body.get('id_plan', None),
    }
    result = ObtenerPlan(**info).execute()
    return make_response(jsonify({'result': result}), 200)
