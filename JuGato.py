import streamlit as st
import random

# --- 1. CONFIGURACIÓN INICIAL Y ESTILOS ---

st.set_page_config(page_title="Juego del Gato", page_icon="🎲")

st.markdown("""
<style>
/* Estilo para las casillas (botones) */
.stButton > button {
    width: 120px;
    height: 120px;
    border: 3px solid #666666;
    font-size: 80px !important;
    line-height: 1;
}
</style>
""", unsafe_allow_html=True)

st.title("🎲 Juego del Gato: Serie de Partidas")

# --- 2. ENTRADAS DEL USUARIO EN LA BARRA LATERAL ---

st.sidebar.header("Configuración de la Serie")
games_to_play_input = st.sidebar.number_input(
    "Número de partidas a jugar:",
    min_value=1,
    max_value=15,
    value=5,
    step=1 # CAMBIO CLAVE: Ajustado a 1 según tu lógica.
)

# --- 3. INICIALIZACIÓN DEL ESTADO DEL JUEGO (SESSION STATE) ---

if 'scores' not in st.session_state:
    st.session_state.scores = {'🟦': 0, '🟥': 0, 'Empates': 0}
    st.session_state.games_played = 0
    st.session_state.board = [['' for _ in range(3)] for _ in range(3)]
    st.session_state.turn = random.choice(['🟦', '🟥'])
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.match_over = False

# CAMBIO CLAVE: Actualizamos el total de partidas en cada rerun del script.
st.session_state.games_to_play = games_to_play_input

# --- 4. LÓGICA DEL JUEGO (FUNCIONES) ---

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != '': return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '': return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '': return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '': return board[0][2]
    if all(cell != '' for row in board for cell in row): return 'Empate'
    return None

def handle_click(row, col):
    if not st.session_state.game_over and st.session_state.board[row][col] == '':
        st.session_state.board[row][col] = st.session_state.turn
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
            st.session_state.games_played += 1
            if winner != 'Empate':
                st.session_state.scores[winner] += 1
            else:
                st.session_state.scores['Empates'] += 1
            
            if st.session_state.games_played >= st.session_state.games_to_play:
                st.session_state.match_over = True
        else:
            st.session_state.turn = '🟥' if st.session_state.turn == '🟦' else '🟦'

def next_round():
    st.session_state.board = [['' for _ in range(3)] for _ in range(3)]
    st.session_state.turn = random.choice(['🟦', '🟥'])
    st.session_state.game_over = False
    st.session_state.winner = None

def new_match():
    st.session_state.scores = {'🟦': 0, '🟥': 0, 'Empates': 0}
    st.session_state.games_played = 0
    # CAMBIO CLAVE: La nueva serie usa el valor actual del selector.
    st.session_state.games_to_play = games_to_play_input
    st.session_state.match_over = False
    next_round()

# --- 5. INTERFAZ DE USUARIO (UI) ---

score1, score2, score3 = st.columns(3)
score1.metric("Puntaje 🟦", st.session_state.scores['🟦'])
score2.metric("Puntaje 🟥", st.session_state.scores['🟥'])
score3.metric("Partidas Jugadas", f"{st.session_state.games_played} / {st.session_state.games_to_play}")

st.markdown("---")

if st.session_state.match_over:
    st.header("🏆 ¡Fin de la Serie! 🏆")
    score_blue = st.session_state.scores['🟦']
    score_red = st.session_state.scores['🟥']
    if score_blue > score_red:
        st.success(f"El jugador 🟦 es el campeón con {score_blue} victorias.")
    elif score_red > score_blue:
        st.success(f"El jugador 🟥 es el campeón con {score_red} victorias.")
    else:
        st.info("La serie ha terminado en empate.")
    st.balloons()
    st.button("Jugar una Nueva Serie", on_click=new_match, use_container_width=True)

elif st.session_state.game_over:
    if st.session_state.winner == 'Empate':
        st.info("¡Partida en empate! 🤝")
    else:
        st.success(f"¡El jugador **{st.session_state.winner}** ha ganado esta partida! 🎉")
    st.button("Siguiente Ronda", on_click=next_round, use_container_width=True)

else:
    st.write(f"Turno del jugador: **{st.session_state.turn}**")

# Dibujar el tablero
for r_idx, row in enumerate(st.session_state.board):
    cols = st.columns(3)
    for c_idx, cell_value in enumerate(row):
        cols[c_idx].button(
            label=cell_value if cell_value else " ",
            key=f'cell_{r_idx}_{c_idx}',
            on_click=handle_click,
            args=(r_idx, c_idx),
            use_container_width=True,
            disabled=st.session_state.game_over
        )