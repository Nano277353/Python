import streamlit as st
import pandas as pd
import numpy as np
from collections import deque
import time
import re
from maze_solver import MAZE, START, END, solve_maze_bfs

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


def solve_bfs(maze, start, end):
    start_time = time.time()
    is_np = hasattr(maze, 'shape')

    def is_free(r, c):
        if is_np:
            return 0 <= r < maze.shape[0] and 0 <= c < maze.shape[1] and maze[r, c] != 1
        else:
            return 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] != 1

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == end:
            return path, time.time() - start_time
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if is_free(nr, nc) and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))

    return None, 0


def solve_dfs(maze, start, end):
    start_time = time.time()
    is_np = hasattr(maze, 'shape')

    def is_free(r, c):
        if is_np:
            return 0 <= r < maze.shape[0] and 0 <= c < maze.shape[1] and maze[r, c] != 1
        else:
            return 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] != 1

    stack = [(start, [start])]
    visited = {start}

    while stack:
        (r, c), path = stack.pop()          
        if (r, c) == end:
            return path, time.time() - start_time
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if is_free(nr, nc) and (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append(((nr, nc), path + [(nr, nc)]))

    return None, 0


st.sidebar.header("Opciones")

modo = st.sidebar.selectbox("Fuente del laberinto", ["Laberinto predefinido", "Cargar archivo .txt"])
algorithm = st.sidebar.selectbox("Algoritmo", ["BFS", "DFS", "A* (no implementado)"])

maze_actual = None
start_actual = None
end_actual = None

if modo == "Laberinto predefinido":
    maze_actual = MAZE
    start_actual = START
    end_actual = END
    render_maze(maze_actual, start=start_actual, end=end_actual)

else:
    archivo = st.sidebar.file_uploader("Sube tu archivo .txt", type=["txt"])

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
            maze_np[maze_np == 2] = 0
            maze_np[maze_np == 3] = 0
            maze_actual  = maze_np
            start_actual = (int(p2[0][0]), int(p2[1][0]))
            end_actual   = (int(p3[0][0]), int(p3[1][0]))
            render_maze(maze_actual, start=start_actual, end=end_actual)
        else:
            st.warning("El archivo debe contener un '2' (inicio) y un '3' (fin).")
    else:
        st.sidebar.info("Esperando archivo .txt...")

solve_button = st.sidebar.button("Resolver Laberinto")

if solve_button and maze_actual is not None:
    if algorithm == "BFS":
        path, tiempo = solve_bfs(maze_actual, start_actual, end_actual)
    elif algorithm == "DFS":
        path, tiempo = solve_dfs(maze_actual, start_actual, end_actual)
    else:
        path = None
        st.warning(f"El algoritmo {algorithm} aún no está implementado.")

    if path:
        st.success(f"¡Camino encontrado con {algorithm}!")
        col1, col2 = st.columns(2)
        col1.metric("Casillas recorridas", len(path))
        col2.metric("Tiempo", f"{tiempo:.6f} s")
        render_maze(maze_actual, path=path, start=start_actual, end=end_actual)
    elif path is not None:
        st.error("No se encontró un camino.")