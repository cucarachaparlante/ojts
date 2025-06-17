import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

# ---------------------- Funciones Objetivo ----------------------

def lata(r: float) -> float:
    return 2 * math.pi * r * r + (500 / r)

def caja(l: float) -> float:
    return -(4 * pow(l, 3) - 60 * l * l + 200 * l)

def funcion_0(x: float) -> float:
    return x**2 + (54/x)

def funcion_1(x: float) -> float:
    return x**3 + 2*x - 3

def funcion_2(x: float) -> float:
    return x**4 + x**2 - 33

def funcion_3(x: float) -> float:
    return 3*x**4 - 8*x**3 - 6*x**2 + 12*x

# ---------------------- Búsqueda Exhaustiva ----------------------

def busqueda_exhaustiva(a: float, b: float, n: int, funcion: callable) -> tuple[float, float]:
    delta_x = (b - a) / n
    x1 = a
    x2 = x1 + delta_x
    x3 = x2 + delta_x

    while not (funcion(x1) >= funcion(x2) <= funcion(x3)) and x3 <= b:
        x1 = x2
        x2 = x3
        x3 = x2 + delta_x

    return (x1, x3)

# ---------------------- Configuración Visual ----------------------

st.set_page_config(page_title="🔍 Búsqueda Exhaustiva", layout="centered")

st.markdown("""
    <style>
    body { background-color: #f0f4f8; }
    .stApp {
        background: linear-gradient(to bottom, #e3f2fd, #ffffff);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 Búsqueda Exhaustiva con Streamlit")
st.markdown("Explora el comportamiento de diferentes funciones y encuentra intervalos de mínimo local usando el **método de búsqueda exhaustiva**.")

# ---------------------- Interfaz ----------------------

funciones = {
    "Área de una lata (lata)": lata,
    "Área de una caja (caja)": caja,
    "f(x) = x² + 54/x": funcion_0,
    "f(x) = x³ + 2x - 3": funcion_1,
    "f(x) = x⁴ + x² - 33": funcion_2,
    "f(x) = 3x⁴ - 8x³ - 6x² + 12x": funcion_3,
}

opcion_funcion = st.selectbox("📌 Elige la función a evaluar", list(funciones.keys()))
funcion = funciones[opcion_funcion]

a = st.number_input("🔽 Límite inferior", value=0.0)
b = st.number_input("🔼 Límite superior", value=5.0)
n = st.slider("📊 Número de particiones", min_value=10, max_value=500, value=100, step=10)

if st.button("🚀 Ejecutar Búsqueda Exhaustiva"):

    # Validación para evitar división por cero
    if (opcion_funcion in ["Área de una lata (lata)", "f(x) = x² + 54/x"]) and a <= 0:
        st.error("❌ El límite inferior debe ser mayor que 0 para esta función (evita división por cero).")
    else:
        try:
            intervalo = busqueda_exhaustiva(a, b, n, funcion)
            x_min = (intervalo[0] + intervalo[1]) / 2
            y_min = funcion(x_min)

            st.success(f"✅ Intervalo encontrado: {intervalo}")
            st.info(f"📍 Aproximación del mínimo local:\n\n**x = {x_min:.4f}**, **f(x) = {y_min:.4f}**")

            # Visualización con punto en el mínimo
            x_vals = np.linspace(a, b, 1000)
            y_vals = [funcion(x) for x in x_vals]

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals, label="Función", color='blue')
            ax.plot(x_min, y_min, marker='o', markersize=8, color='red', label="Mínimo estimado")
            ax.set_title("Visualización de la función")
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.legend()
            ax.grid(True)

            st.pyplot(fig)

        except Exception as e:
            st.error(f"⚠️ Ocurrió un error: {e}")
