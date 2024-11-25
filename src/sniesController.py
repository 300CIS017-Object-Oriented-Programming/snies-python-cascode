from gestorArchivos import GestorArchivos
from programaAcademico import ProgramaAcademico

class SniesController:
    def __init__(self):

        pass


    def procesarDatos(self, ANIO_INICIO, ANIO_FINAL, LISTA_COD_SNIES):
        gestor_archivos_obj = GestorArchivos()

        # Se crea el mapa de programas académicos
        dict_programas_academicos = {}

        for cod_snies in LISTA_COD_SNIES:
            programa_academico_df = ProgramaAcademico()
            dict_programas_academicos[cod_snies] = programa_academico_df

        RUTA_BASE = "C:/SNIES_EXTRACTOR/inputs/new/"

        print("Se procederá a buscar en el rango de anos: ", ANIO_INICIO, "-" , ANIO_FINAL)


        primera_vez = True

        for ano in range(ANIO_INICIO, ANIO_FINAL+1):
            anioString = str(ano)

            gestor_archivos_obj.leer_archivo(RUTA_BASE, anioString, dict_programas_academicos, "inscritos", primera_vez)
            primeraVez = False

            gestor_archivos_obj.leer_archivo(RUTA_BASE, anioString, dict_programas_academicos, "admitidos", False)
            gestor_archivos_obj.leer_archivo(RUTA_BASE, anioString, dict_programas_academicos, "matriculados", False)
            gestor_archivos_obj.leer_archivo(RUTA_BASE, anioString, dict_programas_academicos, "primerCurso", False)
            gestor_archivos_obj.leer_archivo(RUTA_BASE, anioString, dict_programas_academicos, "graduados", False)

        gestor_archivos_obj.exportar_archivo(dict_programas_academicos)

    def listar_archivos_predeterminados(self):
        # Lista los archivos en la carpeta predeterminada
        RUTA_BASE = "C:/SNIES_EXTRACTOR/inputs/new/"
        archivos = [archivo for archivo in os.listdir(RUTA_BASE) if archivo.endswith(".xlsx")]
        return archivos

    def cargar_archivos_nuevos(self, archivos_subidos):
        # Guarda los archivos subidos en la carpeta predeterminada
        RUTA_BASE = "C:/SNIES_EXTRACTOR/inputs/new/"
        for archivo in archivos_subidos:
            with open(os.path.join(RUTA_BASE, archivo.name), "wb") as f:
                shutil.copyfileobj(archivo, f)
        return [archivo.name for archivo in archivos_subidos]