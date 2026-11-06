from app_config import DATABASES

from sqlalchemy import create_engine, pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

class Connection():

    Base = declarative_base()

    @classmethod
    def get_session(cls, connection_name):
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
        DB_TYPE = data['DB_TYPE'].strip()

        if DB_TYPE.lower() == 'mysql':
            DB_TYPE = 'mysql+mysqlconnector'
        elif not DB_TYPE:
            raise ValueError("DB_TYPE no está configurado en el archivo .env.")

        connection_url = URL.create(
            drivername=DB_TYPE,
            username=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=int(DB_PORT) if DB_PORT else None,
            database=DB_NAME,
        )
        engine = create_engine(connection_url, pool_pre_ping=True, poolclass=pool.NullPool)
        Session = sessionmaker(bind=engine)
        
        # Retorna la sesión
        return Session()