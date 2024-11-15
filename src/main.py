from gestorArchivos import GestorArchivos
from src.programaAcademico import ProgramaAcademico


gestor_archivos_obj = GestorArchivos()

# Se crea el mapa de programas académicos
dict_programas_academicos = {}
# Se definen los programas académicos a buscar y se agregan al mapa
lista_cod_snies = [1042, 1043]

for cod_snies in lista_cod_snies:
    programa_academico_df = ProgramaAcademico()
    dict_programas_academicos[cod_snies] = programa_academico_df

# TODO: AGREGAR LOS CONSOLIDADOS. EN ESTE MOMENTO SE ESTÁ GUARDANDO EN EL OBJETO UN DATAFRAME. NO SE LE ESTÁ ASIGNANDO A UNA VARIABLE

# Se definen los años a recorrer
ANIO_INICIO = int(input("Ingrese el ano en el cuál quiere iniciar la búsqueda:\n"))
ANIO_FINAL = int(input("Ingrese el ano en el cuál desea finalizar la búsqueda:\n"))

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