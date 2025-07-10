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
def booth(x: np.ndarray) -> float:
    return (x[0] + 2*x[1] - 7)**2 + (2*x[0] + x[1] - 5)**2

def meshdata(x_min, x_max, y_min, y_max, function, n_puntos=200):
    x_vals = np.linspace(x_min, x_max, n_puntos)
    y_vals = np.linspace(y_min, y_max, n_puntos)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.array([function(np.array([x, y])) for x, y in zip(np.ravel(X), np.ravel(Y))])
    Z = Z.reshape(X.shape)
    return X, Y, Z

def movimiento_exploratorio(x, delta, funcion, N):
    xc = np.array(x)
    for i in range(N):
        x_plus = np.array(x)
        x_minus = np.array(x)
        x_plus[i] = x[i] + delta[i]
        x_minus[i] = x[i] - delta[i]
        xs = [x_minus, x, x_plus]
        fx = [funcion(x) for x in xs]
        x = xs[np.argmin(fx)]
    if np.allclose(x, xc):
        return xc, False
    return x, True

def hooke_jeeves(funcion, x0, delta, epsilon=1e-5, alpha=2.0, N=2, max_iter=100):
    x = np.array(x0)
    historial = [x.copy()]
    for _ in range(max_iter):
        xn, mov = movimiento_exploratorio(x, delta, funcion, N)
        if not mov:
            delta = delta / 2.0
            if np.all(delta < epsilon):
                break
        else:
            xp = xn + alpha * (xn - x)
            fxp = funcion(xp)
            fx = funcion(x)
            if fxp < fx:
                x = xp
            else:
                x = xn
        historial.append(x.copy())
    return x, historial

def plotContourWithPath(X, Y, Z, path):
    fig, ax = plt.subplots()
    contour = ax.contourf(X, Y, Z, levels=30, cmap='viridis')
    fig.colorbar(contour, ax=ax)
    path = np.array(path)
    ax.plot(path[:, 0], path[:, 1], marker='o', color='red')
    ax.set_title('GRAFICA DE CONTORNO')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    return fig


st.title("🎯 Optimización con el Método de Hooke-Jeeves")

st.markdown("""
<div style="text-align: justify; font-size: 16px; line-height: 1.6em; color: #333333;">
<p>
El <strong>método de Hooke-Jeeves</strong> es un algoritmo de optimización sin derivadas diseñado para encontrar mínimos locales de funciones multivariables. Su estrategia se basa en la combinación de dos fases complementarias que permiten explorar el entorno de la solución actual y avanzar hacia una mejora continua.
</p>

<p>
Primero, se realiza un <strong>movimiento exploratorio</strong>, en el cual se evalúan pequeñas variaciones sobre cada variable, una a una, buscando una dirección que reduzca el valor de la función objetivo. Si esta fase detecta una mejora, se procede con un <strong>movimiento de patrón</strong>, que da un salto más largo en la dirección encontrada, con la intención de avanzar más rápidamente hacia una mejor solución.
</p>

<p>
Si no se detecta mejora en alguna de las fases, el algoritmo reduce el tamaño de los desplazamientos y repite el proceso, afinando progresivamente la búsqueda. Este mecanismo de exploración local y avance por patrones lo hace especialmente útil cuando la función no es diferenciable, es ruidosa o no se dispone de gradientes..
</p>

<p>
Gracias a su simplicidad y flexibilidad, el método de Hooke-Jeeves se utiliza en una variedad de aplicaciones, particularmente en problemas de baja o media dimensión. En esta interfaz, puedes visualizar cómo evoluciona la búsqueda en función de los parámetros elegidos y cómo el algoritmo converge hacia una solución óptima.
</p>
</div>
""", unsafe_allow_html=True)


st.subheader("Parámetros de entrada")

col1, col2 = st.columns(2)
with col1:
    x0_0 = st.number_input("x0[0] (punto inicial)", value=0.0)
    delta_0 = st.number_input("delta[0] (paso inicial)", value=1.0)
    epsilon = st.number_input("Epsilon (tolerancia)", value=0.001)
with col2:
    x0_1 = st.number_input("x0[1] (punto inicial)", value=0.0)
    delta_1 = st.number_input("delta[1] (paso inicial)", value=1.0)
    alpha = st.number_input("Alpha (factor de patrón)", value=2.0)

max_iter = st.slider("Máximo de iteraciones", 10, 500, 100)

if st.button("Ejecutar Hooke-Jeeves"):
    x0 = [x0_0, x0_1]
    delta = np.array([delta_0, delta_1])
    X, Y, Z = meshdata(-10, 10, -10, 10, booth)

    sol, path = hooke_jeeves(booth, x0, delta, epsilon=epsilon, alpha=alpha, N=2, max_iter=max_iter)
    fig = plotContourWithPath(X, Y, Z, path)

    st.pyplot(fig)

    st.success(f"Punto mínimo encontrado: {np.round(sol, 6)}")
    st.info(f"Valor de la función en el mínimo: {round(booth(sol), 6)}")
