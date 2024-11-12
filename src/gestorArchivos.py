import pandas as pd
from consolidado import Consolidado

class GestorArchivos:
    def __init__(self):
        pass

    def leer_archivo(self, RUTA_BASE, anio, dict_programas_academicos, atributo_del_archivo, primera_vez):

        ruta_completa = RUTA_BASE + atributo_del_archivo + anio + ".csv"
        print(f"La ruta del archivo es \n{ruta_completa}")
        df = pd.read_csv(ruta_completa, sep=";", encoding='utf-8')

        list_cod_snies = list(dict_programas_academicos.keys())

        for cod_snies in list_cod_snies:
            df_filtrado = df[df["CÓDIGO SNIES DEL PROGRAMA"] == cod_snies]
            index_columna_inicio_exclusion = df.columns.get_loc("ID SEXO")


            if primera_vez:
                dict_programas_academicos[cod_snies].programa_academico = df_filtrado.iloc[:, :index_columna_inicio_exclusion]

            if anio not in dict_programas_academicos[cod_snies].dict_consolidados.keys():
                consolidado_actual_obj = Consolidado()
                consolidado_actual_obj.consolidado = df_filtrado.iloc[:, index_columna_inicio_exclusion:]
                consolidado_actual_obj.consolidado["INSCRITOS"] = None
                consolidado_actual_obj.consolidado["MATRICULADOS"] = None
                consolidado_actual_obj.consolidado["PRIMER CURSO"] = None
                consolidado_actual_obj.consolidado["GRADUADOS"] = None
                dict_programas_academicos[cod_snies].dict_consolidados[anio] = consolidado_actual_obj


        for cod_snies in list_cod_snies:
            df_filtrado = df[df["CÓDIGO SNIES DEL PROGRAMA"] == cod_snies]

            if atributo_del_archivo == "admitidos":
                dict_programas_academicos[cod_snies].dict_consolidados[anio].consolidado.loc[:, "ADMITIDOS"] = df_filtrado.loc[:, "ADMITIDOS"]
                #print(f"Editando el consolidado del año {anio} del programa: {cod_snies}")

            elif atributo_del_archivo == "inscritos":
                dict_programas_academicos[cod_snies].dict_consolidados[anio].consolidado.loc[:, "INSCRITOS"] = df_filtrado.loc[:, "INSCRITOS"]
                print(f"Editando el consolidado del año {anio} del programa: {cod_snies}")

            elif atributo_del_archivo == "matriculados":
                dict_programas_academicos[cod_snies].dict_consolidados[anio].consolidado.loc[:, "MATRICULADOS"] = df_filtrado.loc[:, "MATRICULADOS"]

            elif atributo_del_archivo == "matriculadosPrimerSemestre":
                dict_programas_academicos[cod_snies].dict_consolidados[anio].consolidado.loc[:, "PRIMER CURSO"] = df_filtrado.loc[:, "PRIMER CURSO"]

            elif atributo_del_archivo == "graduados":
                dict_programas_academicos[cod_snies].dict_consolidados[anio].consolidado.loc[:, "GRADUADOS"] = df_filtrado.loc[:, "GRADUADOS"]

        """
        
            elif atributo_del_archivo == "inscritos":
                dict_programas_academicos[cod_snies]["INSCRITOS"] = df_filtrado["INSCRITOS"]
            elif atributo_del_archivo == "matriculados":
                dict_programas_academicos[cod_snies]["MATRICULADOS"] = df_filtrado["MATRICULADOS"]
            elif atributo_del_archivo == "neos":
                dict_programas_academicos[cod_snies]["NEOS"] = df_filtrado["NEOS"]
            elif atributo_del_archivo == "graduados":
                dict_programas_academicos[cod_snies]["GRADUADOS"] = df_filtrado["GRADUADOS"]
            """
        df_filtrado = 0



    def exportar_archivo(self, dict_programas_academicos):

        # FIXME: manejar casos en los que algo esté vacío

        lista_programas_academicos_a_combinar = []

        for cod_prog_actual, programa_academico_obj in dict_programas_academicos.items():

            lista_consolidados_a_combinar = []

            for anio, consolidado_obj in dict_programas_academicos[cod_prog_actual].dict_consolidados.items():
                df_consolidado_actual = consolidado_obj.consolidado
                print(f"El consolidado actual es del ano: {anio}")
                lista_consolidados_a_combinar.append(df_consolidado_actual)

            df_consolidados_por_programa = pd.concat(lista_consolidados_a_combinar, ignore_index=True)

            num_consolidados = len(lista_consolidados_a_combinar)
            df_programa_academico_repetido = pd.concat( [dict_programas_academicos[cod_prog_actual].programa_academico] * num_consolidados, ignore_index=True )

            # df_consolidados_final = df_consolidados_final.reset_index(drop=True)
            # df_programa_academico_repetido = df_programa_academico_repetido.reset_index(drop=True)

            df_programa_academico_final = pd.concat( [df_programa_academico_repetido, df_consolidados_por_programa], axis = 1)

            lista_programas_academicos_a_combinar.append(df_programa_academico_final)

        df_final = pd.concat(lista_programas_academicos_a_combinar, ignore_index=True)

        # FIXME: MANEJAR EL CASO EN QUE PROBABLEENTE ESTÉ VACÍO EL DATAFRAME
        df_final.to_csv("Resultados.csv", sep=";", index=False, encoding="utf-8-sig")
        print("Probando")