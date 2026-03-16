import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

st.set_page_config(page_title="Clusters K-Means", layout="wide")
st.title("ML: Aprendizaje No Supervisado — K-Means Clustering")
st.write("Sube un archivo CSV")

st.sidebar.header("⚙️ Parámetros del modelo")
k = st.sidebar.slider("Número de clústeres (K)", min_value=2, max_value=10, value=3)
max_iter = st.sidebar.slider("Iteraciones máximas", min_value=50, max_value=500, value=300, step=50)
random_state = st.sidebar.number_input("Semilla aleatoria", min_value=0, max_value=999, value=42)

st.sidebar.divider()
st.sidebar.subheader("¿Qué es K-Means?")
st.sidebar.write(
    "K-Means agrupa los datos en **K clústeres** buscando que cada punto "
    "quede lo más cerca posible al centro de su grupo. "
    "El algoritmo repite dos pasos hasta converger: "
    "**asignar** cada punto al centroide más cercano y "
    "**recalcular** los centroides."
)

st.subheader("Sube tu archivo CSV")
uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="latin1")
    st.success(f"Archivo cargado: {df.shape[0]} filas, {df.shape[1]} columnas.")
    st.write("Vista previa:", df.head())

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if len(numeric_cols) < 2:
        st.error("El conjunto de datos necesita al menos 2 columnas numéricas.")
        st.stop()

    st.subheader("🔧 Configuración")
    features = st.multiselect(
        "Selecciona las columnas a usar para el clustering",
        options=numeric_cols,
        default=numeric_cols[:2],
    )

    if len(features) < 2:
        st.warning("Selecciona al menos 2 columnas.")
        st.stop()

    X = df[features].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    modelo = KMeans(n_clusters=k, max_iter=max_iter, random_state=random_state, n_init=10)
    etiquetas = modelo.fit_predict(X_scaled)

    inertia = modelo.inertia_
    sil = silhouette_score(X_scaled, etiquetas)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("Inercia (WCSS)", f"{inertia:,.1f}")
    with col_m2:
        st.metric("Silhouette Score", f"{sil:.3f}")
    st.caption("Silhouette va de -1 a 1. Más cercano a 1 = clústeres mejor definidos.")

    st.divider()

    st.subheader("Visualización de Clústeres")

    col_x, col_y = st.columns(2)
    with col_x:
        eje_x = st.selectbox("Eje X", features, index=0)
    with col_y:
        eje_y = st.selectbox("Eje Y", features, index=1)

    fig, ax = plt.subplots(figsize=(7, 4))
    scatter = ax.scatter(
        X[eje_x], X[eje_y],
        c=etiquetas,
        cmap="tab10",
        alpha=0.6,
        s=40,
    )
    ax.set_xlabel(eje_x)
    ax.set_ylabel(eje_y)
    ax.set_title(f"K-Means — K={k}")
    plt.colorbar(scatter, ax=ax, label="Clúster")
    st.pyplot(fig)

    st.divider()

    st.subheader(" Método del Codo — ¿Cuál es el mejor K?")
    st.write("El mejor K está donde la inercia deja de bajar significativamente.")

    k_range = range(2, min(11, len(X) // 5 + 2))
    inertias = []
    for ki in k_range:
        km = KMeans(n_clusters=ki, n_init=10, random_state=random_state)
        km.fit(X_scaled)
        inertias.append(km.inertia_)

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    ax2.plot(list(k_range), inertias, "o-", color="steelblue")
    ax2.axvline(k, color="red", linestyle="--", label=f"K actual = {k}")
    ax2.set_xlabel("Número de clústeres (K)")
    ax2.set_ylabel("Inercia")
    ax2.set_title("Método del Codo")
    ax2.legend()
    st.pyplot(fig2)

else:
    st.info("Sube un archivo CSV")