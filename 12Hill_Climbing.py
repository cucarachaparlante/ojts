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
    return A * len(x) + sum([xi**2 - A * np.cos(2 * np.pi * xi) for xi in x])

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

funciones = {
    "Rastrigin": rastrigin,
    "Rosenbrock": rosenbrock,
    "Ackley": ackley,
    "Sphere": sphere,
    "Beale": beale,
    "Booth": booth,
    "Himmelblau": himmelblau,
    "McCormick": mccormick
}

class Explorador:
    def __init__(self, funcion_objetivo, punto_inicio, sigma=0.1, pasos=1000):
        self.f = funcion_objetivo
        self.punto = np.array(punto_inicio, dtype=float)
        self.sigma = sigma
        self.pasos = pasos
        self.historia = []
        self.ruta = []

    def vecino(self):
        return self.punto + np.random.normal(0, self.sigma, size=len(self.punto))

    def optimizar(self):
        actual = self.punto.copy()
        valor = self.f(actual)
        self.historia.append(valor)
        self.ruta.append(actual.copy())

        for _ in range(self.pasos):
            candidato = self.vecino()
            val_candidato = self.f(candidato)

            if val_candidato < valor:
                actual = candidato
                valor = val_candidato

            self.historia.append(valor)
            self.ruta.append(actual.copy())

        return actual, valor

    def mostrar_grafica(self, titulo="Ruta del algoritmo"):
        puntos = np.array(self.ruta)
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(puntos[:, 0], puntos[:, 1], marker='o', linestyle='-', markersize=2, color='teal', label='Ruta')
        ax.scatter(puntos[0, 0], puntos[0, 1], color='limegreen', s=50, label='Inicio')
        ax.scatter(puntos[-1, 0], puntos[-1, 1], color='crimson', s=50, label='Fin')
        ax.set_title(titulo)
        ax.set_xlabel("x₁")
        ax.set_ylabel("x₂")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)


st.title("⛰️ Hill Climbing")

st.markdown("""
El **método de Hill Climbing** es una técnica de optimización iterativa que mejora una solución actual evaluando pequeñas modificaciones aleatorias en sus alrededores (vecindario).

En cada iteración, se genera un nuevo punto cercano al actual y se compara su valor con el anterior. 
Si el nuevo punto ofrece una mejor solución (menor valor de la función objetivo), se actualiza la posición; de lo contrario, se conserva el punto actual.

Es un algoritmo simple y eficiente para problemas donde se puede explorar localmente, pero puede quedarse atrapado en óptimos locales si no se aplican técnicas adicionales como reinicios aleatorios o enfriamiento simulado.
""")


nombre_funcion = st.selectbox("Selecciona la función objetivo:", list(funciones.keys()))
funcion_objetivo = funciones[nombre_funcion]

col1, col2 = st.columns(2)
with col1:
    sigma = st.slider("Sigma (variación aleatoria)", 0.01, 1.0, 0.1, step=0.01)
with col2:
    pasos = st.number_input("Número de pasos", min_value=10, max_value=5000, value=1000, step=10)

if "x0" not in st.session_state:
    st.session_state.x0 = float(np.random.uniform(-5, 5))
if "x1" not in st.session_state:
    st.session_state.x1 = float(np.random.uniform(-5, 5))

st.markdown("### Punto inicial")
x0 = st.number_input("x₀", value=st.session_state.x0, key="x0_input")
x1 = st.number_input("x₁", value=st.session_state.x1, key="x1_input")

if st.button("▶️ Ejecutar Hill Climbing"):
    punto_inicio = [x0, x1]
    optimizador = Explorador(funcion_objetivo, punto_inicio, sigma=sigma, pasos=pasos)
    mejor_punto, mejor_valor = optimizador.optimizar()

    st.success(f"📍 Mejor punto encontrado: {np.round(mejor_punto, 6)}")
    st.info(f"🔽 Valor mínimo aproximado: {mejor_valor:.6f}")
    optimizador.mostrar_grafica(f"Ruta - {nombre_funcion}")
