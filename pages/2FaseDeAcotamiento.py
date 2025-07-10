import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt


def lata(r: float) -> float:
    return 2 * math.pi * r * r + (500 / r)

def caja(l: float) -> float:
    return -(4 * pow(l, 3) - 60 * l * l + 200 * l)

def funcion_0(x: float) -> float:
    if x == 0:
        return float('inf')
    return x**2 + (54/x)

def funcion_1(x: float) -> float:
    return x**3 + 2*x - 3

def funcion_2(x: float) -> float:
    return x**4 + x**2 - 33

def funcion_3(x: float) -> float:
    return 3*x**4 - 8*x**3 - 6*x**2 + 12*x


def fase_acotamiento(x0: float, delta: float, lambda_: float, funcion: callable, max_iter=1000, max_x=1e6):
    x1 = x0
    x2 = x1 + delta if funcion(x1 + delta) < funcion(x1) else x1 - delta
    k = 1
    
    valores_x = [x1, x2]
    valores_y = [funcion(x1), funcion(x2)]
    
    while funcion(x2) < funcion(x1):
        if abs(x2) > max_x or k > max_iter:
            break
        
        x1 = x2
        delta *= lambda_
        if x2 > x0:
            x2 = x1 + delta
        else:
            x2 = x1 - delta
        
        valores_x.append(x2)
        valores_y.append(funcion(x2))
        k += 1
    
    return (min(x1, x2), max(x1, x2)), valores_x, valores_y


st.set_page_config(page_title="📈 Fase de Acotamiento", layout="centered")

st.markdown("""
    <style>
    body { background-color: #f9fafb; }
    .stApp {
        background: linear-gradient(to bottom, #d9e7f8, #ffffff);
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Método de Fase de Acotamiento con Streamlit")
st.markdown("Encuentra un intervalo que contenga un mínimo local de una función usando el método de fase de acotamiento.")

funciones = {
    "Área de una lata": lata,
    "Área de una caja": caja,
    "f(x) = x² + 54/x": funcion_0,
    "f(x) = x³ + 2x - 3": funcion_1,
    "f(x) = x⁴ + x² - 33": funcion_2,
    "f(x) = 3x⁴ - 8x³ - 6x² + 12x": funcion_3,
}

opcion_funcion = st.selectbox("📌 Elige la función a evaluar", list(funciones.keys()))
funcion = funciones[opcion_funcion]

x0 = st.number_input("⚪ Punto inicial (x0)", value=1.0, format="%.4f")
delta = st.number_input("↔ Paso inicial (delta)", value=0.1, min_value=0.0001, format="%.4f")
lambda_ = st.number_input("⏫ Factor de crecimiento (lambda)", value=2.0, min_value=1.1, format="%.2f")

if st.button("🚀 Ejecutar Fase de Acotamiento"):
    if opcion_funcion == "f(x) = x² + 54/x" and x0 == 0:
        st.error("❌ El punto inicial x0 no puede ser 0 para esta función (división por cero).")
    else:
        intervalo, valores_x, valores_y = fase_acotamiento(x0, delta, lambda_, funcion)
        st.success(f"✅ Intervalo estimado con mínimo local: {intervalo}")

        fig, ax = plt.subplots()
        ax.plot(valores_x, valores_y, 'bo-', label="Puntos evaluados")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.set_title("Evolución del método de fase de acotamiento")
        ax.grid(True)
        ax.legend()

        st.pyplot(fig)
