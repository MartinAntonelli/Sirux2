import os
import git
import shutil
from version import version
import requests

def obtener_version_actual():
    return version


def obtener_version_repositorio():

    url = 'https://raw.githubusercontent.com/MartinAntonelli/Sirux2/main/version.py'
    response = requests.get(url)
    version_line = response.text.split('\n')[0]
    version = version_line
    return version


def actualizar_app():
    repo_url = 'https://github.com/MartinAntonelli/Sirux2'
    repo_local_path = r'C:\Users\Usuario\OneDrive\Escritorio\GPower\Proyecto GPower\Traducciones\Sirux2\Sirux2_0'
    repo_temp_path = r'C:\Users\Usuario\OneDrive\Escritorio\GPower\Proyecto GPower\Traducciones\Sirux2\Sirux2_0\Act'


    version_actual = obtener_version_actual()
    version_repositorio = obtener_version_repositorio()

    if version_actual < version_repositorio:
        # Clona el repositorio en una carpeta temporal
        git.Repo.clone_from(repo_url, repo_temp_path)

        # Elimina la versión antigua de la aplicación
        shutil.rmtree(repo_local_path)

        # Mueve la nueva versión de la aplicación a la carpeta de la aplicación
        shutil.move(repo_temp_path, repo_local_path)

        print("La aplicación se ha actualizado con éxito.")
    else:
        print("La aplicación ya está actualizada.")