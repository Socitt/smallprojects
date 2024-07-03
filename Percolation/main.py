import numpy as np
import matplotlib.pyplot as plt

def create_grid(size, probability):
    grid = np.random.rand(size, size) < probability
    return grid

def percolate(grid):
    size = grid.shape[0]
    percolation_grid = np.zeros_like(grid, dtype=bool)
    
    # Start percolation from the top row
    for i in range(size):
        if grid[0, i]:
            percolate_recursive(grid, percolation_grid, 0, i)
    
    return percolation_grid

def percolate_recursive(grid, percolation_grid, x, y):
    if x < 0 or x >= grid.shape[0] or y < 0 or y >= grid.shape[1]:
        return
    if not grid[x, y] or percolation_grid[x, y]:
        return
    
    percolation_grid[x, y] = True
    percolate_recursive(grid, percolation_grid, x + 1, y)
    percolate_recursive(grid, percolation_grid, x - 1, y)
    percolate_recursive(grid, percolation_grid, x, y + 1)
    percolate_recursive(grid, percolation_grid, x, y - 1)

def visualize(grid, percolation_grid):
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap='gray', interpolation='none')
    plt.imshow(percolation_grid, cmap='Blues', alpha=0.6, interpolation='none')
    plt.title('Percolation Simulation')
    plt.show()

size = 100
probability = 0.6

grid = create_grid(size, probability)
percolation_grid = percolate(grid)


visualize(grid, percolation_grid)
