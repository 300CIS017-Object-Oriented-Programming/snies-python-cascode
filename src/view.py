from sniesController import SniesController

class Menu:
    def __init__(self):
        controladorSnies = SniesController()

        # FIXME: ESTO DEBE SER UN INPUT EN EL STREAMLIT
        # Se definen los programas académicos a buscar y se agregan al mapa
        lista_cod_snies = [1042, 1043]

        # FIXME: ESTO DEBE SER UN INPUT EN EL STREAMLIT
        # Se definen los años a recorrer
        """ANIO_INICIO = int(input("Ingrese el ano en el cuál quiere iniciar la búsqueda:\n"))
        ANIO_FINAL = int(input("Ingrese el ano en el cuál desea finalizar la búsqueda:\n"))"""
        ANIO_INI = 2021
        ANIO_FIN = 2022

        controladorSnies.procesarDatos(ANIO_INI, ANIO_FIN, lista_cod_snies)

