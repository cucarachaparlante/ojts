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

class RecocidoSimulado:
    def __init__(self, funcion_objetivo, punto_inicio, sigma=0.1, max_iter=1000, w=20, alpha=0.95):
        self.f = funcion_objetivo
        self.x_actual = np.array(punto_inicio, dtype=float)
        self.sigma = sigma
        self.max_iter = max_iter
        self.w = w
        self.alpha = alpha
        self.historial = []
        self.ruta = []
        self.temperaturas = []

    def tweak(self):
        return self.x_actual + np.random.normal(0, self.sigma, size=len(self.x_actual))

    def optimizar(self):
        mejor = self.x_actual.copy()
        T = 1.0
        
        self.historial.append(self.f(mejor))
        self.ruta.append(mejor.copy())
        self.temperaturas.append(T)

        iteracion = 0
        while iteracion < self.max_iter and T > 1e-8:
            for _ in range(self.w):
                vecino = self.tweak()
                f_vecino = self.f(vecino)
                f_mejor = self.f(mejor)
                
                if f_vecino < f_mejor:
                    mejor = vecino.copy()
                    self.x_actual = vecino.copy()
                else:
                    delta = f_vecino - self.f(self.x_actual)
                    if np.exp(-delta / T) >= np.random.uniform():
                        self.x_actual = vecino.copy()

                self.historial.append(self.f(mejor))
                self.ruta.append(mejor.copy())
                self.temperaturas.append(T)

            T *= self.alpha
            iteracion += 1

        return mejor, self.f(mejor)

    def mostrar_grafica(self, titulo="Recorrido Recocido Simulado"):
        puntos = np.array(self.ruta)
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(puntos[:, 0], puntos[:, 1], marker='o', linestyle='-', markersize=2, color='purple', label='Ruta')
        ax.scatter(puntos[0, 0], puntos[0, 1], color='limegreen', s=50, label='Inicio')
        ax.scatter(puntos[-1, 0], puntos[-1, 1], color='crimson', s=50, label='Fin')
        ax.set_title(titulo)
        ax.set_xlabel("x₁")
        ax.set_ylabel("x₂")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

st.title("🔥 Recocido Simulado (Simulated Annealing)")

st.markdown("""
El **recocido simulado** es un algoritmo de optimización inspirado en el proceso físico de enfriamiento de metales. 

A partir de una solución inicial, el algoritmo explora su vecindario generando soluciones aleatorias. 
A diferencia de otros métodos, permite aceptar soluciones peores de manera controlada, con el fin de escapar de óptimos locales. 
Esta aceptación se regula mediante una **"temperatura"** que disminuye gradualmente con el tiempo.

Cuando la temperatura es alta, hay mayor probabilidad de aceptar soluciones peores; a medida que la temperatura disminuye, el algoritmo se vuelve más estricto.  
Es especialmente útil en espacios de búsqueda complejos donde abundan los mínimos locales..
""")


nombre_funcion = st.selectbox("Selecciona la función objetivo:", list(funciones.keys()))
funcion_objetivo = funciones[nombre_funcion]

col1, col2 = st.columns(2)
with col1:
    sigma = st.slider("Sigma (variación aleatoria)", 0.01, 1.0, 0.1, step=0.01)
    alpha = st.slider("Alpha (enfriamiento)", 0.80, 0.99, 0.95, step=0.01)
with col2:
    max_iter = st.number_input("Iteraciones máximas", 100, 5000, 500, step=100)
    w = st.number_input("Vecinos por iteración (w)", 1, 100, 20)

if "x0" not in st.session_state:
    st.session_state.x0 = float(np.random.uniform(-5, 5))
if "x1" not in st.session_state:
    st.session_state.x1 = float(np.random.uniform(-5, 5))

st.markdown("### Punto inicial")
x0 = st.number_input("x₀", value=st.session_state.x0, key="x0_input")
x1 = st.number_input("x₁", value=st.session_state.x1, key="x1_input")

if st.button("▶️ Ejecutar Recocido Simulado"):
    punto_inicio = [x0, x1]
    algoritmo = RecocidoSimulado(funcion_objetivo, punto_inicio, sigma=sigma, max_iter=max_iter, w=w, alpha=alpha)
    mejor_punto, mejor_valor = algoritmo.optimizar()

    st.success(f"📍 Mejor punto encontrado: {np.round(mejor_punto, 6)}")
    st.info(f"🔽 Valor mínimo aproximado: {mejor_valor:.6f}")

    algoritmo.mostrar_grafica(f"Recorrido - {nombre_funcion}")
