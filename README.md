# Python — Academic Projects Collection

A collection of Python projects from my Computer Engineering coursework at Universidad Regiomontana (U-ERRE), covering search algorithms, sorting, and introductory machine learning. Several projects include interactive [Streamlit](https://streamlit.io/) web apps for visualizing how the algorithms work step by step.

> Note: code comments and app interfaces are in Spanish.

## Project Overview

### Graph Search & Maze Solving (BFS)

| File | Description |
|---|---|
| `maze_solver.py` | Core BFS maze-solving module. Defines the maze grid, start/end points, and a `solve_maze_bfs()` function that returns the shortest path. Imported by the visualizer apps. |
| `applaberinto.py` | Streamlit app that visualizes maze-solving algorithms (BFS and priority-queue search) with an animated, emoji-rendered grid. |
| `3.3.py` | Streamlit maze visualizer built on top of `maze_solver.py`, with step-by-step path animation. |
| `BFS3.py` | Command-line BFS solver that loads a maze from a CSV file (`laberinto.csv`) using pandas and prints the path found. |
| `bfs.py` | Streamlit app that applies BFS to a social-network graph, rendered with NetworkX and Matplotlib, with a custom dark UI theme. |
| `buscarcamino.py` | Minimal BFS pathfinding implementation on an adjacency-list graph — the algorithm at its simplest. |
| `laberinto.py` | Maze represented directly as a graph (adjacency list of grid coordinates) solved with BFS. |
| `laberinto.csv` | Sample maze grid (0 = open cell, 1 = wall) used by the CSV-based solvers. |

### Machine Learning (scikit-learn + Streamlit)

| File | Description |
|---|---|
| `tarea2_3.py` | Interactive linear regression app: upload a CSV, choose target and feature columns, train a model, view R² and predictions, and export results. |
| `avance2_2.py` | K-Means clustering app with configurable K, max iterations, and random seed. Includes feature scaling (StandardScaler), silhouette score evaluation, and Matplotlib visualizations. |
| `Anios_Experiencia_Salario.csv` | Sample dataset (years of experience vs. salary) for the regression app. |
| `datos_ejemplo.csv` | Sample dataset for the clustering app. |

### Algorithms

| File | Description |
|---|---|
| `ordenamiento.py` | Merge sort implementation. |

## Getting Started

### Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

> `bfs.py` additionally requires NetworkX: `pip install networkx`

### Running the Streamlit apps

```bash
streamlit run applaberinto.py   # Maze solver visualizer
streamlit run bfs.py            # BFS on a social-network graph
streamlit run tarea2_3.py       # Linear regression
streamlit run avance2_2.py      # K-Means clustering
```

### Running the command-line scripts

```bash
python BFS3.py            # BFS maze solver from CSV
python buscarcamino.py    # BFS pathfinding on a graph
python ordenamiento.py    # Merge sort demo
```

## 🛠️ Tech Stack

- **Python** — core language
- **Streamlit** — interactive web apps
- **pandas / NumPy** — data loading and manipulation
- **scikit-learn** — regression, clustering, metrics
- **Matplotlib / NetworkX** — plotting and graph visualization

## Author

**Nano** — Computer Engineering student at U-ERRE (Monterrey, Mexico)
GitHub: [@Nano277353](https://github.com/Nano277353)
