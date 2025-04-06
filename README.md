# 2D-CA-Map-Generator
Project to generate 2D game maps using cellular automata. 

## Steps to Reproduce

You will need Python, and some kind of environment manager: I use [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main). Additionally, Make is used to execute the code in the project:

- **make environment** - this make command creates a conda environment called `ca-map` from `environment.yml`
- **conda activate ca-map** - activates our conda environment
- **make simple_map** - to generate a random noise map and use Cellular Automata to smooth it into a game map. Has optional arguments:
  - `HEIGHT`: to set the number of rows / height of the map.
  - `WIDTH`: to set the number of columns / width of the map.
  - `DENSITY`: to set the density of the starting noise map. For example, DENSITY = 50 would have 50% of the cells on the table black/walls, and 50% of the cells white/floors. 
  - `ITERATIONS`: the number of iterations over which to run the Cellular-Automata based map smoothing procedure. 
  - `SEED`: the seed for random number generation while creating the map.
  - **Example:** to run this command with custom arguments, we could type: `make simple_map HEIGHT=50 WIDTH=50 DENSITY=59 ITERATIONS=10 SEED=42` in the command line.
- **make enhanced_map** - to generate a map using the same procedure as `make simple_map`, but then to apply another Cellular Automata based procedure to add cells representing items and enemies to the generated map. 
  - Has the same optional arguments as `make simple_map`, and has two additional optional arguments.
  - `PROB_ITEM`: a float between 0 - 1, the likelihood of spawning an item in an appropriate cell. 
  - `PROB_ENEMY`: a float between 0 - 1, the likelihood of spawning an enemy in an appropriate cell. 
  - **make clean** - may be used to remove saved images from the `figs` directory.
