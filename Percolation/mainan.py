import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def create_grid(size, probability):
    grid = np.random.rand(size, size) < probability
    return grid

def percolate_step(grid, percolation_grid, to_visit):
    new_to_visit = set()
    for x, y in to_visit:
        if x < 0 or x >= grid.shape[0] or y < 0 or y >= grid.shape[1]:
            continue
        if not grid[x, y] or percolation_grid[x, y]:
            continue
        percolation_grid[x, y] = True
        new_to_visit.update([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    return new_to_visit

def animate(i, grid, percolation_grid, ax, to_visit_container):
    to_visit = to_visit_container[0]
    if to_visit:
        to_visit_container[0] = percolate_step(grid, percolation_grid, to_visit)
        ax.clear()
        ax.imshow(grid, cmap='gray', interpolation='none')
        ax.imshow(percolation_grid, cmap='Blues', alpha=0.6, interpolation='none')
        ax.set_title(f'Percolation Simulation Step {i}')

def main():
    size = 500
    probability = 0.75


    grid = create_grid(size, probability)
    percolation_grid = np.zeros_like(grid, dtype=bool)

    # Initialize percolation from the top row
    to_visit = set((0, y) for y in range(size) if grid[0, y])
    to_visit_container = [to_visit]  # Use a list to mutate the to_visit set across frames


    fig, ax = plt.subplots(figsize=(10, 10))


    ani = animation.FuncAnimation(
        fig, animate, fargs=(grid, percolation_grid, ax, to_visit_container), 
        frames=100, interval=100, repeat=False)

    plt.show()

if __name__ == "__main__":
    main()



