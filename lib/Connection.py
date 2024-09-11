from app_config import DATABASES

from sqlalchemy import create_engine, pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

class Connection():

    Base = declarative_base()

    @classmethod
    def get_session(self, connection_name):
        """
        Returns a session object for the specified database connection.

        Args:
            connection_name (str): The name of the database connection.

        Returns:
            Session: A session object for the specified database connection.
        """

        # Recuperar la conexión según el nombre dado
        data = DATABASES[connection_name]

        DB_HOST = data['DB_HOST']
        DB_USER = data['DB_USER']
        DB_PASSWORD = data['DB_PASSWORD']
        DB_PORT = data['DB_PORT']
        DB_NAME = data['DB_NAME']
        DB_TYPE = data['DB_TYPE']

        encoded_password = quote_plus(DB_PASSWORD)
        connection_string = f"{DB_TYPE}://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(connection_string, pool_pre_ping=True, poolclass=pool.NullPool)
        Session = sessionmaker(bind=engine)
        
        # Retorna la sesión
        return Session()