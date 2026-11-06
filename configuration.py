import os
import secrets
import subprocess
import json

def create_env_file():
    """
    Crea un archivo .env y agrega las variables de entorno especificadas.

    El archivo .env se crea en la misma ubicación que este archivo de configuración.
    Las variables de entorno se definen en el diccionario `variables_entorno`.

    """
    if verify_project_created("create_env_file"):
        print("Ya existe el archivo .env")
        return False

    # Ruta del archivo .env
    ruta_archivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

    # Variables de entorno a agregar
    variables_entorno = {
        "SECRET_KEY": generate_secret_key(longitud=50),
        "EXPIRE_DATE": 1,
        "LOG_DIRECTORY": "src/utils/log",
        "ENVIRONMENTS": "development",
        "DB_HOST": "",
        "DB_USER": "",
        "DB_PASSWORD": "",
        "DB_PORT": "",
        "DB_NAME": "",
        "DB_TYPE": "",
        "LARAVEL_API_URL": "http://localhost:8085/api",
        "LARAVEL_AUTH_TIMEOUT": 5
    }

    # Crear el archivo .env y agregar las variables de entorno
    with open(ruta_archivo, "w") as archivo:
        for variable, valor in variables_entorno.items():
            linea = f"{variable}={valor}\n"
            archivo.write(linea)

    # Cargar las variables de entorno del archivo .env
    os.environ["PYTHON_ENV_FILE"] = ruta_archivo
    print("Archivo .env creado con éxito")


def create_virtual_environment():
    """
    Crea un entorno virtual utilizando el comando 'virtualenv' en la raíz del proyecto.
    """

    if verify_project_created("create_virtual_environment"):
        print("Ya existe la carpeta del entorno virtual")
        return False

    # Ruta de la raíz del proyecto
    ruta_proyecto = os.path.join(os.path.dirname(os.path.abspath(__file__)))

    # Comando para crear el entorno virtual
    comando = f"virtualenv env"
    # Ejecutar el comando en la raíz del proyecto
    subprocess.run(comando, shell=True, cwd=ruta_proyecto)
    print("Entorno virtual creado con éxito")


def generate_json_file():
    """
    Genera un archivo .json con un diccionario que contiene la clave "is_create_project" y el valor "true".
    """
    # Ruta del archivo .json
    ruta_archivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configuration.json")
    
    # Diccionario a guardar en el archivo .json
    data = {
        "is_create_project": "true"
    }
    
    # Crear el archivo .json y guardar el diccionario
    with open(ruta_archivo, "w") as archivo:
        json.dump(data, archivo)


def verify_project_created(key_json):
    """
    Verifica si el archivo configuration.json existe y contiene la clave "is_create_project" con el valor "true".

    Retorna True si el archivo existe y contiene la clave y valor especificados, de lo contrario retorna False.
    """
    # Ruta del archivo configuration.json
    ruta_archivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configuration.json")

    # Verificar si el archivo existe
    if os.path.isfile(ruta_archivo):
        # Leer el contenido del archivo
        with open(ruta_archivo, "r") as archivo:
            try:
                data = json.load(archivo)
                # Verificar si la clave "is_create_project" existe y tiene el valor "true"
                if key_json in data and data[key_json] == "true":
                    return True
                else:
                    # Agregar la clave y valor al archivo configuration.json
                    data[key_json] = "true"
                    with open(ruta_archivo, "w") as archivo:
                        json.dump(data, archivo)

            except json.JSONDecodeError:
                pass
    
    else:
        # Crear el archivo configuration.json
        generate_json_file()

    return False

def generate_secret_key(longitud=50):
    return secrets.token_hex(longitud // 2)

def create_requirements_file(file_path='requirements.txt'):
    dependencies = [
        "Flask",
        "python-decouple",
        "flask-swagger-ui",
        "python-dotenv",
        "APScheduler",
        "requests",
        "sqlalchemy",
        "mysql-connector-python",
        "flask-cors",
        "PyJWT",
        "bcrypt",
        "psycopg2-binary",
        "paramiko",
        "# boto3",
        "firebase-admin",
        "pandas",
        "openpyxl"
    ]

    with open(file_path, "w") as file:
        for dependence in dependencies:
            file.write(dependence + "\n")

def install_dependencies2():
    # Activar el entorno virtual
    subprocess.run(["source", "env/bin/activate"], shell=True)
    # Instalar las dependencias
    #subprocess.run(["pip", "install", "-r", "requirements.txt"])

def install_dependencies():
    # Crear un script de shell para activar el entorno virtual e instalar las dependencias
    script = """
    source env/bin/activate
    pip install -r requirements.txt
    """

    with open("install.sh", "w") as file:
        file.write(script)

    # Hacer el script ejecutable
    os.chmod("install.sh", 0o775)

    # Ejecutar el script
    result = subprocess.run(["./install.sh"], capture_output=True, text=True, shell=True)

    if result.returncode != 0:
        print("Error al instalar las dependencias")
        print(result.stderr)
        return False

    return True


def update_configuration_json():
    ruta_archivo = "configuration.json"
    dependencies = [
        "Flask",
        "python-decouple",
        "flask-swagger-ui",
        "python-dotenv",
        "APScheduler",
        "requests",
        "sqlalchemy",
        "mysql-connector-python",
        "flask-cors",
        "PyJWT",
        "bcrypt",
        "psycopg2-binary",
        "paramiko",
        "# boto3",
        "firebase-admin",
        "pandas",
        "openpyxl"
    ]

    if os.path.isfile(ruta_archivo):
        with open(ruta_archivo, "r") as archivo:
            try:
                data = json.load(archivo)
                if "installed_libraries" not in data:
                    data["installed_libraries"] = {}
                for dependency in dependencies:
                    data["installed_libraries"][dependency] = "installed"
                with open(ruta_archivo, "w") as archivo:
                    json.dump(data, archivo, indent=4)
            except json.JSONDecodeError:
                pass
    else:
        generate_json_file()
# Llamar a la función para crear el archivo .env
create_env_file()
create_virtual_environment()
create_requirements_file()
install_dependencies()
update_configuration_json()

path_app = os.path.join(os.path.dirname(os.path.abspath(__file__)))

print(" ================================================ ")
print("\n INTRUCCIONES: \n")
print("Proyecto creado con éxito")
print(f"1 ==> source env/bin/activate (solo en caso que no inicie el entorno virtual)")
print(f"2 ==> python3 index.py")
print("\n Para mas detalles revisar README.md\n")
print("\n ================================================ ")
