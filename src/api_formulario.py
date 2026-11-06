import base64
import json
import random
import tempfile
import traceback
import os
import requests
import hashlib
import hmac

from flask import current_app
from sqlalchemy import text

from lib.Connection import Connection

from datetime import date, datetime, timedelta
from decouple import config as load_data
from flask import request, jsonify, Blueprint
from lib.Email import EmailSender
from lib.ExceptionsHTTP import HTTP404Error
from lib.Stech import Logger
from lib.ExceptionsJson import ExceptionsJson, Responses
from src.decorators import jwt_required

from datetime import datetime

main_listado_productos = Blueprint('listado_productos', __name__)

@main_listado_productos.route('/', methods=['GET'])
@jwt_required
def listado_productos():
    try:
        nombre_conexion = load_data('ENVIRONMENTS')

        with Connection.get_session(nombre_conexion) as sesion:
            consulta = text("""
                SELECT
                    id,
                    sku,
                    nombre,
                    descripcion_web,
                    marca,
                    cantidad,
                    precio_clp,
                    iva,
                    precio_clp_mas_iva
                FROM producto
                WHERE activo = :estado
                ORDER BY nombre ASC
            """)

            resultados = sesion.execute(
                consulta,
                {'estado': 'Y'}
            ).mappings().all()

            productos = [dict(producto) for producto in resultados]

        return jsonify({
            'success': True,
            'total': len(productos),
            'productos': productos
        }), 200

    except Exception:
        current_app.logger.exception('No se pudo consultar el listado de productos')

        return jsonify({
            'success': False,
            'message': 'No se pudo obtener el listado de productos'
        }), 500
