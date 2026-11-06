import os
import unittest
from unittest.mock import Mock, patch

from flask import Flask, jsonify

from lib.JWT_Tokens import JWT_Tokens
from src.decorators import jwt_required


class JwtRequiredTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.get('/protegida')
        @jwt_required
        def protected_route():
            return jsonify({'success': True})

        self.client = self.app.test_client()

    def test_rejects_request_without_authorization_header(self):
        response = self.client.get('/protegida')

        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.get_json()['success'])

    @patch('src.decorators.JWT_Tokens.validate_bearer_token')
    def test_accepts_valid_bearer_token(self, validate_bearer_token):
        validate_bearer_token.return_value = {'id': 1, 'nombre': 'Usuario'}

        response = self.client.get(
            '/protegida',
            headers={'Authorization': 'Bearer token-valido'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()['success'])
        validate_bearer_token.assert_called_once_with('Bearer token-valido')

    @patch('src.decorators.JWT_Tokens.validate_bearer_token')
    def test_rejects_invalid_or_expired_token(self, validate_bearer_token):
        validate_bearer_token.side_effect = PermissionError('El token es inválido o ha expirado.')

        response = self.client.get(
            '/protegida',
            headers={'Authorization': 'Bearer token-invalido'},
        )

        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.get_json()['success'])

    @patch('src.decorators.JWT_Tokens.validate_bearer_token')
    def test_reports_unavailable_authentication_service(self, validate_bearer_token):
        validate_bearer_token.side_effect = ConnectionError(
            'No fue posible validar el token con Laravel.'
        )

        response = self.client.get(
            '/protegida',
            headers={'Authorization': 'Bearer token-valido'},
        )

        self.assertEqual(response.status_code, 503)
        self.assertFalse(response.get_json()['success'])


class JwtTokensTest(unittest.TestCase):
    @patch('lib.JWT_Tokens.requests.get')
    def test_validates_token_with_laravel_current_user_endpoint(self, get_request):
        laravel_response = Mock()
        laravel_response.status_code = 200
        laravel_response.ok = True
        laravel_response.json.return_value = {'id': 25, 'nombre': 'Usuario'}
        get_request.return_value = laravel_response

        with patch.dict(
            os.environ,
            {
                'LARAVEL_API_URL': 'http://laravel.test/api',
                'LARAVEL_AUTH_TIMEOUT': '3',
            },
        ):
            user = JWT_Tokens.validate_bearer_token('Bearer jwt-firmado')

        self.assertEqual(user['id'], 25)
        get_request.assert_called_once_with(
            'http://laravel.test/api/usuario-actual',
            headers={
                'Authorization': 'Bearer jwt-firmado',
                'Accept': 'application/json',
            },
            timeout=3.0,
        )


if __name__ == '__main__':
    unittest.main()
