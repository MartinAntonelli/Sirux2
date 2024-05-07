from Actualizacion import obtener_version_actual
from Actualizacion import obtener_version_repositorio
from Actualizacion import actualizar_app
from Sirux2_0 import general


def main():
    print('Iniciando la aplicación...')

    version_actual = obtener_version_actual()
    version_repositorio = obtener_version_repositorio()
    print(version_actual, version_repositorio)

    if version_actual < version_repositorio:
        print('Hay una nueva versión disponible. Actualizando...')
        actualizar_app()
        print('La aplicación se ha actualizado a la versión', version_repositorio)
        general()
    else:
        general()

if __name__ == '__main__':
    main()