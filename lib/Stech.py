import os
import re
import traceback
# import boto3
import paramiko

from app_config import DATABASES
from decouple import config as config_environment

from lib.ConnectionGoogle import GoogleSFTPConnection
from lib.Logger import Logger



class Stech():


    @classmethod
    #def object_to_json(self, headers_list, tuplas_list, query_list):
    def object_to_json(self, query_object, type_object="list"):
        """
        Converts a query object to a JSON list.

        Args:
            query_object (list): The query object to be converted.

        Returns:
            list: A list of JSON objects representing the query object.
        """

        if not query_object:
            return []
        
        list_to_json = []
        headers_list = query_object[0]._fields
        tuplas_list = query_object

        for tupla in tuplas_list:
            object_json = {}
            for i in range(len(headers_list)):
                object_json[headers_list[i]] = tupla[i]
            list_to_json.append(object_json)

        return list_to_json
    
    
    @classmethod
    def go_up_to_root_directory(self, image, file_name):
        """
        Guarda una imagen en el directorio raíz del proyecto
        @param current_file_path: Directorio actual
        @param file_name: Nombre del archivo
        @param image: Imagen en base64
        """
        try:
            print(file_name)
            route_static = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src', 'static'))
            if not os.path.exists(route_static):
                os.makedirs(route_static)

            # Guardar la imagen decodificada en el directorio especificado
            with open(os.path.join(route_static, file_name), 'wb') as archivo_salida:
                archivo_salida.write(image)

            return True

        except Exception as ex:
            Logger.add_to_log("error", f"go_up_to_root_directory_base64: {str(ex)}")
            Logger.add_to_log("error", traceback.format_exc())
            
            return False
        
    # @classmethod
    # def go_up_to_root_directory_S3(self, image, name_file, directorio_destino):

    #     try:
    #         content_type = self.get_content_type(name_file)
    #         _name_file = name_file

    #         s3_client = boto3.resource(
    #             's3', 
    #             aws_access_key_id=config_environment('ENV_AWS_ACCESS_KEY_IS'), 
    #             aws_secret_access_key=config_environment('ENV_AWS_SECRET_ACCESS_KEY'), 
    #             region_name=config_environment('ENV_AWS_REGION_NAME')
    #         )

    #         name_file = os.path.join(directorio_destino, name_file)
    #         s3_client.Bucket(config_environment('ENV_AWS_S3_BUCKET_NAME')).put_object(
    #             Key=name_file
    #             , Body=image
    #             , ContentType=content_type
    #             , ContentDisposition=f'inline; filename="{_name_file}"'
    #         )

    #         url_s3 = f"https://s3.amazonaws.com/{config_environment('ENV_AWS_S3_BUCKET_NAME')}/{name_file}"

    #         return url_s3
        
    #     except Exception as ex:
    #         Logger.add_to_log("error", f"go_up_to_root_directory_base64: {str(ex)}")
    #         Logger.add_to_log("error", traceback.format_exc())
            
    #         return False
        

    @classmethod
    def update_image_google_sftp(self, file_name, position_image, extra=None, extra_twoo=None):
        
        
        # Obtén la ruta del archivo .pem

        route_file_key = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src', 'static', config_environment("ENV_GOOGLE_SFTP_ROUTE_PPK_PEM")))
        route_static = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','src', 'static', file_name))

        try:

            if extra_twoo == 'reportesApp':
                google_sftp = config_environment('ENV_GOOGLE_SFTP_REMOTE_PATH') + "/" + extra.upper()
                file_name = file_name.split("/")[len(file_name.split("/")) - 1]
            else:
                google_sftp = config_environment('ENV_GOOGLE_SFTP_REMOTE_PATH_DINAMIC') + extra_twoo + "/" + extra.upper()
                file_name = "img" + str(position_image) + ".jpg"

            if_upload = self.connect_sftp(route_file_key, route_static, google_sftp, file_name)

            if if_upload:
                return True
            else:
                return False

        except Exception as ex:
            print(f"Error en la conexión SFTP: {str(ex)}")
            return False


    @classmethod
    def connect_sftp(self, route_file_key, route_static, google_sftp, file_name):

        ip = config_environment("ENV_GOOGLE_SFTP_IP")
        user = config_environment("ENV_GOOGLE_SFTP_USER")

        try:
            # Crear una instancia de SSHClient
            cliente_ssh = paramiko.SSHClient()

            connection = GoogleSFTPConnection(ip, user, route_file_key)
            connection.connect()
            connection.upload_file(route_static, f"{google_sftp}", file_name)
            connection.disconnect()
                        # Cerrar la conexión SSH
            cliente_ssh.close()
            return True
        except Exception as ex:
            print(f"Error en la conexión SFTP: {str(ex)}")
            return False
        
        finally:
            # Cerrar la conexión SSH
            cliente_ssh.close()



    
