import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

st.set_page_config(page_title="ML Export", layout="wide")
st.title("ðŸ¤ ML: Regresión y Exportación")

uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if uploaded_file is not None:
    # CORRECCIÓN 1: Leer el archivo subido, no una ruta hardcodeada
    df = pd.read_csv(uploaded_file, encoding='latin1')

    col_config, col_viz = st.columns(2)
    with col_config:
        # CORRECCIÓN 2: Usar nombres de columnas, no valores de columna
        target = st.selectbox("Variable a predecir (Y)", df.columns.tolist())
        features = st.multiselect("Variables predictoras (X)", df.columns.tolist())

    if features and target:
        X, y = df[features], df[target]
        model = LinearRegression().fit(X, y)
        df['Prediccion_Modelo'] = model.predict(X)

        r2 = r2_score(y, df['Prediccion_Modelo'])
        st.metric("Precisión del Modelo (R²)", f"{r2:.2%}")

        with col_viz:
            if len(features) == 1:
                fig, ax = plt.subplots()
                ax.scatter(X, y, color="blue", alpha=0.5, label="Datos reales")
                ax.plot(X, df['Prediccion_Modelo'], color="red", label="Predicción")
                ax.legend()
                st.pyplot(fig)

        st.divider()
        st.subheader("📥 Descargar Resultados")
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV con Predicciones",
            data=csv_data,
            file_name="resultados_prediccion.csv",
            mime="text/csv",
        )
        st.write("Vista previa:", df.head())

        st.subheader("🔮 Predicción manual")
        inputs = [st.number_input(f"Ingresa {f}", value=0.0) for f in features]
        if st.button("Calcular"):
            resultado = model.predict([inputs])[0]
            st.success(f"Resultado: {resultado:.2f}")

else:
    st.info("Sube un CSV para activar las funciones.")