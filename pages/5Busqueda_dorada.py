import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math


def lata(r):
    return 2 * math.pi * r * r + (500 / r)

def caja(l):
    return -(4 * l**3 - 60 * l**2 + 200 * l)

def funcion_0(x):
    return float('inf') if x == 0 else x**2 + (54/x)

def funcion_1(x):
    return x**3 + 2*x - 3

def funcion_2(x):
    return x**4 + x**2 - 33

def funcion_3(x):
    return 3*x**4 - 8*x**3 - 6*x**2 + 12*x

def golden_section_search(a: float, b: float, epsilon: float, func: callable):
    phi = (1 + np.sqrt(5)) / 2 
    resphi = 2 - phi            

    c = a + resphi * (b - a)
    d = b - resphi * (b - a)
    fc = func(c)
    fd = func(d)
    
    points = [(c, fc), (d, fd)]  
    min_intervalo = (a, b)

    while abs(b - a) > epsilon:
        if fc < fd:
            b, d, fd = d, c, fc
            c = a + resphi * (b - a)
            fc = func(c)
        else:
            a, c, fc = c, d, fd
            d = b - resphi * (b - a)
            fd = func(d)
        
        points.append((c, fc))
        points.append((d, fd))
        min_intervalo = (a, b)

    return (a + b) / 2, points, min_intervalo

def plot_function_with_points(func, a, b, points, title):
    x = np.linspace(a, b, 1000)
    y = [func(xi) for xi in x]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, label='Función', color='black')
    
    if points:
        x_points, y_points = zip(*points)
        ax.scatter(x_points, y_points, color='red', label='Puntos evaluados')

    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()
    ax.grid(True)
    return fig


st.set_page_config(page_title="🔆 Golden Section Search", layout="centered")


st.markdown("""
    <style>
    body { background-color: #f9fafb; }
    .stApp {
        background: linear-gradient(to bottom, #d9e7f8, #ffffff);
    }
    </style>
""", unsafe_allow_html=True)
st.title("🔆 Método de Búsqueda de la Sección Áurea")

functions = {
    'Lata': (lata, 0.1, 10),
    'Caja': (caja, 2, 3),
    'Función 1 (x² + 54/x)': (funcion_0, 0.1, 10),
    'Función 2 (x³ + 2x - 3)': (funcion_1, 0, 5),
    'Función 3 (x⁴ + x² - 33)': (funcion_2, -2.5, 2.5),
    'Función 4 (3x⁴ - 8x³ - 6x² + 12x)': (funcion_3, -1.5, 3)
}

funcion_nombre = st.selectbox("📌 Selecciona la función", list(functions.keys()))
funcion, default_a, default_b = functions[funcion_nombre]

a = st.number_input("🔽 Límite inferior (a)", value=float(default_a))
b = st.number_input("🔼 Límite superior (b)", value=float(default_b))

epsilon = st.number_input("⚠️ Precisión (ε)", min_value=0.0001, max_value=1.0, value=0.01, step=0.0001, format="%.4f")

if st.button("▶️ Ejecutar Búsqueda"):
    if funcion_nombre == 'Función 1 (x² + 54/x)' and (a <= 0 <= b):
        st.error("❌ El intervalo no puede incluir x=0 para esta función (división por cero).")
    else:
        minimo, points, min_intervalo = golden_section_search(a, b, epsilon, funcion)
        st.success(f"✅ Mínimo aproximado en x = {minimo:.6f}")
        st.write(f"Último intervalo evaluado: {min_intervalo}")
        
        fig = plot_function_with_points(funcion, a, b, points, f"{funcion_nombre} (ε={epsilon})")
        st.pyplot(fig)
