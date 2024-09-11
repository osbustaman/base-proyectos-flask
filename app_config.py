from decouple import config

class Config():
    SECRET_KEY = config('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

configure = {
    'development': DevelopmentConfig
}


# Se debe crear las variables de entorno en el archivo .env
# 
# ENVIRONMENTS = nombre de la conexion de base de base de datos para el sistema
# DB_HOST = host/ip de la base de datos
# DB_USER = usuario de la base de datos
# DB_PASSWORD = contraseña de la base de datos
# DB_PORT = puerto de la base de datos
# DB_NAME = nombre de la base de datos
# DB_TYPE = tipo de base de datos (mysql, postgresql)

# Se pueden agregar mas variables de entorno para configurar la base de datos

DATABASES = {
    # config('ENVIRONMENTS'): {
    #     'DB_HOST': config('DB_HOST'),
    #     'DB_USER': config('DB_USER'),
    #     'DB_PASSWORD': config('DB_PASSWORD'),
    #     'DB_PORT': config('DB_PORT'),
    #     'DB_NAME': config('DB_NAME'),
    #     'DB_TYPE': config('DB_TYPE'),
    # }
}