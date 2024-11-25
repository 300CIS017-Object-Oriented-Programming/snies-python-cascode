from streamlit.runtime.scriptrunner_utils.script_run_context import get_script_run_ctx

from sniesController import SniesController
import pandas as pd
import streamlit as st
from streamlit import button


class Menu:
    def __init__(self):
        self.controladorSnies = SniesController()
        self.mostrar_inicio()

    def mostrar_inicio(self):

        st.set_page_config(layout="wide")

        # Título de la aplicación
        st.title('Snies extractor')

        st.sidebar.header('Entrada de Datos')

        # Se definen los años a recorrer
        ANIO_INI, ANIO_FIN = st.sidebar.slider('Selecciona los años en los cuáles buscar:', 2021, 2024, (2021, 2022))
        filtro_nombre = st.sidebar.text_input("Escriba un nombre para buscar en los programas académicos: ")


        if "anio_ini" not in st.session_state or st.session_state.get("ANIO_INI") != ANIO_INI:
            st.session_state.ANIO_INI = ANIO_INI
            st.session_state.df_opciones = self.obtener_filtrado_de_programas(ANIO_INI)

        if "df_filtrado" not in st.session_state:
            st.session_state.df_filtrado = st.session_state.df_opciones


        if not st.session_state.df_filtrado.empty:
            st.session_state.df_filtrado = st.session_state.df_opciones


            if filtro_nombre:
                st.session_state.df_filtrado = st.session_state.df_filtrado[
                    st.session_state.df_filtrado["PROGRAMA ACADÉMICO"].str.contains(filtro_nombre, case=False, na=False)]
                st.session_state.df_filtrado.reset_index(drop=True, inplace=True)

            # Crea un set para los codigos snies
            if "filas_seleccionadas" not in st.session_state:
                st.session_state.filas_seleccionadas = set()

            event = st.dataframe(
                st.session_state.df_filtrado,
                key="opciones_df",
                on_select="rerun",
                selection_mode="multi-row",
                #hide_index=True,
            )

            if event.selection:
                selected_rows = event.selection['rows']  # Filas seleccionadas
                selected_snies = st.session_state.df_filtrado.loc[selected_rows, 'CÓDIGO SNIES DEL PROGRAMA'].tolist()
                st.session_state.filas_seleccionadas.update(selected_snies)

            # Filtrar los códigos seleccionados que aún están en el DataFrame filtrado
            codigos_actuales = st.session_state.df_filtrado['CÓDIGO SNIES DEL PROGRAMA'].tolist()
            """codigos_seleccionados_visibles = [snies for snies in st.session_state.filas_seleccionadas if
                                              snies in codigos_actuales]"""


            if st.button("Limpiar selección"):
                st.session_state.filas_seleccionadas.clear()
                st.session_state.selected_values = []

            list_filas_seleccionadas = list(st.session_state.filas_seleccionadas)
            # Mostrar la lista resultante en Streamlit
            st.write(f"Códigos SNIES seleccionados: {list_filas_seleccionadas}")

            if list_filas_seleccionadas and st.button("Procesar datos"):
                self.controladorSnies.procesarDatos(ANIO_INI, ANIO_FIN, list_filas_seleccionadas)
                st.write("Se procesó correctamente")



    def obtener_filtrado_de_programas(self, ANIO_INI):
        filtrado = []
        anio = str(ANIO_INI)
        RUTA = "C:/SNIES_EXTRACTOR/inputs/new/ADMITIDOS" + anio + ".xlsx"
        df = pd.read_excel(RUTA, usecols=["PROGRAMA ACADÉMICO", "INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)",
                                          "CÓDIGO SNIES DEL PROGRAMA", "NIVEL DE FORMACIÓN", "IES_PADRE",
                                          "PRINCIPAL O SECCIONAL"] )
        # FIXME: ESTÁ BORRANDO LOS REPETIDOS. Y YA QUE HAY VARIOS PROGRAMAS QUE SE LLAMAN IGUAL EN DIFERENTES UNIVERSIDADES
        # FIXME: ESTÁ BORRANDO DE LAS OTRAS UNIVERSIDADES TAMBIÉN
        df = df.drop_duplicates(subset=["PROGRAMA ACADÉMICO", "INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)", "CÓDIGO SNIES DEL PROGRAMA"])
        df = df.reset_index(drop=True)

        return df




