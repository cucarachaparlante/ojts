import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# Estilo CSS para el fondo y apariencia
st.markdown("""
    <style>
    body { background-color: #f9fafb; }
    .stApp {
        background: linear-gradient(to bottom, #d9e7f8, #ffffff);
    }
    </style>
""", unsafe_allow_html=True)

# ------------------- Funciones -------------------

def metodo_newton_raphson(f, x0, epsilon, delta=1e-5, max_iter=100, a=None, b=None):
    puntos = []
    x = x0

    for _ in range(max_iter):
        fx = f(x)
        derivada = (f(x + delta) - f(x)) / delta
        puntos.append((x, fx))

        if abs(derivada) < 1e-10:
            st.warning("Derivada muy pequeña. Método detenido.")
            break

        x_nuevo = x - fx / derivada

        if a is not None:
            x_nuevo = max(a, x_nuevo)
        if b is not None:
            x_nuevo = min(b, x_nuevo)

        if abs(x_nuevo - x) < epsilon or abs(f(x_nuevo)) < epsilon:
            x = x_nuevo
            puntos.append((x, f(x)))
            break

        x = x_nuevo

    return x, puntos

def plot_function_with_points(func, a, b, points, title):
    x = np.linspace(a, b, 1000)
    y = [func(xi) for xi in x]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, label='Función', color='black')
    if points:
        x_points, y_points = zip(*points)
        ax.scatter(x_points, y_points, color='red', label='Puntos Visitados')
    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()
    ax.grid(True)
    return fig

# ------------------- Definición de funciones a usar -------------------

def lata(r): return 2 * math.pi * r * r + (500 / r)
def caja(l): return -(4 * l**3 - 60 * l**2 + 200 * l)
def funcion_0(x): return float('inf') if x == 0 else x**2 + (54/x)
def funcion_1(x): return x**3 + 2*x - 3
def funcion_2(x): return x**4 + x**2 - 33
def funcion_3(x): return 3*x**4 - 8*x**3 - 6*x**2 + 12*x

functions = {
    'Lata': (lata, 1, 0.1, 10),
    'Caja': (caja, 2, 2, 3),
    'Función 1 (x^2 + 54/x)': (funcion_0, 5, 0.1, 10),
    'Función 2 (x^3 + 2x - 3)': (funcion_1, 1, 0, 5),
    'Función 3 (x^4 + x^2 - 33)': (funcion_2, 2, -2.5, 2.5),
    'Función 4 (3x^4 - 8x^3 - 6x^2 + 12x)': (funcion_3, 1, -1.5, 3)
}

# ------------------- Interfaz Streamlit -------------------

st.title("📐 Método de Newton-Raphson")

funcion_nombre = st.selectbox("📌 Selecciona la función", list(functions.keys()))
funcion, default_x0, default_a, default_b = functions[funcion_nombre]

x0 = st.number_input("Punto inicial (x0)", value=float(default_x0))
a = st.number_input("Límite inferior (a)", value=float(default_a))
b = st.number_input("Límite superior (b)", value=float(default_b))

epsilon = st.number_input("Precisión (ε)", min_value=0.000001, max_value=0.1, value=0.001, step=0.000001, format="%.6f")
delta = st.number_input("Delta para derivada (δ)", min_value=1e-7, max_value=1e-2, value=1e-5, format="%.7f")

if st.button("▶️ Ejecutar Newton-Raphson"):
    if funcion_nombre == 'Función 1 (x^2 + 54/x)' and (a <= 0 <= b):
        st.error("❌ El intervalo no puede incluir x=0 para esta función (división por cero).")
    else:
        minimo, points = metodo_newton_raphson(funcion, x0, epsilon, delta=delta, a=a, b=b)
        st.success(f"Mínimo aproximado en x = {minimo:.6f}, f(x) = {funcion(minimo):.6f}")

        fig = plot_function_with_points(funcion, a, b, points, f"{funcion_nombre} (ε={epsilon})")
        st.pyplot(fig)
