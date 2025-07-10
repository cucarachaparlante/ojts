import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.markdown("""
    <style>
    body { background-color: #f9fafb; }
    .stApp {
        background: linear-gradient(to bottom, #d9e7f8, #ffffff);
    }
    </style>
""", unsafe_allow_html=True)
def rastrigin(x):
    A = 10
    return A * len(x) + sum([(xi**2 - A * np.cos(2 * np.pi * xi)) for xi in x])

def rosenbrock(x):
    return sum([100 * (x[i+1] - x[i]**2)**2 + (1 - x[i])**2 for i in range(len(x) - 1)])

def ackley(x):
    a, b, c = 20, 0.2, 2 * np.pi
    d = len(x)
    sum1 = sum([xi**2 for xi in x])
    sum2 = sum([np.cos(c * xi) for xi in x])
    term1 = -a * np.exp(-b * np.sqrt(sum1 / d))
    term2 = -np.exp(sum2 / d)
    return term1 + term2 + a + np.exp(1)

def sphere(x):
    return sum([xi**2 for xi in x])

def beale(x):
    x1, x2 = x[0], x[1]
    return ((1.5 - x1 + x1 * x2)**2 + 
            (2.25 - x1 + x1 * x2**2)**2 + 
            (2.625 - x1 + x1 * x2**3)**2)

def booth(x):
    x1, x2 = x[0], x[1]
    return (x1 + 2*x2 - 7)**2 + (2*x1 + x2 - 5)**2

def himmelblau(x):
    x1, x2 = x[0], x[1]
    return (x1**2 + x2 - 11)**2 + (x1 + x2**2 - 7)**2

def mccormick(x):
    x1, x2 = x[0], x[1]
    return np.sin(x1 + x2) + (x1 - x2)**2 - 1.5 * x1 + 2.5 * x2 + 1

class BuscadorAleatorio:
    def __init__(self, funcion, punto_inicial, sigma=0.1, iteraciones=1000):
        self.f = funcion
        self.x_actual = np.array(punto_inicial, dtype=float)
        self.sigma = sigma
        self.max_iter = iteraciones
        self.historial = []
        self.trayectoria = []

    def paso(self):
        return self.x_actual + np.random.normal(0, self.sigma, size=len(self.x_actual))

    def ejecutar(self):
        mejor_x = self.x_actual.copy()
        mejor_valor = self.f(mejor_x)
        self.historial.append(mejor_valor)
        self.trayectoria.append(mejor_x.copy())

        for _ in range(self.max_iter):
            nuevo_x = self.paso()
            nuevo_valor = self.f(nuevo_x)

            if nuevo_valor < mejor_valor:
                mejor_x = nuevo_x
                mejor_valor = nuevo_valor

            self.historial.append(mejor_valor)
            self.trayectoria.append(mejor_x.copy())

        return mejor_x, mejor_valor

    def graficar(self, titulo="Recorrido"):
        coords = np.array(self.trayectoria)
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(coords[:, 0], coords[:, 1], marker='o', linestyle='-', markersize=2, label='Trayectoria')
        ax.scatter(coords[0, 0], coords[0, 1], c='green', label='Inicio', s=50)
        ax.scatter(coords[-1, 0], coords[-1, 1], c='red', label='Fin', s=50)
        ax.set_title(titulo)
        ax.set_xlabel("x₁")
        ax.set_ylabel("x₂")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

st.title("🎲 Búsqueda Aleatoria (Random Walk)")

st.markdown("""
La **búsqueda aleatoria**, también conocida como **random walk**, es una técnica de optimización que explora el espacio de soluciones mediante movimientos aleatorios.

A partir de un punto inicial, se generan nuevos puntos cercanos de forma aleatoria y se aceptan aquellos que mejoran el valor de la función objetivo. 
Este proceso se repite durante un número definido de iteraciones o hasta alcanzar una condición de parada.

Es un método simple y versátil que no requiere información sobre derivadas ni la forma de la función, aunque puede ser lento para funciones complejas o de alta dimensión.
""")

funciones = {
    "Rastrigin": (rastrigin, 2),
    "Rosenbrock": (rosenbrock, 2),
    "Ackley": (ackley, 2),
    "Sphere": (sphere, 2),
    "Beale": (beale, 2),
    "Booth": (booth, 2),
    "Himmelblau": (himmelblau, 2),
    "McCormick": (mccormick, 2)
}

nombre_funcion = st.selectbox("Selecciona la función objetivo:", list(funciones.keys()))
funcion_objetivo, dimensiones = funciones[nombre_funcion]

sigma = st.slider("Sigma (desviación estándar del paso aleatorio)", 0.01, 1.0, 0.1, step=0.01)
iteraciones = st.number_input("Número de iteraciones", min_value=10, max_value=5000, value=1000, step=10)

if "x0" not in st.session_state:
    st.session_state.x0 = float(np.random.uniform(-5, 5))
if "x1" not in st.session_state:
    st.session_state.x1 = float(np.random.uniform(-5, 5))

st.markdown("### Punto inicial")
x0 = st.number_input("x₀", value=st.session_state.x0, key="x0_input")
x1 = st.number_input("x₁", value=st.session_state.x1, key="x1_input")

if st.button("▶️ Ejecutar algoritmo"):
    punto_inicial = [x0, x1]

    buscador = BuscadorAleatorio(funcion_objetivo, punto_inicial, sigma=sigma, iteraciones=iteraciones)
    mejor_punto, mejor_valor = buscador.ejecutar()

    st.success(f"✅ Mejor punto encontrado: {np.round(mejor_punto, 6)}")
    st.info(f"📉 Valor mínimo aproximado: {mejor_valor:.6f}")

    buscador.graficar(f"Recorrido - {nombre_funcion}")
