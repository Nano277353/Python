from collections import deque

grafo = {
    (0,0): [(0,1),(1,0)],
    (0,1): [(0,0),(1,1)],
    (0,2): [(0,3),(1,2)],
    (0,3): [(0,4)],
    (0,4): [(0,3),(0,5),(1,4)],
    (0,5): [(0,4),(1,5)],

    (1,0): [(0,0)],
    (1,1): [(1,2),(0,1)],
    (1,2): [(1,1),(1,3),(0,2)],
    (1,3): [(1,2),(1,4)],
    (1,4): [(0,4),(1,3),(1,5)],
    (1,5): [(0,5),(1,4)],

    (2,0): [(1,0),(2,1),(3,0)],
    (2,1): [(2,0),(1,1)],
    (2,2): [(2,3),(3,2)],
    (2,3): [(2,2),(2,4)],
    (2,4): [(2,5)],
    (2,5): [(3,5),(1,5)],

    (3,0): [(2,0),(3,1),(4,0)],
    (3,1): [(3,0),(3,2)],
    (3,2): [(3,1),(2,2),(3,3)],
    (3,3): [(3,2),(3,4)],
    (3,4): [(2,4), (4,4)],
    (3,5): [(2,5),(4,5)],

    (4,0): [(4,1)],   # A
    (4,1): [(4,0),(4,2)],   # B
    (4,2): [(4,1),(4,3)],   # C
    (4,3): [(4,2),(4,4)],
    (4,4): [(3,4)],
    (4,5): [(4,4)],
}

def bfs(grafo, inicio, objetivo):
    cola = deque([(inicio, [inicio])])
    visitados = {inicio}

    while cola:
        nodo, camino = cola.popleft()

        if nodo == objetivo:
            return camino

        for vecino in grafo.get(nodo, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, camino + [vecino]))

    return None

inicio   = (4, 0)  # Nodo A
objetivo = (4, 5)  # Salida

camino = bfs(grafo, inicio, objetivo)

if camino:
    print(f"Camino encontrado ({len(camino)-1} pasos):")
    for paso in camino:
        print(f"  {paso}")
else:
    print("No se encontró camino.")