import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
import Acotamiento as AC  # Asegúrate que esté en la misma carpeta

# Estilo CSS para el fondo y apariencia
st.markdown("""
    <style>
    body { background-color: #f9fafb; }
    .stApp {
        background: linear-gradient(to bottom, #d9e7f8, #ffffff);
    }
    </style>
""", unsafe_allow_html=True)

def calcular_derivada(x, delta, funcion):
    return (funcion(x + delta) - funcion(x - delta)) / (2 * delta)

def Secante(a, b, epsilon, funcion, delta=0.01):
    fa = calcular_derivada(a, delta, funcion)
    fb = calcular_derivada(b, delta, funcion)

    puntos_x = [a, b]
    puntos_y = [funcion(a), funcion(b)]

    while abs(b - a) > epsilon:
        if fb - fa == 0:
            st.warning("División entre cero en método de la secante. Deteniendo.")
            break  # Evitar división por cero

        x_new = b - fb * (b - a) / (fb - fa)

        if abs(calcular_derivada(x_new, delta, funcion)) < epsilon:
            puntos_x.append(x_new)
            puntos_y.append(funcion(x_new))
            return x_new, list(zip(puntos_x, puntos_y))

        a, b = b, x_new
        fa = fb
        fb = calcular_derivada(b, delta, funcion)

        puntos_x.append(b)
        puntos_y.append(funcion(b))

    return b, list(zip(puntos_x, puntos_y))

def plot_function_with_points(funcion, a, b, puntos, titulo):
    x_vals = np.linspace(a, b, 500)
    y_vals = [funcion(x) for x in x_vals]

    puntos_x, puntos_y = zip(*puntos) if puntos else ([], [])

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_vals, y_vals, label='Función')
    ax.scatter(puntos_x, puntos_y, c="red", label='Puntos del método')
    ax.set_title(titulo)
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()
    ax.grid(True)
    return fig

# ---------------- Funciones a optimizar ----------------

def lata(r): return 2 * math.pi * r * r + (500 / r)
def caja(l): return -(4 * l**3 - 60 * l**2 + 200 * l)
def funcion_0(x): return float('inf') if x == 0 else x**2 + (54/x)
def funcion_1(x): return x**3 + 2*x - 3
def funcion_2(x): return x**4 + x**2 - 33
def funcion_3(x): return 3*x**4 - 8*x**3 - 6*x**2 + 12*x

functions = {
    'Lata': (lata, 0.2, 5),
    'Caja': (caja, 0.2, 5),
    'Función 1 (x^2 + 54/x)': (funcion_0, 0.1, 10),
    'Función 2 (x^3 + 2x - 3)': (funcion_1, 0, 5),
    'Función 3 (x^4 + x^2 - 33)': (funcion_2, -2.5, 2.5),
    'Función 4 (3x^4 - 8x^3 - 6x^2 + 12x)': (funcion_3, -1.5, 3)
}

# ---------------- Interfaz Streamlit ----------------

st.title("⚖️ Método de la Secante para Encontrar Mínimos")

funcion_nombre = st.selectbox("Selecciona la función", list(functions.keys()))
funcion, inicio_default, fin_default = functions[funcion_nombre]

inicio = st.number_input("Intervalo inicio (a)", value=float(inicio_default))
fin = st.number_input("Intervalo fin (b)", value=float(fin_default))
epsilon = st.number_input("Precisión (ε)", min_value=0.000001, max_value=0.1, value=0.001, step=0.000001, format="%.6f")
delta = st.number_input("Delta para derivada numérica", min_value=0.000001, max_value=0.1, value=0.01, step=0.000001, format="%.6f")

if st.button("▶️ Ejecutar Método de la Secante"):
    a, b = AC.fase_acotamiento(inicio, fin, delta, funcion=funcion)
    
    minimo, puntos = Secante(a, b, epsilon, funcion, delta=delta)
    st.success(f"Mínimo aproximado en x = {minimo:.6f}, f(x) = {funcion(minimo):.6f}")

    fig = plot_function_with_points(funcion, a, b, puntos, f"{funcion_nombre} (ε={epsilon})")
    st.pyplot(fig)
