import streamlit as st
import pandas as pd

class graficasEstadisticas:
    def __init__(self):

        pass

    def grafica_linea(self):
        st.title("Gráfico de Líneas Interactivo con Plotly")

        ruta_completa = "src/Resultados.xlsx"

        archivo_subido = pd.read_excel(ruta_completa)

        metricas_disponibles = [
            "INSCRITOS",
            "GRADUADOS",
            "MATRICULADOS",
            "ADMITIDOS",
        ]
        metricas_seleccionadas = st.sidebar.multiselect(
            "Selecciona las métricas para graficar", metricas_disponibles, default=metricas_disponibles[:1])


        archivo_subido['SEMESTRECOMPLETO'] = archivo_subido['AÑO'] + archivo_subido['SEMESTRE']
        opciones = ["AÑO", "SEMESTRECOMPLETO"]
        columna_eje_x = st.selectbox("Selecciona una variable", opciones)

        st.sidebar.title("Filtros")
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
                valores_unicos = archivo_subido[columna].dropna().unique()
                seleccion = st.sidebar.selectbox(
                    f"Escoja una opción para {columna}",
                    ["Todos"] + list(valores_unicos)
                )
                filtros[columna] = seleccion

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

