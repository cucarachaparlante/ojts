import streamlit as st

st.title("🧭 Métodos de Optimización Basados en Gradiente")

st.markdown("""
<style>
.justify {
    text-align: justify;
    font-size: 16px;
    line-height: 1.7em;
    color: #333333;
}
</style>

<div class="justify">
<p>
Los <strong>métodos de optimización basados en gradiente</strong> son técnicas fundamentales en el análisis numérico y en el aprendizaje automático. Su propósito es encontrar los mínimos (o máximos) de funciones continuas mediante el uso de información derivada: el <strong>gradiente</strong> o vector de derivadas parciales.
</p>

<p>
Estos métodos parten de un punto inicial y se mueven iterativamente en la dirección opuesta al gradiente, ya que este indica el sentido de mayor incremento de la función. Al avanzar en sentido contrario, se busca minimizar la función..
</p>

<p>
La ventaja principal de estos métodos radica en su <strong>velocidad de convergencia</strong>, especialmente cuando la función es suave y diferenciable. Además, su estructura permite aplicarlos en problemas de gran escala, siendo la base de algoritmos modernos como el descenso estocástico y el método Adam.
</p>

<p>
Entre los enfoques más conocidos se encuentran:
</p>

<p><strong>🟦 Descenso del Gradiente (Gradient Descent):</strong> se mueve directamente en la dirección negativa del gradiente, ajustando el tamaño del paso (learning rate) en cada iteración.</p>

<p><strong>🟨 Método de Cauchy:</strong> también conocido como el método del gradiente más rápido, busca un paso óptimo mediante una minimización unidimensional en la dirección del gradiente.</p>

<p><strong>🟧 Método de Newton:</strong> utiliza la segunda derivada (Hessiano) para ajustar la dirección de avance, permitiendo una convergencia cuadrática cerca del mínimo si la matriz es invertible.</p>

<p><strong>🟥 Método quasi-Newton:</strong> construye una aproximación del Hessiano de forma más eficiente, como lo hace el algoritmo BFGS.</p>

<p>
Estos métodos ofrecen un equilibrio entre precisión y rapidez, aunque pueden presentar dificultades si el gradiente es costoso de calcular, si existen múltiples óptimos o si la función tiene valles estrechos o planos.
</p>

<p>
Esta aplicación te permitirá visualizar cómo evolucionan distintas estrategias basadas en gradientes frente a varias funciones objetivo, y cómo cada una ajusta su trayecto hasta alcanzar un punto óptimo.
</p>
</div>
""", unsafe_allow_html=True)
