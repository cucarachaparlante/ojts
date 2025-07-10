import streamlit as st

st.title("📌 Búsqueda Unidireccional")

st.markdown("""
<style>
.justify {
    text-align: justify;
    font-size: 16px;
    line-height: 1.7em;
    color: #333333;
}
</style>

<div class="justify">
<p>
La <strong>búsqueda unidireccional</strong> es una técnica utilizada para optimizar funciones que dependen de varias variables, pero enfocándose únicamente en una dirección específica. En lugar de explorar todas las variables al mismo tiempo, este método reduce el problema a buscar el mejor valor a lo largo de una sola línea o camino determinado..
</p>

<p>
El proceso inicia en un punto dentro del espacio de búsqueda y se define una dirección a seguir. Luego, se analiza cómo cambia la función objetivo al moverse en esa dirección, buscando encontrar el punto que minimice o maximice el valor de la función.
</p>

<p>
Este enfoque es muy útil porque simplifica problemas complejos en uno más manejable, y suele emplearse como paso dentro de métodos de optimización más avanzados, como el descenso por gradiente o algoritmos basados en Newton.
</p>

<p>
A continuación, se muestra una implementación sencilla que ejemplifica cómo funciona la búsqueda unidireccional en una función de prueba.
</p>
</div>
""", unsafe_allow_html=True)


import numpy as np
import matplotlib.pyplot as plt

st.subheader("🧪 Ejemplo interactivo")

def funcion(x):
    return (x - 2)**2 + 1  

a = st.number_input("Límite inferior (a)", value=0.0)
b = st.number_input("Límite superior (b)", value=5.0)
epsilon = st.number_input("Precisión (ε)", value=0.01)

def busqueda_unidireccional(f, a, b, epsilon):
    puntos = []
    while abs(b - a) > epsilon:
        x1 = a + (b - a) / 3
        x2 = b - (b - a) / 3
        f1 = f(x1)
        f2 = f(x2)
        puntos.append((x1, f1))
        puntos.append((x2, f2))

        if f1 < f2:
            b = x2
        else:
            a = x1

    x_opt = (a + b) / 2
    return x_opt, f(x_opt), puntos

if st.button("▶️ Ejecutar búsqueda"):
    x_opt, f_opt, puntos = busqueda_unidireccional(funcion, a, b, epsilon)
    st.success(f"Mínimo aproximado: x = {x_opt:.4f}, f(x) = {f_opt:.4f}")

    x_vals = np.linspace(a - 1, b + 1, 400)
    y_vals = funcion(x_vals)
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label='Función')
    if puntos:
        px, py = zip(*puntos)
        ax.scatter(px, py, color='red', s=30, label='Puntos evaluados')
    ax.axvline(x_opt, color='green', linestyle='--', label='Óptimo')
    ax.set_title("Búsqueda unidireccional")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
