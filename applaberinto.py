import streamlit as st
import numpy as np
from collections import deque
import heapq
import time
import re
from maze_solver import MAZE, START, END

st.title("Visualizador de Algoritmo de Búsqueda en Laberinto")

def render_maze(maze, path=None, start=None, end=None):
    if path is None:
        path = []
    path_set = set(map(tuple, path))

    display_maze = []
    for r_idx, row in enumerate(maze):
        display_row = []
        for c_idx, col in enumerate(row):
            cell = (r_idx, c_idx)
            if cell == tuple(start):
                display_row.append("🟢")
            elif cell == tuple(end):
                display_row.append("🏆")
            elif cell in path_set:
                display_row.append("🔵")
            elif (hasattr(maze, 'shape') and maze[r_idx, c_idx] == 1) or \
                 (not hasattr(maze, 'shape') and col == 1):
                display_row.append("⬛")
            else:
                display_row.append("⬜")
        display_maze.append("".join(display_row))

    st.markdown("<br>".join(display_maze), unsafe_allow_html=True)


def make_is_free(maze):
    is_np = hasattr(maze, 'shape')
    def is_free(r, c):
        if is_np:
            return 0 <= r < maze.shape[0] and 0 <= c < maze.shape[1] and maze[r, c] != 1
        else:
            return 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] != 1
    return is_free

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def solve_bfs(maze, start, end):
    start_time = time.time()
    is_free = make_is_free(maze)
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == end:
            return path, time.time() - start_time
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if is_free(nr, nc) and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))

    return None, 0


def solve_dfs(maze, start, end):
    start_time = time.time()
    is_free = make_is_free(maze)
    stack = [(start, [start])]
    visited = {start}

    while stack:
        (r, c), path = stack.pop()
        if (r, c) == end:
            return path, time.time() - start_time
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if is_free(nr, nc) and (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append(((nr, nc), path + [(nr, nc)]))

    return None, 0


def solve_astar(maze, start, end):
    start_time = time.time()
    is_free = make_is_free(maze)

    def heuristic(r, c):
        dr = end[0] - r
        dc = end[1] - c
        penalty = 0
        if dr < 0:
            penalty += abs(dr) * 2
        if dc < 0:
            penalty += abs(dc) * 2
        return abs(dr) + abs(dc) + penalty

    heap = [(heuristic(*start), 0, start, [start])]
    visited = {}

    while heap:
        f, g, (r, c), path = heapq.heappop(heap)

        if (r, c) == end:
            return path, time.time() - start_time

        if (r, c) in visited and visited[(r, c)] <= g:
            continue
        visited[(r, c)] = g

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if is_free(nr, nc):
                ng = g + 1
                if (nr, nc) not in visited or visited[(nr, nc)] > ng:
                    nf = ng + heuristic(nr, nc)
                    heapq.heappush(heap, (nf, ng, (nr, nc), path + [(nr, nc)]))

    return None, 0


st.sidebar.header("Opciones")
algorithm = st.sidebar.selectbox("Algoritmo", ["BFS", "DFS", "A*"])

st.sidebar.divider()

st.sidebar.subheader("Laberinto predefinido")
usar_default = st.sidebar.button("Usar laberinto predefinido")

st.sidebar.divider()

st.sidebar.subheader("Cargar tu propio laberinto")
archivo = st.sidebar.file_uploader("Sube tu archivo .txt", type=["txt"])

st.sidebar.divider()
solve_button = st.sidebar.button("▶ Resolver Laberinto", type="primary")

if "maze_actual" not in st.session_state:
    st.session_state.maze_actual  = MAZE
    st.session_state.start_actual = START
    st.session_state.end_actual   = END

if usar_default:
    st.session_state.maze_actual  = MAZE
    st.session_state.start_actual = START
    st.session_state.end_actual   = END

if archivo:
    content = archivo.read().decode("utf-8")
    lines = content.strip().split('\n')

    maze_data = []
    for line in lines:
        row = [int(d) for d in re.findall(r'\d', line)]
        if row:
            maze_data.append(row)

    maze_np = np.array(maze_data)
    p2 = np.where(maze_np == 2)
    p3 = np.where(maze_np == 3)

    if p2[0].size > 0 and p3[0].size > 0:
        start_cargado = (int(p2[0][0]), int(p2[1][0]))
        end_cargado   = (int(p3[0][0]), int(p3[1][0]))
        maze_np[maze_np == 2] = 0
        maze_np[maze_np == 3] = 0

        st.session_state.maze_actual  = maze_np
        st.session_state.start_actual = start_cargado
        st.session_state.end_actual   = end_cargado
    else:
        st.warning("El archivo debe contener un '2' (inicio) y un '3' (fin).")

maze_actual  = st.session_state.maze_actual
start_actual = st.session_state.start_actual
end_actual   = st.session_state.end_actual

render_maze(maze_actual, start=start_actual, end=end_actual)

if solve_button:
    solvers = {"BFS": solve_bfs, "DFS": solve_dfs, "A*": solve_astar}
    path, tiempo = solvers[algorithm](maze_actual, start_actual, end_actual)

    if path:
        st.success(f"¡Camino encontrado con {algorithm}!")
        col1, col2 = st.columns(2)
        col1.metric("Casillas recorridas", len(path))
        col2.metric("Tiempo", f"{tiempo:.6f} s")
        render_maze(maze_actual, path=path, start=start_actual, end=end_actual)
    else:
        st.error("No se encontró un camino.")