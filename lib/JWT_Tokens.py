import datetime

import bcrypt
import requests
from decouple import config as load_data

class JWT_Tokens:

    @classmethod
    def encrypt(self, pass_user):
        salt_rounds = 10
        # Generar una salt aleatoria y encriptar la contraseña
        salt = bcrypt.gensalt(rounds=salt_rounds)
        hashed_password = bcrypt.hashpw(pass_user.encode('utf-8'), salt)
        return hashed_password
    

    @classmethod
    def validate_bearer_token(cls, authorization_header: str) -> dict:
        """Valida el Bearer token contra la autenticacion central de Laravel."""
        if not authorization_header:
            raise ValueError('Debes enviar el encabezado Authorization.')

        authorization_parts = authorization_header.strip().split()
        if len(authorization_parts) != 2 or authorization_parts[0].lower() != 'bearer':
            raise ValueError('El encabezado Authorization debe usar el formato Bearer <token>.')

        api_url = load_data('LARAVEL_API_URL', default='http://localhost:8085/api').rstrip('/')
        timeout_seconds = load_data('LARAVEL_AUTH_TIMEOUT', default=5, cast=float)

        try:
            response = requests.get(
                f'{api_url}/usuario-actual',
                headers={
                    'Authorization': authorization_header,
                    'Accept': 'application/json',
                },
                timeout=timeout_seconds,
            )
        except requests.RequestException as error:
            raise ConnectionError('No fue posible validar el token con Laravel.') from error

        if response.status_code == 401:
            raise PermissionError('El token es inválido o ha expirado.')

        if not response.ok:
            raise ConnectionError('Laravel no pudo validar el token.')

        try:
            user = response.json()
        except requests.JSONDecodeError as error:
            raise ConnectionError('Laravel entregó una respuesta de autenticación inválida.') from error

        if not isinstance(user, dict) or not user.get('id'):
            raise PermissionError('El token no tiene un usuario asociado.')

        return user

    @classmethod
    def encode_token_jwt(cls, token: str) -> dict:
        """Mantiene compatibilidad con el nombre utilizado por el proyecto."""
        return cls.validate_bearer_token(token)
        

    @classmethod
    def expire_date(days: int):
        now = datetime.datetime.now()
        new_date = now + datetime.timedelta(days)
        return new_date
