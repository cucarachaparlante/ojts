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

def rosenbrock(x: np.ndarray) -> float:
    return np.sum(100*(x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)

def meshdata(x_min, x_max, y_min, y_max, function, n_puntos=200):
    x_vals = np.linspace(x_min, x_max, n_puntos)
    y_vals = np.linspace(y_min, y_max, n_puntos)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.array([function(np.array([x, y])) for x, y in zip(np.ravel(X), np.ravel(Y))])
    Z = Z.reshape(X.shape)
    return X, Y, Z

def createSimplex(x0: np.ndarray, alpha: float, N: int):
    delta1 = ((np.sqrt(N+1) + N - 1) / (N * np.sqrt(2))) * alpha
    delta2 = ((np.sqrt(N+1) - 1) / (N * np.sqrt(2))) * alpha
    xn = [np.array([x0[i] + delta1 if i == j else x0[i] + delta2 for i in range(N)]) for j in range(N)]
    xn.insert(0, x0)
    return np.array(xn)

def terminar(fx, fc, N, epsilon=0.001):
    return np.sqrt(np.sum(((fx - fc)**2)/(N+1))) < epsilon

def plotContourWithSimplex(X, Y, Z, simplex, nuevo_punto=None):
    fig, ax = plt.subplots()
    contour = ax.contourf(X, Y, Z, levels=30, cmap='viridis')
    fig.colorbar(contour, ax=ax)

    for punto in simplex:
        ax.plot(punto[0], punto[1], 'r*', markersize=10)

    if nuevo_punto is not None:
        ax.plot(nuevo_punto[0], nuevo_punto[1], 'bs', markersize=8)

    ax.set_title('GRAFICA DE CONTORNO')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    return fig

st.title("🔻 Optimización con el Método Nelder-Mead")

st.markdown("""
<div style="text-align: justify; font-size: 16px; line-height: 1.6em; color: #333333;">
<p>
El <strong>método de Nelder-Mead</strong>, también conocido como <em>simplex de búsqueda</em>, es una técnica de optimización que no requiere derivadas ni información del gradiente. A diferencia de otros métodos, su estrategia consiste en manipular un conjunto de puntos en el espacio —denominado <strong>simplex</strong>— para explorar progresivamente el entorno y encontrar un mínimo local de una función objetivo.
</p>

<p>
En dos dimensiones, el simplex es un triángulo; en tres, un tetraedro. A lo largo del proceso, el algoritmo evalúa la función en los vértices y transforma este conjunto mediante operaciones geométricas clave: <strong>reflexión</strong> para alejarse del peor punto, <strong>expansión</strong> si el nuevo punto resulta prometedor, <strong>contracción</strong> si no se obtiene mejora significativa, y <strong>reducción</strong> cuando el progreso se detiene.
</p>

<p>
Este método es ampliamente utilizado cuando la función es ruidosa, discontinua o simplemente desconocida. Su simplicidad y flexibilidad lo hacen una opción práctica en muchas aplicaciones, aunque su rendimiento puede verse limitado en problemas de alta dimensión o funciones con múltiples mínimos locales.
</p>

<p>
A continuación, podrás visualizar cómo evoluciona el simplex en cada iteración, acercándose gradualmente a una solución óptima dentro del dominio de la función seleccionada.
</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    x0_0 = st.number_input("x0[0]", value=0.0)
    alpha = st.number_input("Alpha (tamaño simplex)", value=1.0)
    epsilon = st.number_input("Epsilon (criterio de parada)", value=0.001)
with col2:
    x0_1 = st.number_input("x0[1]", value=0.0)
    gamma = st.number_input("Gamma (expansión)", value=1.2)
    beta = st.number_input("Beta (contracción)", value=0.5)

max_iter = st.slider("Máximo de iteraciones", min_value=1, max_value=200, value=100)

if st.button("Ejecutar Nelder-Mead"):
    N = 2
    x0 = np.array([x0_0, x0_1])
    simplex = createSimplex(x0, alpha, N)
    trayectoria = [simplex.copy()]
    final = False
    iteracion = 0

    while not final and iteracion < max_iter:
        fx = np.array([rosenbrock(x) for x in simplex])
        indices = np.argsort(fx)
        i_xl, i_xg, i_xh = indices[0], indices[-2], indices[-1]

        xc = (np.sum(simplex, axis=0) - simplex[i_xh]) / N
        xr = 2 * xc - simplex[i_xh]
        fxr = rosenbrock(xr)
        fxc = rosenbrock(xc)
        xnew = xr

        if fxr < fx[i_xl]:
            xnew = (1 + gamma)*xc - gamma*simplex[i_xh]  
        elif fxr >= fx[i_xh]:
            xnew = (1 - beta)*xc + beta*simplex[i_xh]  
        elif fx[i_xg] < fxr < fx[i_xh]:
            xnew = (1 + beta)*xc - beta*simplex[i_xh] 

        simplex[i_xh] = xnew
        trayectoria.append(simplex.copy())
        final = terminar(fx, fxc, N, epsilon)
        iteracion += 1

    X, Y, Z = meshdata(-2, 2, -1, 3, rosenbrock)
    fig = plotContourWithSimplex(X, Y, Z, simplex)
    st.pyplot(fig)

    mejor = simplex[np.argmin([rosenbrock(x) for x in simplex])]
    st.success(f"Punto mínimo encontrado: {np.round(mejor, 6)}")
    st.info(f"Valor de la función: {round(rosenbrock(mejor), 6)}")
    st.write(f"Iteraciones realizadas: {iteracion}")