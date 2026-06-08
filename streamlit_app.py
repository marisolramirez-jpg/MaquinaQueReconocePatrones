import streamlit as st

st.set_page_config(page_title="Laboratorio: Reconocedor de Patrones", layout="centered")

st.title("Práctica 2: Reconocimiento Manual de Patrones ($3 \\times 3$)")
st.write("Modelado manual de una matriz de pesos para la clasificación de la letra 'T'.")

banco_imagenes = [
    {"nombre": "T Estándar (Positiva)", "matriz": [[1,1,1], [0,1,0], [0,1,0]], "es_t": True},
    {"nombre": "T Plana (Positiva)", "matriz": [[1,1,1], [0,1,0], [0,0,0]], "es_t": True},
    {"nombre": "T Con Base (Positiva)", "matriz": [[1,1,1], [0,1,0], [1,1,1]], "es_t": True},
    {"nombre": "Signo Más / Cruz (Negativa)", "matriz": [[0,1,0], [1,1,1], [0,1,0]], "es_t": False},
    {"nombre": "Línea Superior (Negativa)", "matriz": [[1,1,1], [0,0,0], [0,0,0]], "es_t": False},
    {"nombre": "Marco Cuadrado (Negativa)", "matriz": [[1,1,1], [1,0,1], [1,1,1]], "es_t": False}
]

st.sidebar.header("⚙️ Parámetros del Modelo")

umbral = st.sidebar.slider("Umbral de Activación (θ)", min_value=-8, max_value=15, value=4)

st.sidebar.write("---")
st.sidebar.subheader("Pesos de la Matriz ($W$)")

pesos_lista = []
for idx in range(9):
    fila = idx // 3
    col = idx % 3
    valor_defecto = 2 if fila == 0 else (-2 if col != 1 else 3)
    w_input = st.sidebar.slider(f"Peso Píxel [{fila}][{col}]", -5, 5, valor_defecto, key=f"w_{idx}")
    pesos_lista.append(w_input)

matriz_pesos = [pesos_lista[0:3], pesos_lista[3:6], pesos_lista[6:9]]

st.subheader("🔍 Selección de Estímulo Visual")
opciones_Nombres = [img["nombre"] for img in banco_imagenes]
seleccion = st.selectbox("Elige un patrón para evaluar:", opciones_Nombres)

datos_img = next(item for item in banco_imagenes if item["nombre"] == seleccion)
matriz_img = datos_img["matriz"]

st.write("**Matriz de Entrada (X):**")
texto_matriz = ""
for f in matriz_img:
    texto_matriz += f" ` {f[0]} ` | ` {f[1]} ` | ` {f[2]} ` \n\n"
st.markdown(texto_matriz)


acumulador = 0
for i in range(3):
    for j in range(3):
        acumulador += matriz_img[i][j] * matriz_pesos[i][j]

st.subheader("🧮 Resultado del Procesamiento")
st.write(f"La sumatoria ponderada $\\sum (W \\cdot X)$ dio como resultado: **{acumulador}**")

if acumulador >= umbral:
    st.info(f"🟢 **Predicción:** Patrón aceptado como Letra T ({acumulador} $\\ge$ {umbral})")
else:
    st.warning(f"🔴 **Predicción:** Patrón rechazado / No es T ({acumulador} < {umbral})")

st.write("---")
st.subheader("📋 Estado General del Clasificador")
st.write("Validación simultánea de todo el banco de pruebas:")

for img in banco_imagenes:
    neto = sum(img["matriz"][i][j] * matriz_pesos[i][j] for i in range(3) for j in range(3))
    prediccion_t = neto >= umbral
    es_correcto = prediccion_t == img["es_t"]
    
    status = "✅ Éxito" if es_correcto else "❌ Error de Clasificación"
    tipo_detalle = ""
    if not es_correcto:
        tipo_detalle = " (Falso Positivo)" if prediccion_t else " (Falso Negativo)"
        
    st.write(f"- **{img['nombre']}**: Puntaje = `{neto}` | Clasifica como T? -> *{prediccion_t}* | **[{status}{tipo_detalle}]**")