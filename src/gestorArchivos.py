import pandas as pd

class GestorArchivos:
    def __init__(self):
        pass

    def leer_archivo(self, RUTA_BASE, anio, dict_programas_academicos, atributo_del_archivo, primera_vez):

        ruta_completa = RUTA_BASE + atributo_del_archivo + anio + ".xlsx"
        print(f"La ruta del archivo es \n{ruta_completa}")
        df = pd.read_excel(ruta_completa)
        df = self.convertir_columna_to_int64(df)


        list_cod_snies = list(dict_programas_academicos.keys())

        for cod_snies in list_cod_snies:
            df_filtrado = df[df["CÓDIGO SNIES DEL PROGRAMA"] == cod_snies]
            df_filtrado = self.convertir_columna_sexo(df_filtrado)

            index_columna_inicio_exclusion = df.columns.get_loc("ID SEXO")


            if primera_vez:
                dict_programas_academicos[cod_snies].programa_academico = df_filtrado.iloc[:, :index_columna_inicio_exclusion]

            if anio not in dict_programas_academicos[cod_snies].dict_consolidados.keys():
                consolidado_actual = df_filtrado.iloc[:, index_columna_inicio_exclusion:]
                consolidado_actual = consolidado_actual.reset_index(drop=True)

                dict_programas_academicos[cod_snies].dict_consolidados[anio] = consolidado_actual


        for cod_snies in list_cod_snies:
            df_filtrado = df[df["CÓDIGO SNIES DEL PROGRAMA"] == cod_snies]
            df_filtrado = df_filtrado.reset_index(drop=True)



            if atributo_del_archivo == "inscritos":
                dict_programas_academicos[cod_snies].dict_consolidados[anio].loc[:, "INSCRITOS"] = df_filtrado["INSCRITOS"]

            if atributo_del_archivo == "admitidos":
                dict_programas_academicos[cod_snies].dict_consolidados[anio].loc[:, "ADMITIDOS"] = df_filtrado.loc[:, "ADMITIDOS"]

            if atributo_del_archivo == "matriculados":
                dict_programas_academicos[cod_snies].dict_consolidados[anio].loc[:, "MATRICULADOS"] = df_filtrado.loc[:, "MATRICULADOS"]

            if atributo_del_archivo == "matriculadosPrimerSemestre":
                dict_programas_academicos[cod_snies].dict_consolidados[anio].loc[:, "PRIMER CURSO"] = df_filtrado.loc[:, "PRIMER CURSO"]

            if atributo_del_archivo == "graduados":
                dict_programas_academicos[cod_snies].dict_consolidados[anio].loc[:, "GRADUADOS"] = df_filtrado.loc[:, "GRADUADOS"]


    def exportar_archivo(self, dict_programas_academicos):

        # FIXME: manejar casos en los que algo esté vacío
        lista_programas_academicos_a_combinar = []

        for cod_prog_actual, programa_academico_obj in dict_programas_academicos.items():

            lista_consolidados_a_combinar = []

            for anio, df_consolidado_actual in dict_programas_academicos[cod_prog_actual].dict_consolidados.items():
                lista_consolidados_a_combinar.append(df_consolidado_actual)

            df_consolidados_por_programa = pd.concat(lista_consolidados_a_combinar, ignore_index=True)

            num_consolidados = len(lista_consolidados_a_combinar)
            df_programa_academico_repetido = pd.concat( [dict_programas_academicos[cod_prog_actual].programa_academico] * num_consolidados, ignore_index=True )

            df_programa_academico_final = pd.concat( [df_programa_academico_repetido, df_consolidados_por_programa], axis = 1)

            lista_programas_academicos_a_combinar.append(df_programa_academico_final)

        df_final = pd.concat(lista_programas_academicos_a_combinar, ignore_index=True)

        # FIXME: MANEJAR EL CASO EN QUE PROBABLEENTE ESTÉ VACÍO EL DATAFRAME
        df_final.to_excel("Resultados.xlsx")


    def convertir_columna_to_int64(self, df):
        df["CÓDIGO SNIES DEL PROGRAMA"] = df["CÓDIGO SNIES DEL PROGRAMA"].astype(str).str.strip()
        df["CÓDIGO SNIES DEL PROGRAMA"] = pd.to_numeric(df["CÓDIGO SNIES DEL PROGRAMA"], errors='coerce')
        df.dropna(subset=["CÓDIGO SNIES DEL PROGRAMA"], inplace=True)
        df["CÓDIGO SNIES DEL PROGRAMA"] = df["CÓDIGO SNIES DEL PROGRAMA"].astype("int64")

        return df

    def convertir_columna_sexo(self, df):
        df.loc[:, "SEXO"] = df["SEXO"].replace({'Femenino': 'Mujer', 'Masculino': 'Hombre'})
        return df