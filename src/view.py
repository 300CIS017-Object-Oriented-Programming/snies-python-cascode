from sniesController import SniesController
from graficas import graficasEstadisticas
import pandas as pd
import streamlit as st
from streamlit import button
import os

class Menu:
    def __init__(self):
        self.controladorSnies = SniesController()
        self.graficosNew = graficasEstadisticas()


        self.archivos_predeterminados = self.controladorSnies.listar_archivos_predeterminados()
        [anio_min, anio_max] = self.controladorSnies.obtener_anio_minimo_y_maximo(self.archivos_predeterminados)

        self.ANIO_INICIO = anio_min
        self.ANIO_FINAL = anio_max


    def mostrar_interfaz(self):
        st.set_page_config(page_title="Gestor SNIES", layout="wide")
        st.sidebar.title("Navegación")
        page = st.sidebar.selectbox("Selecciona una página:", ["Inicio", "Carga de Archivos", "Procesar Datos", "Resultados", "Visualizaciones"])
        if page == "Inicio":
            self.mostrar_inicio()
        elif page == "Carga de Archivos":
            self.mostrar_carga_archivos()
        elif page == "Procesar Datos":
            self.procesar_datos()
        elif page == "Resultados":
            self.mostrar_resultados()
        elif page == "Visualizaciones":
            self.mostrar_visualizacion()


    def mostrar_carga_archivos(self):
        st.title("Carga de Archivos")
        # Mostrar archivos predeterminados
        st.subheader("Archivos Cargados Predeterminados (Últimos 4 años)")


        if self.archivos_predeterminados:
            for archivo in self.archivos_predeterminados:
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
        # BARRA LATERAL: --------------------------------------------
        st.sidebar.title("Filtrar programas académicos")
        filtro_nombre = st.sidebar.text_input("Escriba una palabra para buscar en los programas académicos disponibles: ",
                                              placeholder="Por ej. 'Medicina', 'Ingeniería'")
        st.sidebar.write("Nota: si al filtrar no encuentra su programa académico, preste atención a las tildes (´) 	"
                         ":nerd_face:, puede que su Programa Académico esté guardado con ellas. :stuck_out_tongue_winking_eye:")

        st.sidebar.title('Entrada de datos para el procesamiento')
        # Cambia las fechas de año máximas y mínimas según los archivos que hayan
        self.ANIO_INICIO, self.ANIO_FINAL = st.sidebar.slider('Selecciona los años en los cuáles buscar:',
                                               self.ANIO_INICIO, self.ANIO_FINAL, (self.ANIO_INICIO, self.ANIO_FINAL))

        # INICIALIZAR VARIABLES EN SESSION STATE----------------------
        if "anio_ini" not in st.session_state or st.session_state.get("ANIO_INI") != self.ANIO_INICIO:
            st.session_state.ANIO_INI = self.ANIO_INICIO
            st.session_state.ANIO_FINAL = self.ANIO_FINAL
            st.session_state.df_opciones = self.obtener_filtrado_de_programas(self.ANIO_INICIO)

        if "df_filtrado" not in st.session_state:
            st.session_state.df_filtrado = st.session_state.df_opciones

        # PANTALLA PRINCIPAL: ---------------------------------------
        st.title("Procesar Datos Académicos")

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


            if st.button("Limpiar listado de códigos SNIES"):
                st.session_state.filas_seleccionadas.clear()
                st.session_state.selected_values = []

            list_filas_seleccionadas = list(st.session_state.filas_seleccionadas)
            # Mostrar la lista resultante en Streamlit
            st.write(f"Códigos SNIES seleccionados: {list_filas_seleccionadas}")

            if list_filas_seleccionadas and st.button("Procesar datos"):
                with st.spinner('Procesando...'):
                    st.session_state.df_consolidado = self.controladorSnies.procesarDatos(self.ANIO_INICIO, self.ANIO_FINAL, list_filas_seleccionadas)


                    st.success("¡Datos procesados con éxito!")
                    st.success("¡Vaya a la página de Resultados para exportar sus resultados! :hugging_face: :money_mouth_face::money_mouth_face:")





    def obtener_filtrado_de_programas(self, ANIO_INI):
        anio = str(ANIO_INI)
        RUTA = "C:/SNIES_EXTRACTOR/inputs/admitidos" + anio +".xlsx"
        df = pd.read_excel(RUTA, usecols=["PROGRAMA ACADÉMICO", "INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)",
                                          "CÓDIGO SNIES DEL PROGRAMA", "NIVEL DE FORMACIÓN", "IES_PADRE",
                                          "PRINCIPAL O SECCIONAL"] )
        df = df.drop_duplicates(subset=["PROGRAMA ACADÉMICO", "INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)", "CÓDIGO SNIES DEL PROGRAMA"])
        df = df.reset_index(drop=True)

        return df


    def mostrar_resultados(self):
        st.title("Resultados Consolidados")

        if 'df_consolidado' not in st.session_state:
            st.session_state.df_consolidado = pd.DataFrame()

        if not st.session_state.df_consolidado.empty:
            # OPCIONES PARA ELEGIR CÓMO EXPORTAR LOS ARCHIVOS

            if "export_xlsx" not in st.session_state:
                st.session_state.export_xlsx = False
            if "export_json" not in st.session_state:
                st.session_state.export_json = False
            if "export_csv" not in st.session_state:
                st.session_state.export_csv = False

                # Mostrar los checkboxes para seleccionar formatos de exportación
            st.markdown("### Selecciona los formatos para exportar los datos procesados:")

            st.session_state.export_xlsx = st.checkbox("Exportar a Excel (.xlsx)",
                                                       value=st.session_state.export_xlsx)
            st.session_state.export_json = st.checkbox("Exportar a JSON (.json)",
                                                       value=st.session_state.export_json)
            st.session_state.export_csv = st.checkbox("Exportar a CSV (.csv)",
                                                      value=st.session_state.export_csv)

            if 'formatos' not in st.session_state:
                st.session_state.formatos = []

            # Botón para ejecutar la exportación
            if st.button("Exportar archivos"):
                if st.session_state.export_xlsx:
                    st.session_state.formatos.append("xlsx")
                if st.session_state.export_json:
                    st.session_state.formatos.append("json")
                if st.session_state.export_csv:
                    st.session_state.formatos.append("csv")

                if st.session_state.formatos:
                    self.exportar_datos(st.session_state.df_consolidado, st.session_state.formatos)
                    st.session_state.formatos = []
                else:
                    st.warning("Selecciona al menos un formato para exportar.")


        else:
            st.write("Aún no hay datos para exportar :disappointed_relieved: :sleepy:")

    def exportar_datos(self, dataframe, formato):
        if "xlsx" in formato:
            filename = "Resultados.xlsx"
            dataframe.to_excel(filename, index=False)
            st.success(f"Archivo exportado como {filename} correctamente.")
        if "json" in formato:
            filename = "Resultados.json"
            dataframe.to_json(filename, orient="records")
            st.success(f"Archivo exportado como {filename} correctamente.")
        if "csv" in formato:
            filename = "Resultados.csv"
            dataframe.to_csv(filename, index=False)
            st.success(f"Archivo exportado como {filename} correctamente.")

    def mostrar_visualizacion(self):

        if "active_function" not in st.session_state:
            st.session_state.active_function = None

        # Manejo de botones
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Iniciar Función 1"):
                st.session_state.active_function = "funcion_1"

        with col2:
            if st.button("Iniciar Función 2"):
                st.session_state.active_function = "funcion_2"

        # Ejecutar la función activa
        if st.session_state.active_function == "funcion_1":
            self.graficosNew.grafica_linea(st.session_state.df_consolidado)
        elif st.session_state.active_function == "funcion_2":
            self.graficosNew.grafica_barras(st.session_state.df_consolidado)
        else:
            st.write("Selecciona una función para iniciar.")

