from gestorArchivos import GestorArchivos

gestorArchivosObj = GestorArchivos()


# Se definen los años a recorrer
anioInicio = int(input("Ingrese el ano en el cuál quiere iniciar la búsqueda:\n"))
anioFinal = int(input("Ingrese el ano en el cuál desea finalizar la búsqueda:\n"))

rangoAnios = anioInicio - anioFinal

rutaBase = "C:/SNIES_EXTRACTOR/inputs/"
for ano in range(anioInicio, anioFinal+1):
    rutaPorAnio = str(ano) + ".csv"
    gestorArchivosObj.leerArchivo( rutaBase + "admitidos" + rutaPorAnio )
    # Hacer lo mismo con el resto de archivos. Es decir,
    # gestorArchivosObj.leerArchivo( rutaBase + "matriculados" + rutaPorAnio )
    # gestorArchivosObj.leerArchivo( rutaBase + "neos" + rutaPorAnio )
    # etc ...


