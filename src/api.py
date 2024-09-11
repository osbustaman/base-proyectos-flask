import base64
import json
import random
import tempfile
import traceback
import os
import requests
import hashlib
import hmac

from datetime import date, datetime, timedelta
from decouple import config as load_data
from flask import request, jsonify, Blueprint
from lib.Email import EmailSender
from lib.ExceptionsHTTP import HTTP404Error
from lib.Stech import Logger, Stech, Validate
from lib.ExceptionsJson import ExceptionsJson, Responses

from datetime import datetime

main_ejemplo = Blueprint('main_ejemplo', __name__)

@main_ejemplo.route('/', methods=['GET'])
def ejemplo():
    try:
        return jsonify({'message': 'Hello World', 'success': True}), 200
    
    except Exception as e:
        Logger.error(traceback.format_exc())
        return jsonify({'message': 'Error en el servidor', 'success': False}), 500