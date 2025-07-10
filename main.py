import streamlit as st

st.markdown("""
    <style>
        body {
            background-color: #f7f9fb;
            color: #333;
        }
        .title-container {
            text-align: center;
            padding: 2rem 0 0 0;
        }
        .title-text {
            font-size: 3em;
            font-weight: bold;
            color: #205375;
        }
        .subtitle-text {
            font-size: 1.5em;
            color: #41729F;
        }
        .highlight-box {
            background-color: #eaf2fb;
            padding: 1rem;
            border-radius: 10px;
            margin: 2rem 0;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="title-container">
        <div class="title-text">🚀 Explorador de Métodos de Optimización</div>
        <div class="subtitle-text">Visualiza, analiza y comprende los algoritmos fundamentales</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="highlight-box">
    <h3>🔎 ¿Qué es esta aplicación?</h3>
    <p>Este proyecto te ofrece una forma interactiva de estudiar métodos de optimización clásicos y modernos.
    Está diseñado especialmente para estudiantes de ingeniería, matemáticas aplicadas e inteligencia artificial.</p>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<p>📌 A lo largo de las páginas podrás:</p>
<ul>
    <li>Visualizar paso a paso cómo se comporta cada método</li>
    <li>Ajustar parámetros y observar el efecto en tiempo real</li>
    <li>Comparar funciones objetivo con diferentes dificultades</li>
</ul>
""", unsafe_allow_html=True)

st.markdown("## 🎯 Filosofía del proyecto")
st.info("""
Esta plataforma nació del deseo de hacer más accesible el aprendizaje de algoritmos matemáticos. 
Cada método aquí presentado no es solo un bloque de código, sino una historia visual de cómo resolver problemas reales.
""")


st.markdown("## 🔧 Funcionalidades principales")
st.success("""
✅ Interfaz limpia y accesible  
✅ Parámetros configurables  
✅ Gráficos en tiempo real  
✅ Ideal para estudiantes y profesores  
✅ Basado en Python y Streamlit
""")

st.markdown("## 👥 Créditos")
st.write("""
**Autor:** Carlos Einar Vidaña Huesca [Proyecto de Optimización]  \n
**Universidad:** Universidad de Xalapa \n
**Año:** 2025  
""")

with st.sidebar:
    st.header("🧭 Navegación") 
    st.page_link("pages/1Busqueda_exhaustiva.py", label="🔍 Búsqueda Exhaustiva")
    st.page_link("pages/2FaseDeAcotamiento.py", label="📏 Fase de Acotamiento")
    st.page_link("pages/3Eliminacion_De_Regiones.py", label="🗂️ Métodos de eliminación de regiones")
    st.page_link("pages/4Intervalos_Mitad.py", label="✂️ Intervalos por la mitad")
    st.page_link("pages/5Fibonacci.py", label="🔢 Fibonacci")
    st.page_link("pages/6Busqueda_dorada.py", label="🌟 Búsqueda Dorada")
    st.page_link("pages/7Newton_Raphson.py", label="📉 Newton-Raphson")
    st.page_link("pages/8Biseccion.py", label="🪓 Bisección")
    st.page_link("pages/9Secante.py", label="➗ Secante")
    st.page_link("pages/10Busqueda_unidireccional.py", label="🚶‍♂️ Búsqueda unidireccional")
    st.page_link("pages/11Caminata_aleatoria.py", label="🚶 Caminata aleatoria")
    st.page_link("pages/12Hill_Climbing.py", label="⛰️ Hill Climbing")
    st.page_link("pages/13Simulated_annealling.py", label="🔥 Recocido Simulado")
    st.page_link("pages/14Nelder_Mead.py", label="🔺 Nelder-Mead")
    st.page_link("pages/15Hooke_Jeeves.py", label="🧭 Hooke Jeeves")
    st.page_link("pages/16Metodos_De_Gradiente.py", label="📈 Métodos basados en gradiente")
    st.page_link("pages/17Cauchy.py", label="🎯 Método de Cauchy")
    st.page_link("pages/18Newton.py", label="⚙️ Método de Newton")

