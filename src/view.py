from sniesController import SniesController
import pandas as pd
import streamlit as st
from streamlit import button


class Menu:
    def __init__(self):
        self.controladorSnies = SniesController()

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


    def mostrar_interfaz(self):
        st.set_page_config(page_title="Gestor SNIES", layout="wide")
        st.sidebar.title("Navegación")
        page = st.sidebar.selectbox("Selecciona una página:", ["Inicio", "Carga de Archivos", "Procesar Datos", "Resultados"])
        if page == "Inicio":
            self.mostrar_inicio()
        elif page == "Carga de Archivos":
            self.mostrar_carga_archivos()
        elif page == "Procesar Datos":
            self.procesar_datos()
        elif page == "Resultados":
            self.mostrar_resultados()

    def mostrar_carga_archivos(self):
        st.title("Carga de Archivos")
        # Mostrar archivos predeterminados
        st.subheader("Archivos Cargados Predeterminados (Últimos 4 años)")
        archivos_predeterminados = self.controladorSnies.listar_archivos_predeterminados()
        if archivos_predeterminados:
            for archivo in archivos_predeterminados:
                st.write(f"✔️ {archivo}")
        else:
            st.write("No hay archivos disponibles.")
        # Cargar archivos nuevos
        st.subheader("Subir Archivos Nuevos")
        archivos_subidos = st.file_uploader("Selecciona archivos Excel:", accept_multiple_files=True, type=["xlsx"])
        if archivos_subidos:
            archivos_guardados = self.controladorSnies.cargar_archivos_nuevos(archivos_subidos)
            st.success(f"Archivos cargados correctamente: {', '.join(archivos_guardados)}")

    def mostrar_inicio(self):
        st.title("Bienvenido al Gestor SNIES")
        st.write("""
        Esta aplicación facilita la consolidación de datos académicos. 
        Utiliza el menú de la izquierda para navegar entre las secciones.
        """)

    def procesar_datos(self):
        st.title("Procesar Datos Académicos")
        anio_inicio = st.number_input("Año de inicio:", min_value=2000, max_value=2025, value=2021)
        anio_final = st.number_input("Año final:", min_value=2000, max_value=2025, value=2022)
        codigos_snies = st.text_input("Códigos SNIES (separados por comas):", "1042, 1043")
        if st.button("Procesar Datos"):
            lista_cod_snies = [int(cod.strip()) for cod in codigos_snies.split(",")]
            with st.spinner('Procesando...'):
                self.controladorSnies.procesarDatos(anio_inicio, anio_final, lista_cod_snies)
                st.success("¡Datos procesados con éxito!")

    def mostrar_resultados(self):
        st.title("Resultados Consolidados")
        with open("Resultados.xlsx", "rb") as file:
            st.download_button(label="Descargar Resultados",
                               data=file,
                               file_name="Resultados.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
