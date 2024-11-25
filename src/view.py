import streamlit as st
from sniesController import SniesController

class Menu:
    def __init__(self):
        self.controladorSnies = SniesController()

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
