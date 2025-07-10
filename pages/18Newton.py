import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
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
    return A * len(x) + sum(xi**2 - A * np.cos(2 * np.pi * xi) for xi in x)

def rosenbrock(x):
    return sum(100 * (x[i+1] - x[i]**2)**2 + (1 - x[i])**2 for i in range(len(x) - 1))

def ackley(x):
    a, b, c = 20, 0.2, 2 * np.pi
    d = len(x)
    sum1 = sum(xi**2 for xi in x)
    sum2 = sum(np.cos(c * xi) for xi in x)
    return -a * np.exp(-b * np.sqrt(sum1 / d)) - np.exp(sum2 / d) + a + np.exp(1)

def sphere(x):
    return sum(xi**2 for xi in x)

def beale(x):
    x1, x2 = x[0], x[1]
    return ((1.5 - x1 + x1*x2)**2 +
            (2.25 - x1 + x1*x2**2)**2 +
            (2.625 - x1 + x1*x2**3)**2)

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

class Optimizador:
    def __init__(self, funcion, epsilon1=1e-3, epsilon2=1e-3, max_iter=100):
        self.funcion = funcion
        self.epsilon1 = epsilon1
        self.epsilon2 = epsilon2
        self.max_iter = max_iter
        self.ruta = []

    def gradiente(self, x, h=1e-6):
        grad = np.zeros_like(x)
        for i in range(len(x)):
            x_plus = x.copy()
            x_minus = x.copy()
            x_plus[i] += h
            x_minus[i] -= h
            grad[i] = (self.funcion(x_plus) - self.funcion(x_minus)) / (2 * h)
        return grad

    def hessiano(self, x, delta=1e-5):
        fx = self.funcion(x)
        N = len(x)
        H = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                if i == j:
                    xp = x.copy()
                    xnn = x.copy()
                    xp[i] += delta
                    xnn[i] -= delta
                    H[i, j] = (self.funcion(xp) - 2 * fx + self.funcion(xnn)) / (delta**2)
                else:
                    xpp = x.copy(); xpn = x.copy()
                    xnp = x.copy(); xnn = x.copy()
                    xpp[i] += delta; xpp[j] += delta
                    xpn[i] += delta; xpn[j] -= delta
                    xnp[i] -= delta; xnp[j] += delta
                    xnn[i] -= delta; xnn[j] -= delta
                    H[i, j] = (self.funcion(xpp) - self.funcion(xpn) - self.funcion(xnp) + self.funcion(xnn)) / (4 * delta**2)
        return H

class NewtonOptimizer(Optimizador):
    def optimizar(self, x_inicial):
        xk = x_inicial
        k = 0
        self.ruta.append(xk.copy())

        while True:
            grad = self.gradiente(xk)
            hess = self.hessiano(xk)

            if np.linalg.norm(grad) < self.epsilon1 or k > self.max_iter:
                break

            try:
                hess_inv = np.linalg.inv(hess)
                xk1 = xk - hess_inv @ grad
            except np.linalg.LinAlgError:
                st.warning("⚠️ Hessiano no invertible. Se usó paso pequeño en dirección del gradiente.")
                xk1 = xk - 0.01 * grad

            if np.linalg.norm(xk1 - xk) / (np.linalg.norm(xk) + 1e-10) < self.epsilon2:
                break

            xk = xk1
            self.ruta.append(xk.copy())
            k += 1

        return xk

st.title("🔎 Método de Newton")

st.markdown(r"""
El **método de Newton** es una técnica de optimización basada en el uso de derivadas, que busca encontrar mínimos locales de una función de manera rápida y precisa.

Este método utiliza tanto la primera como la segunda derivada de la función para calcular la dirección y el tamaño del paso hacia el mínimo.  
En cada iteración, se aplica la fórmula:

$$
x_{n+1} = x_n - \frac{f'(x_n)}{f''(x_n)}
$$

Al aprovechar la curvatura de la función (segunda derivada), el método puede converger en pocas iteraciones si el punto inicial está cerca del mínimo.  
Sin embargo, requiere que la función sea dos veces diferenciable y que la segunda derivada no sea cero.
""")



funcion_nombre = st.selectbox("Selecciona la función objetivo", list(funciones.keys()))
funcion_obj = funciones[funcion_nombre]

col1, col2 = st.columns(2)
with col1:
    epsilon1 = st.number_input("Tolerancia gradiente (ε₁)", 1e-6, 1e-1, value=0.001, format="%.6f")
    max_iter = st.number_input("Máx. iteraciones", 10, 1000, value=100)
with col2:
    epsilon2 = st.number_input("Tolerancia cambio relativo (ε₂)", 1e-6, 1e-1, value=0.001, format="%.6f")

if "x0" not in st.session_state:
    st.session_state.x0 = float(np.random.uniform(-5, 5))
if "x1" not in st.session_state:
    st.session_state.x1 = float(np.random.uniform(-5, 5))

st.markdown("### Punto inicial")
x0 = st.number_input("x₀", value=st.session_state.x0, key="x0_input")
x1 = st.number_input("x₁", value=st.session_state.x1, key="x1_input")

if st.button("▶️ Ejecutar Newton"):
    x_inicial = np.array([x0, x1])
    opt = NewtonOptimizer(funcion_obj, epsilon1=epsilon1, epsilon2=epsilon2, max_iter=max_iter)
    resultado = opt.optimizar(x_inicial)

    st.success(f"📌 Mínimo encontrado en: {np.round(resultado, 6)}")
    st.info(f"Valor de la función: {funcion_obj(resultado):.6f}")

    puntos = np.array(opt.ruta)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(puntos[:, 0], puntos[:, 1], marker='o', linestyle='-', markersize=3, color='blue', label='Recorrido')
    ax.scatter(puntos[0, 0], puntos[0, 1], color='green', s=60, label='Inicio')
    ax.scatter(puntos[-1, 0], puntos[-1, 1], color='red', s=60, label='Fin')
    ax.set_title(f"Trayectoria - {funcion_nombre}")
    ax.set_xlabel("x₀")
    ax.set_ylabel("x₁")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
