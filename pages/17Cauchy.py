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
    return A * len(x) + sum([xi**2 - A * np.cos(2 * np.pi * xi) for xi in x])

def rosenbrock(x):
    return sum([100 * (x[i+1] - x[i]**2)**2 + (1 - x[i])**2 for i in range(len(x) - 1)])

def ackley(x):
    a, b, c = 20, 0.2, 2 * np.pi
    d = len(x)
    sum1 = sum([xi**2 for xi in x])
    sum2 = sum([np.cos(c * xi) for xi in x])
    return -a * np.exp(-b * np.sqrt(sum1 / d)) - np.exp(sum2 / d) + a + np.exp(1)

def sphere(x):
    return sum([xi**2 for xi in x])

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

    def gradiente(self, x, h=1e-6):
        grad = np.zeros_like(x)
        for i in range(len(x)):
            x_plus = x.copy()
            x_minus = x.copy()
            x_plus[i] += h
            x_minus[i] -= h
            grad[i] = (self.funcion(x_plus) - self.funcion(x_minus)) / (2 * h)
        return grad

class CauchyOptimizer(Optimizador):
    def regla_eliminacion(self, x1, x2, fx1, fx2, a, b):
        if fx1 > fx2:
            return x1, b
        if fx1 < fx2:
            return a, x2
        return x1, x2

    def w_to_x(self, w, a, b):
        return w * (b - a) + a

    def busqueda_dorada(self, funcion, epsilon, a=0.0, b=1.0):
        PHI = (1 + math.sqrt(5)) / 2 - 1
        aw, bw = 0, 1
        Lw = 1
        while Lw > epsilon:
            w2 = aw + PHI * Lw
            w1 = bw - PHI * Lw
            aw, bw = self.regla_eliminacion(w1, w2, funcion(self.w_to_x(w1, a, b)), 
                                            funcion(self.w_to_x(w2, a, b)), aw, bw)
            Lw = bw - aw
        return (self.w_to_x(aw, a, b) + self.w_to_x(bw, a, b)) / 2

    def optimizar(self, x_inicial):
        ruta = [x_inicial.copy()]
        xk = x_inicial
        k = 0
        while True:
            grad = self.gradiente(xk)
            if np.linalg.norm(grad) < self.epsilon1 or k > self.max_iter:
                break
            def alpha_func(alpha):
                return self.funcion(xk - alpha * grad)
            alpha = self.busqueda_dorada(alpha_func, self.epsilon2)
            xk1 = xk - alpha * grad
            ruta.append(xk1.copy())
            if np.linalg.norm(xk1 - xk) / (np.linalg.norm(xk) + 1e-10) < self.epsilon2:
                break
            xk = xk1
            k += 1
        return xk, ruta

st.title("📉 Método de Cauchy")

st.markdown("""
El **método de Cauchy**, también conocido como **descenso por gradiente**, es una técnica de optimización basada en derivadas que busca minimizar una función moviéndose en la dirección opuesta al gradiente.

En cada iteración, se calcula el gradiente de la función en el punto actual y se da un paso en la dirección negativa de este gradiente.  
El tamaño del paso puede ser fijo o determinarse mediante una búsqueda de línea.

Es un método simple y ampliamente utilizado, especialmente en problemas de optimización diferenciable, aunque puede requerir ajustes en la tasa de aprendizaje para garantizar la convergencia.
""")

funcion_nombre = st.selectbox("Selecciona la función objetivo", list(funciones.keys()))
funcion = funciones[funcion_nombre]

col1, col2 = st.columns(2)
with col1:
    x0 = st.number_input("x₀", value=float(np.random.uniform(-5, 5)))
    x1 = st.number_input("x₁", value=float(np.random.uniform(-5, 5)))
with col2:
    epsilon1 = st.number_input("ε₁ (gradiente)", min_value=1e-6, max_value=0.1, value=0.001, format="%.6f")
    epsilon2 = st.number_input("ε₂ (cambio relativo)", min_value=1e-6, max_value=0.1, value=0.001, format="%.6f")
    M = st.number_input("Máx. iteraciones", min_value=10, max_value=1000, value=100)

if st.button("▶️ Ejecutar Cauchy"):
    optimizador = CauchyOptimizer(funcion, epsilon1=epsilon1, epsilon2=epsilon2, max_iter=M)
    x_ini = np.array([x0, x1])
    minimo, ruta = optimizador.optimizar(x_ini)
    st.success(f"Mínimo encontrado en: {np.round(minimo, 6)}")
    st.info(f"Valor de la función: {funcion(minimo):.6f}")

    puntos = np.array(ruta)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(puntos[:, 0], puntos[:, 1], marker='o', linestyle='-', markersize=3, color='blue', label='Ruta')
    ax.scatter(puntos[0, 0], puntos[0, 1], color='green', s=60, label='Inicio')
    ax.scatter(puntos[-1, 0], puntos[-1, 1], color='red', s=60, label='Fin')
    ax.set_title(f"Trayectoria - {funcion_nombre}")
    ax.set_xlabel("x₀")
    ax.set_ylabel("x₁")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)