import streamlit as st
import pandas as pd
import plotly.express as px

class graficasEstadisticas:
    def __init__(self):

        pass


    def grafica_linea(self, df):
        st.title("Gráfico de Líneas Interactivo")

        archivo_subido = df


        archivo_subido['AÑO']= archivo_subido['AÑO'].astype(str)
        archivo_subido['SEMESTRES'] = archivo_subido['AÑO'].astype(str) + archivo_subido['SEMESTRE'].astype(str)
        opciones = ["AÑO", "SEMESTRES"]
        columna_eje_x = st.selectbox("Selecciona una variable", opciones)

        st.sidebar.title("Filtros")

        metricas_disponibles = [
            "INSCRITOS",
            "GRADUADOS",
            "MATRICULADOS",
            "ADMITIDOS",
        ]
        metricas_seleccionadas = st.sidebar.multiselect(
            "Selecciona las métricas para graficar", metricas_disponibles, default=metricas_disponibles[:1])

        columnas_filtro = [
            "INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)",
            "DESC CINE CAMPO ESPECIFICO",
            "PROGRAMA ACADÉMICO",
            "NIVEL DE FORMACIÓN",
            "SEXO"
        ]
        filtros = {}
        for columna in columnas_filtro:
            if columna in archivo_subido.columns:
                archivo_subido.valores_unicos = archivo_subido[columna].dropna().unique()
                st.session_state.seleccion = st.sidebar.selectbox(
                    f"Escoja una opción para {columna}",
                    ["Todos"] + list(archivo_subido.valores_unicos)
                )
                filtros[columna] = st.session_state.seleccion

        datos_filtrados = archivo_subido.copy()
        for columna, seleccion in filtros.items():
            if seleccion != "Todos":
                datos_filtrados = datos_filtrados[datos_filtrados[columna] == seleccion]

        anios_list = datos_filtrados[columna_eje_x].unique()
        df_resultante = pd.DataFrame({columna_eje_x: anios_list})

        for metrica in metricas_seleccionadas:
            if metrica in datos_filtrados.columns:
                datos_agrupados = datos_filtrados.groupby([columna_eje_x] , as_index=False)[metrica].sum()
                columna_metrica = pd.DataFrame({metrica: datos_agrupados[metrica]})
                df_resultante = pd.concat([df_resultante, columna_metrica], axis=1, join='outer')

        df_resultante.set_index(columna_eje_x, inplace=True)
        st.line_chart(df_resultante)


    def grafica_barras(self, df):
        st.title("Gráfico de Líneas Interactivo con Plotly")

        archivo_subido = df

        #archivo_subido['AÑO']= archivo_subido['AÑO'].astype(str)

        archivo_subido['SEMESTRES'] = archivo_subido['AÑO'].astype(str) + archivo_subido['SEMESTRE'].astype(str)
        opciones = ["AÑO", "SEMESTRES"]
        columna_eje_x = st.selectbox("Selecciona una variable", opciones)

        st.sidebar.title("Filtros")

        metricas_disponibles = [
            "INSCRITOS",
            "GRADUADOS",
            "MATRICULADOS",
            "ADMITIDOS",
        ]
        metrica_seleccionada = st.sidebar.selectbox(
            "Selecciona las métricas para graficar", metricas_disponibles)

        columnas_opciones = [
            "MODALIDAD",
            "IES ACREDITADA",
            "PROGRAMA ACADÉMICO",
            "DESC CINE CAMPO ESPECIFICO",
            "NIVEL DE FORMACIÓN",
            "SEXO"
        ]
        seleccionada = st.sidebar.selectbox(
            "Selecciona una opción:",
            columnas_opciones   # Lista de opciones
        )

        anios_list = archivo_subido[columna_eje_x]
        df_resultante = pd.DataFrame({columna_eje_x: anios_list})

        if metrica_seleccionada in archivo_subido.columns and seleccionada in archivo_subido.columns:
            # Agrupar datos por Año y la variable seleccionada
            df_resultante = archivo_subido.groupby([columna_eje_x, seleccionada], as_index=False)[metrica_seleccionada].sum()

        fig = px.bar(
            df_resultante,
            x=columna_eje_x,  # Eje X

            y=metrica_seleccionada,  # Eje Y (de la versión vieja)

            color=seleccionada,  # Agrupación por color
            barmode="stack",  # Barras apiladas
            title="Gráfico de Barras ",
            labels={metrica_seleccionada: "Cantidad", columna_eje_x: "Periodo", seleccionada: "Variable"}
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)