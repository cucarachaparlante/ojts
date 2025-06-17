import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
import Acotamiento as AC  # Asegúrate que este archivo esté en el mismo directorio

# Estilo CSS para el fondo y apariencia
st.markdown("""
    <style>
    body { background-color: #f9fafb; }
    .stApp {
        background: linear-gradient(to bottom, #d9e7f8, #ffffff);
    }
    </style>
""", unsafe_allow_html=True)

# Funciones auxiliares

def calcular_derivada(x, delta, funcion):
    return (funcion(x + delta) - funcion(x - delta)) / (2 * delta)

def Biseccion(a, b, epsilon, funcion):
    medio = (a + b) / 2
    derivada_medio = calcular_derivada(medio, epsilon, funcion)

    puntos_x = [medio]
    puntos_y = [funcion(medio)]

    while abs(derivada_medio) > epsilon and a < medio < b:
        if derivada_medio < 0:
            a = medio
        else:
            b = medio

        medio = (a + b) / 2
        derivada_medio = calcular_derivada(medio, epsilon, funcion)
        puntos_x.append(medio)
        puntos_y.append(funcion(medio))

    return medio, list(zip(puntos_x, puntos_y))

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

st.title("⚖️ Método de Bisección para Encontrar Mínimos")

funcion_nombre = st.selectbox("Selecciona la función", list(functions.keys()))
funcion, inicio_default, fin_default = functions[funcion_nombre]

inicio = st.number_input("Intervalo inicio (a)", value=float(inicio_default))
fin = st.number_input("Intervalo fin (b)", value=float(fin_default))
epsilon = st.number_input("Precisión (ε)", min_value=0.000001, max_value=0.1, value=0.001, step=0.000001, format="%.6f")

if st.button("▶️ Ejecutar Método de Bisección"):
    # Usamos fase de acotamiento para reducir intervalo
    a, b = AC.fase_acotamiento(inicio, fin, 0.1, funcion=funcion)
    
    minimo, puntos = Biseccion(a, b, epsilon, funcion)
    st.success(f"Mínimo aproximado en x = {minimo:.6f}, f(x) = {funcion(minimo):.6f}")

    fig = plot_function_with_points(funcion, a, b, puntos, f"{funcion_nombre} (ε={epsilon})")
    st.pyplot(fig)
