# 🤖 Dynamic Pathfinding Agent

> An interactive AI pathfinding visualizer built with Python & Pygame, demonstrating **A\* Search** and **Greedy Best-First Search (GBFS)** on a dynamic 2D grid.

**Course:** AI2002 – Artificial Intelligence | Assignment 02  
**Student:** Taha Saleem | BSCS-6E

---

## 📸 Preview

| A\* Search (Maze) | Greedy BFS (Clear Grid) |
|---|---|
| 76 nodes visited, optimal path found | 29 nodes visited, fast greedy path |

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Dynamic-Pathfinding-Agent.git
cd Dynamic-Pathfinding-Agent
```

### 2. Install Dependencies

```bash
pip install pygame
```

> **Python 3.12** is required. No other external libraries are needed.

### 3. Run the Application

```bash
python main.py
```

You will be prompted to enter grid dimensions:

```
=== AI2002 Dynamic Pathfinding Agent ===
Enter number of rows    (default 15):
Enter number of columns (default 15):
```

Press **Enter** to use the default 15×15 grid, or type a number between 5 and 30.

---

## 🎮 Controls & GUI Guide

### Sidebar Buttons

| Button | Action |
|---|---|
| **A\* Search** | Select A\* as the active algorithm |
| **Greedy BFS** | Select Greedy Best-First Search |
| **Manhattan** | Use Manhattan distance heuristic |
| **Euclidean** | Use Euclidean distance heuristic |
| **Run Search** | Execute the selected algorithm |
| **Dynamic Mode** | Enable real-time obstacle spawning & replanning |
| **Random Map (30%)** | Generate a random maze with 30% wall density |
| **Clear Grid** | Remove all walls and reset the grid |
| **Reset Visuals** | Clear path/visited highlights, keep walls |

### Mouse Controls

- **Left Click** on any cell → Toggle wall on/off
- Start is fixed at **top-left** (green)
- Goal is fixed at **bottom-right** (red)

### Color Legend

| Color | Meaning |
|---|---|
| 🟩 Green | Optimal path found |
| 🟦 Blue | Visited/expanded nodes |
| 🟨 Yellow | Frontier nodes |
| ⬛ Black | Wall |
| 🟥 Red | Goal cell |

---

## 📁 Project Structure

```
Dynamic-Pathfinding-Agent/
│
├── main.py           # Entry point — prompts grid size, launches GUI
├── visualizer.py     # Pygame GUI, rendering, user input handling
├── algorithms.py     # GBFS and A* implementations + heuristics
├── grid.py           # Grid state, wall management, neighbour queries
├── metrics.py        # Tracks nodes visited, path cost, execution time
└── README.md         # This file
```

---

## 🧠 Algorithms Implemented

### A\* Search
- **Formula:** f(n) = g(n) + h(n)
- **Optimal:** ✅ Yes (with admissible heuristic)
- **Complete:** ✅ Yes
- Best for: guaranteed shortest path, complex mazes

### Greedy Best-First Search (GBFS)
- **Formula:** f(n) = h(n) only
- **Optimal:** ❌ No
- **Complete:** ✅ Yes (with visited set)
- Best for: fast approximate paths in open environments

### Heuristics
- **Manhattan Distance** → `|Δrow| + |Δcol|` — recommended for 4-directional grids
- **Euclidean Distance** → `√(Δrow² + Δcol²)` — weaker estimate, more nodes expanded

---

## 📊 Metrics Panel

After each run, the sidebar displays:

```
Nodes Visited : 76
Path Cost     : 32
Time (ms)     : 1.0
```

---

## ⚙️ Requirements

```
pygame
```

Install with:

```bash
pip install pygame
```

---

## 🔄 Dynamic Mode

Enable **Dynamic Mode** to watch the agent replan in real time:
1. Click **Run Search** to find an initial path
2. Click **Dynamic Mode** — new walls spawn randomly each tick
3. The agent automatically replans around each new obstacle
4. If no path exists, the GUI displays **"No path found!"**

---

## 📝 License

This project is submitted as academic coursework for AI2002 at FAST-NUCES.
