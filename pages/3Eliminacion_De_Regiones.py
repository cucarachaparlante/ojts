import streamlit as st

st.title("📉 Métodos de Eliminación de Regiones")

st.markdown("""
<style>
.justify { text-align: justify; font-size: 16px; line-height: 1.6em; color: #333333; }
</style>
<div class="justify">
<p>
Los <strong>métodos de eliminación de regiones</strong> son algoritmos clásicos utilizados para encontrar el mínimo de una función continua en un intervalo cerrado. Su objetivo es <strong>reducir progresivamente el tamaño del intervalo</strong> que contiene el mínimo, descartando las regiones que no lo contienen.
</p>

<p>
Estos métodos se caracterizan por no requerir derivadas y por ofrecer una alta estabilidad numérica, lo que los hace ideales para funciones ruidosas, no diferenciables o costosas de evaluar.
</p>

<p>
Durante el proceso, la función se evalúa en ciertos puntos estratégicos del intervalo actual, y con base en los valores obtenidos, se descarta parte del dominio. Esta operación se repite hasta que el intervalo restante sea menor que una tolerancia predefinida \( \epsilon \), lo cual indica que se ha localizado un punto cercano al mínimo.
</p>

<p>
Entre los métodos más conocidos de este tipo se encuentran:
</p>

<p><strong>🔸 Bisección modificada:</strong> divide el intervalo en dos subintervalos desiguales para reducir la función evaluada.</p>
<p><strong>🔸 Método de los puntos medios (intervalos mitad):</strong> evalúa la función en puntos equidistantes para decidir qué mitad eliminar.</p>
<p><strong>🔸 Búsqueda de razón áurea:</strong> utiliza la proporción áurea para ubicar puntos de evaluación y minimizar el número de cálculos.</p>
<p><strong>🔸 Método de Fibonacci:</strong> similar al anterior, pero basado en los números de Fibonacci para garantizar una cantidad fija de evaluaciones.</p>

<p>
Estos métodos son ampliamente utilizados como punto de partida en optimización global, así como en rutinas donde se busca eficiencia y simplicidad sin perder precisión.
</p>

<p>
A continuación, puedes seleccionar cualquiera de estos algoritmos para experimentar su comportamiento y observar cómo se reduce el intervalo de búsqueda paso a paso.
</p>
</div>
""", unsafe_allow_html=True)
