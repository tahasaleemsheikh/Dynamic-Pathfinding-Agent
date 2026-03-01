from visualizer import Visualizer


def main():
    # Ask user for grid size before launching
    print("=== AI2002 Dynamic Pathfinding Agent ===")
    print("Press Enter to use default 15x15 grid\n")

    try:
        rows = input("Enter number of rows    (default 15): ").strip()
        cols = input("Enter number of columns (default 15): ").strip()
        rows = int(rows) if rows else 15
        cols = int(cols) if cols else 15
    except ValueError:
        print("Invalid input, using default 15x15")
        rows, cols = 15, 15

    # Clamp grid size to reasonable limits
    rows = max(5, min(rows, 30))
    cols = max(5, min(cols, 30))

    print(f"\nLaunching {rows}x{cols} grid...")
    print("Controls:")
    print("  - Click on grid cells to place/remove walls")
    print("  - Use sidebar buttons to select algorithm and heuristic")
    print("  - Click 'Run Search' to find the path")
    print("  - Click 'Dynamic Mode' to enable real-time obstacle spawning")
    print("  - Click 'Random Map' to generate a random maze")
    print("  - Click 'Clear Grid' to reset everything\n")

    app = Visualizer(rows=rows, cols=cols)
    app.run()


if __name__ == "__main__":
    main()