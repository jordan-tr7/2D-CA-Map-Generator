import numpy as np
import matplotlib.pyplot as plt



def plot_grid(grid):
    num_rows = grid.shape[0]
    num_cols = grid.shape[1]

    plot = plt.figure()

    #plot.add_axes()

    plt.title = "Map Test"
    plot = plt.imshow(
        grid, cmap = 'Greys', interpolation = 'nearest', origin = 'lower'
    )

    #plt.colorbar(plot)
    
    

    plt.savefig('figs/test.png')

    plt.show()

def main():

    """
    Note: in case we want to change density of the 2D grid, 
    googled the prompt "numpy randint with set probability": 

    Which returned the following code from Google's AI Overview:

    # Generate an array of 10 random integers from the same set and probabilities
    random_ints = np.random.choice([0, 1, 2], size=10, p=[0.2, 0.5, 0.3])
    """
    grid = np.random.randint(0, 2, (100,100))
    print(grid)
    print(grid.shape)

    plot_grid(grid)



if __name__ == "__main__":
    main()
