import streamlit as st

# ---------------------- Estilo personalizado ----------------------
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

# ---------------------- Título ----------------------
st.markdown("""
    <div class="title-container">
        <div class="title-text">🚀 Explorador de Métodos de Optimización</div>
        <div class="subtitle-text">Visualiza, analiza y comprende los algoritmos fundamentales</div>
    </div>
""", unsafe_allow_html=True)

# ---------------------- Sección destacada ----------------------
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

# ---------------------- Filosofía del proyecto ----------------------
st.markdown("## 🎯 Filosofía del proyecto")
st.info("""
Esta plataforma nació del deseo de hacer más accesible el aprendizaje de algoritmos matemáticos. 
Cada método aquí presentado no es solo un bloque de código, sino una historia visual de cómo resolver problemas reales.
""")

# ---------------------- Características ----------------------
st.markdown("## 🔧 Funcionalidades principales")
st.success("""
✅ Interfaz limpia y accesible  
✅ Parámetros configurables  
✅ Gráficos en tiempo real  
✅ Ideal para estudiantes y profesores  
✅ Basado en Python y Streamlit
""")

# ---------------------- Créditos ----------------------
st.markdown("## 👥 Créditos")
st.write("""
**Autor:** Carlos Einar Vidaña Huesca [Proyecto de Optimización]  \n
**Universidad:** Universidad de Xalapa \n
**Año:** 2025  
""")

# ---------------------- Sidebar (NO TOCAR) ----------------------
# Dentro del sidebar (ya lo tienes):

