import bcrypt
import datetime
import jwt

from jwt import decode

class JWT_Tokens:

    @classmethod
    def encrypt(self, pass_user):
        salt_rounds = 10
        # Generar una salt aleatoria y encriptar la contraseña
        salt = bcrypt.gensalt(rounds=salt_rounds)
        hashed_password = bcrypt.hashpw(pass_user.encode('utf-8'), salt)
        return hashed_password
    

    @classmethod
    def encode_token_jwt(self, token):
        
        try:
            token = token.split(' ')[1]
            # Decodifica el token y obtén el payload
            payload = jwt.decode(token, options={"verify_signature": False})  # El parámetro "verify_signature" se establece en False para omitir la verificación de la firma. Puedes configurarlo según tus necesidades.
            return payload
        except jwt.ExpiredSignatureError:
            return "El token ha expirado."
        except jwt.InvalidTokenError:
            return "Token no válido."
        

    @classmethod
    def expire_date(days: int):
        now = datetime.datetime.now()
        new_date = now + datetime.timedelta(days)
        return new_date