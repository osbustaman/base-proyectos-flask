
from functools import wraps

from flask import g, jsonify, request

from lib.JWT_Tokens import JWT_Tokens


def jwt_required(view_function):
    """Exige un JWT de Laravel en el encabezado Authorization Bearer."""

    @wraps(view_function)
    def decorated_view(*args, **kwargs):
        try:
            g.authenticated_user = JWT_Tokens.validate_bearer_token(
                request.headers.get('Authorization', '')
            )
        except (ValueError, PermissionError) as error:
            return jsonify({
                'success': False,
                'message': str(error),
            }), 401
        except ConnectionError as error:
            return jsonify({
                'success': False,
                'message': str(error),
            }), 503

        return view_function(*args, **kwargs)

    return decorated_view
