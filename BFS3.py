import pandas as pd
from collections import deque
import sys

def cargar_laberinto(ruta_csv):
    df = pd.read_csv(ruta_csv, header=None)
    return df.values.tolist()

def resolver_y_mostrar(matriz, inicio=None, meta=None):
    filas = len(matriz)
    cols = len(matriz[0])

    if inicio is None:
        inicio = (1, 1)
    if meta is None:
        meta = (filas - 2, cols - 2)

    cola = deque([(inicio, [inicio])])
    visitados = {inicio}

    while cola:
        (f, c), camino = cola.popleft()

        if (f, c) == meta:
            print("\n--- CAMINO ENCONTRADO ---")
            for i in range(filas):
                fila_visual = ""
                for j in range(cols):
                    if (i, j) == inicio:    fila_visual += " 🟢 "
                    elif (i, j) == meta:    fila_visual += " 🏆 "
                    elif (i, j) in camino:  fila_visual += " 🔵 "
                    elif matriz[i][j] == 1: fila_visual += " ⬛ "
                    else:                   fila_visual += " ⬜ "
                print(fila_visual)
            print(f"\nLongitud del camino: {len(camino)} pasos")
            return camino

        for df_, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nf, nc = f + df_, c + dc
            if 0 <= nf < filas and 0 <= nc < cols \
               and matriz[nf][nc] == 0 \
               and (nf, nc) not in visitados:
                visitados.add((nf, nc))
                cola.append(((nf, nc), camino + [(nf, nc)]))

    print("No se encontró camino.")
    return None

ruta = sys.argv[1] if len(sys.argv) > 1 else "laberinto.csv"
laberinto = cargar_laberinto(ruta)
resolver_y_mostrar(laberinto)