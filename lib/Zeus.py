import hashlib
import locale
import os
import re
import secrets
import string

from app_config import DATABASES
from decouple import config as config_environment

class Zeus():

    MEDIA_TYPE_STATIC_FORMAT = [
        "gif"
        , "jpg"
        , "jpeg"
        , "png"
        , "mp4"
    ]


    @classmethod
    def validate_email_format(self, email):
        # Expresión regular para validar un formato básico de correo electrónico
        email_regex = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'

        # Verificar si el correo electrónico coincide con la expresión regular
        return bool(re.match(email_regex, email))


    @classmethod
    def make_password(self, password):
        
        # Generar una sal aleatoria
        characters = string.ascii_letters + string.digits + string.punctuation
        salt = ''.join(secrets.choice(characters) for i in range(12))  # Sal de 12 caracteres

        # Combinar la contraseña y la sal
        password_with_salt = password + salt

        # Aplicar el algoritmo de hash (en este caso, SHA-256)
        hashed_password = hashlib.sha256(password_with_salt.encode()).hexdigest()

        # Retornar la contraseña encriptada junto con la sal
        return f"{hashed_password}${salt}"


    def get_content_type(file_name):
        """
        Obtiene el tipo de contenido (Content-Type) basado en la extensión del archivo.

        Parameters:
        - file_name: El nombre del archivo.

        Returns:
        - El tipo de contenido correspondiente a la extensión del archivo.
        """
        
        _, file_extension = os.path.splitext(file_name.lower())
        content_type_mapping = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.mp4': 'video/mp4'
        }
        return content_type_mapping.get(file_extension, 'application/octet-stream')


    @classmethod
    def validate_json_keys(self, json_data, array_no_required=[]):
        """
        Valida un JSON asegurándose de que todos los campos tengan un valor.

        Parameters:
        - json_data: El JSON a validar.
        - array_no_required: Arreglo de key que no son requeridos.

        Raises:
        - ValueError: Si se encuentra algún campo sin valor.

        Returns:
        - Tuple: Una tupla que contiene el mensaje de error y un indicador de éxito.
        """
        for key, value in json_data.items():
            if key not in array_no_required:
                if value is None or (isinstance(value, str) and value.strip() == ''):
                    return f'El campo "{key}" no tiene un valor válido.', True
        return None, False
    

    @classmethod
    def format_to_set_locale_peso(number, set_locale='es_CL.UTF-8'):
        """
        Format a number as Chilean peso.

        - es_CL.UTF-8'

        Args:
            number (float): The number to be formatted.
            set_locale (str, optional): The locale to be used for formatting. Defaults to 'es_CL.UTF-8'.

        Returns:
            str: The formatted number as Chilean peso.

        """
        # Set the locale for Chile
        locale.setlocale(locale.LC_ALL, set_locale)

        # Format the number as Chilean peso
        formatted_number = locale.currency(number, grouping=True)

        return formatted_number
    


    @classmethod
    def validate_rut(self, rut):
            """
            Validates a Chilean RUT (Rol Único Tributario) number.

            Args:
                rut (str): The RUT number to be validated.

            Returns:
                bool: True if the RUT is valid, False otherwise.
            """
            rut = rut.replace(".", "").replace("-", "")
            if not re.match(r'^\d{1,8}[0-9K]$', rut):
                return False
            rut_not_dv = rut[:-1]
            dv = rut[-1].upper()
            multiplier = 2
            _sum = 0
            for r in reversed(rut_not_dv):
                _sum += int(r) * multiplier
                multiplier += 1
                if multiplier == 8:
                    multiplier = 2
            _rest = _sum % 11
            dv_calculated = 11 - _rest
            if dv_calculated == 11:
                dv_calculated = '0'
            elif dv_calculated == 10:
                dv_calculated = 'K'
            else:
                dv_calculated = str(dv_calculated)
            return dv == dv_calculated


    @classmethod
    def validate_mail(self, email):
            """
            Valida si una dirección de correo electrónico es válida.

            Args:
                correo (str): La dirección de correo electrónico a validar.

            Returns:
                bool: True si la dirección de correo electrónico es válida, False en caso contrario.
            """
            compiled_model = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

            compiled_model = re.compile(compiled_model)

            if compiled_model.match(email):
                return True
            else:
                return False
