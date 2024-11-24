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
            df_opciones = self.obtener_filtrado_de_programas(ANIO_INI)

        df_filtrado = df_opciones

        if not df_filtrado.empty:

            st.session_state.df_filtrado = df_filtrado

            if "df_filtrado" not in st.session_state:
                st.session_state.df_filtrado = df_filtrado

            if filtro_nombre:
                st.session_state.df_filtrado = st.session_state.df_filtrado[st.session_state.df_filtrado["PROGRAMA ACADÉMICO"].str.contains(filtro_nombre, case=False, na=False)]

            event = st.dataframe(
                st.session_state.df_filtrado,
                key="opciones_df",
                on_select="rerun",
                selection_mode="multi-row",
                hide_index=True,
            )
            #st.write("Seleccionados: ", event.selection)

            if event.selection:
                selected_rows = event.selection['rows']  # Filas seleccionadas
                selected_column = 'CÓDIGO SNIES DEL PROGRAMA'  # Nombre de la columna de la que queremos los valores

                # Obtener los valores de la columna 'CODIGO SNIES DEL PROGRAMA' para las filas seleccionadas
                selected_values = df_filtrado.loc[selected_rows, selected_column].tolist()

                # Mostrar la lista resultante en Streamlit
                st.write(f"Valores seleccionados de la columna '{selected_column}': {selected_values}")




        # FIXME: ESTO DEBE SER UN INPUT EN EL STREAMLIT
        # Se definen los programas académicos a buscar y se agregan al mapa
        lista_cod_snies = [1042, 1043]

        #self.controladorSnies.procesarDatos(ANIO_INI, ANIO_FIN, lista_cod_snies)


    def obtener_filtrado_de_programas(self, ANIO_INI):
        filtrado = []
        anio = str(ANIO_INI)
        RUTA = "C:/SNIES_EXTRACTOR/inputs/new/ADMITIDOS" + anio + ".xlsx"
        df = pd.read_excel(RUTA, usecols=["PROGRAMA ACADÉMICO", "INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)",
                                          "CÓDIGO SNIES DEL PROGRAMA", "NIVEL DE FORMACIÓN", "IES_PADRE",
                                          "PRINCIPAL O SECCIONAL"] )
        # FIXME: ESTÁ BORRANDO LOS REPETIDOS. Y YA QUE HAY VARIOS PROGRAMAS QUE SE LLAMAN IGUAL EN DIFERENTES UNIVERSIDADES
        # FIXME: ESTÁ BORRANDO DE LAS OTRAS UNIVERSIDADES TAMBIÉN
        df = df.drop_duplicates(subset="PROGRAMA ACADÉMICO")
        df = df.reset_index(drop=True)

        return df




