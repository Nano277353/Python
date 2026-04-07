from collections import deque

def encontrar_camino_bfs(grafo, inicio, objetivo):
    # La cola ahora guarda (nodo_actual, camino_recorrido)
    cola = deque([(inicio, [inicio])])
    visitados = {inicio}

    while cola:
        nodo, camino = cola.popleft()

        if nodo == objetivo:
            return camino  # Retorna la lista de nodos del trayecto

        for vecino in grafo.get(nodo, []):
            if vecino not in visitados:
                visitados.add(vecino)
                # Creamos un nuevo camino extendido para el vecino
                cola.append((vecino, camino + [vecino]))

    return None  # Si no hay conexión

# Tu grafo
mi_grafo = {
    'A': ['F', 'E'],
    'B': ['E', 'G'],
    'C': ['F', 'H', 'D'],
    'D': ['C'],
    'E': ['A', 'B'],
    'F': ['A', 'C'],
    'G': ['B'],
    'H': ['C']
}

camino = encontrar_camino_bfs(mi_grafo, 'A', 'G')
print(f"El camino más corto es: {camino}")