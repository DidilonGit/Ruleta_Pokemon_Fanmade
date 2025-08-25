
# roulette_streamlit.py
# Versión web en Streamlit del generador de Pokémon fanmade por ruletas
import streamlit as st
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ruleta Pokémon", page_icon="🎡")

# --- Inicializar estado ---
if "fase" not in st.session_state:
    st.session_state.fase = 0

if "resultados" not in st.session_state:
    st.session_state.resultados = {}

# --- Opciones en español ---
ruleta_by = [
    "Pokémon normal", "Ultracriatura", "Evolución convergente",
    "Inicial 🔥💧🌿", "Pokémon dios", "Fósil",
    "Pseudo legendario", "Pokémon singular ⭐", "Pokémon legendario", "Pokémon normal"
]

ruleta_many = ["0", "1", "2", "Evolución dividida ⭐"]

ruleta_typing = [
    "Normal", "Fuego", "Agua", "Planta", "Eléctrico", "Hielo", "Lucha",
    "Veneno", "Tierra", "Volador", "Psíquico", "Bicho", "Roca", "Fantasma",
    "Dragón", "Siniestro", "Acero", "Hada", "Sin tipo", "Cósmico"
]

ruleta_pokemon = [
    "Ninguna", "Megaevolución", "Forma adicional", "Movimiento exclusivo",
    "Habilidad exclusiva", "Nueva mecánica", "Corrupto", "Ninguna"
]

# --- Funciones ---
def tirar_ruleta(opciones):
    idx = random.randrange(len(opciones))
    return idx, opciones[idx]

def tirar_tipos():
    primero = random.choice(ruleta_typing)
    if primero == "Sin tipo":
        segundo = random.choice([t for t in ruleta_typing if t != "Sin tipo"])
        return [segundo]
    else:
        segundo = random.choice([t for t in ruleta_typing if t != "Sin tipo" and t != primero])
        return [primero, segundo]

def dibujar_ruleta(opciones, resaltado=None):
    sizes = [1]*len(opciones)
    explode = [0.1 if i in resaltado else 0 for i in range(len(opciones))] if resaltado else [0]*len(opciones)
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=opciones, explode=explode, startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

# --- App ---
st.title("🎡 Generador de Pokémon Fanmade")
fase = st.session_state.get("fase", 0)
resultados = st.session_state.get("resultados", {})

# Botón para reiniciar
if st.button("🔁 Reiniciar"):
    st.session_state.fase = 0
    st.session_state.resultados = {}
    st.rerun()

if fase == 0:
    st.subheader("1. Categoría (BY)")
    if st.button("Tirar ruleta de categoría"):
        idx, resultado = tirar_ruleta(ruleta_by)
        st.session_state.resultados["Categoría"] = resultado
        st.session_state.fase = 1
        st.session_state.last_draw = ("BY", ruleta_by, [idx])
        st.rerun()

elif fase == 1:
    st.subheader("2. Número de formas (MANY)")
    if st.button("Tirar ruleta de formas"):
        idx, resultado = tirar_ruleta(ruleta_many)
        st.session_state.resultados["Formas"] = resultado
        st.session_state.fase = 2
        st.session_state.last_draw = ("MANY", ruleta_many, [idx])
        st.rerun()

elif fase == 2:
    st.subheader("3. Tipos (TYPING)")
    if st.button("Tirar ruleta de tipos"):
        tipos = tirar_tipos()
        st.session_state.resultados["Tipos"] = tipos
        indices = [ruleta_typing.index(t) for t in tipos]
        st.session_state.fase = 3
        st.session_state.last_draw = ("TYPING", ruleta_typing, indices)
        st.rerun()

elif fase == 3:
    st.subheader("4. Mecánica especial (POKEMON)")
    if st.button("Tirar ruleta de mecánica"):
        idx, resultado = tirar_ruleta(ruleta_pokemon)
        st.session_state.resultados["Mecánica"] = resultado
        st.session_state.fase = 4
        st.session_state.last_draw = ("POKEMON", ruleta_pokemon, [idx])
        st.rerun()

elif fase == 4:
    st.success("✅ Has terminado todas las tiradas.")
    r = st.session_state.resultados
    st.markdown("### Resultado final:")
    st.markdown(f"- **Categoría:** {r.get('Categoría', '?')}")
    st.markdown(f"- **Número de formas:** {r.get('Formas', '?')}")
    tipos = r.get("Tipos", [])
    if len(tipos) == 1:
        st.markdown(f"- **Tipo único:** {tipos[0]}")
    elif len(tipos) == 2:
        st.markdown(f"- **Tipos:** {tipos[0]} (principal) / {tipos[1]} (secundario)")
    st.markdown(f"- **Mecánica especial:** {r.get('Mecánica', '?')}")

# Mostrar ruleta gráfica si hubo tirada reciente
if "last_draw" in st.session_state:
    nombre, opciones, indices = st.session_state.last_draw
    st.markdown(f"#### Visualización de la ruleta: {nombre}")
    dibujar_ruleta(opciones, indices)
