# 2D Game Map Generation with Cellular Automata

--- 

Code to procedurally generate 2D game maps using Cellular Automata and other techniques. Includes capabilities for visualizing the procedural generation in .gif files, and a Pygame implementation that converts the randomly generated maps into a traversable game environemnt. 

**CS7880:** *Special Topics in Theoretical Computer Science*

The Roux Institute - Northeastern University

**Author:** Tristan Jordan

## Required Utilities

---

All dependencies used in this project are free and open-source. A full list is included in `environment.yml`. The main required utilities include [Python](https://www.python.org/downloads/), [Make](https://www.gnu.org/software/make/), [Git](https://git-scm.com/), and [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) (*or some other virtual environment manager*).

## Makefile Instructions for Reproducibility

---

After utilities are installed, the following make commands can be used to run various files in the project:

- **make environment** - this make command creates a conda environment called `ca-map` from `environment.yml`
- **conda activate ca-map** - running this command in the terminal activates our conda environment
- **make game** - if you want to see the final result, running this command will open a Pygame implementation with default arguments. Character movement can be done with WASD keys. 
  - The optional arguments noted in other make commands below can be passed to this command to change the randomly generated game map. 
  - **Example:** running the command `make game SEED=1337` will change the RNG seed but keep other default arguments.
- **make simple_map** - will generate a random noise map and use Cellular Automata to smooth it into a game map. Has optional arguments:
  - `HEIGHT` (**int**): to set the number of rows / height of the map.
  - `WIDTH` (**int**): to set the number of columns / width of the map.
  - `DENSITY` (**int**): to set the density of the starting noise map. For example, DENSITY = 50 would have 50% of the cells in the matrix black/walls, and 50% of the cells white/floors. 
  - `ITERATIONS` (**int**): the number of iterations over which to run the Cellular-Automata based map smoothing procedure. 
  - `SEED` (**int**): the seed for random number generation while creating the map.
  - `ANIMATE` (**int**): 1 to generate a GIF of the map creation, 0 to only save a PNG of the final result
  - **Example:** to run this command with custom arguments, we could type: `make simple_map HEIGHT=50 WIDTH=50 DENSITY=59 ITERATIONS=10 SEED=42 ANIMATE=0` in the command line.
- **make connect_map** - running this command will generate a simple map from a random noise grid, and then connect the disparate rooms on the map. 
  - Has the same optional arguments as `make simple_map`, including the animation parameter.
- **make enhanced_map** - to generate a connected map using the same procedure as `make connect_map`, but then to apply another Cellular Automata based procedure to add cells representing items and enemies to the generated map. 
  - Has the same optional arguments as `make connect_map`, and has two additional optional arguments.
  - `PROB_ITEM`: a float between 0 - 1, the likelihood of spawning an item in an appropriate cell. 
  - `PROB_ENEMY`: a float between 0 - 1, the likelihood of spawning an enemy in an appropriate cell. 
- **make complete_map** - running this command will generate a complete map with connected rooms, items, enemies, and points for player spawn, and level-exit. 
  - Has the same optional arguments as `make enhanced_map`, except this one does not have the ability to `ANIMATE`, it will only save a PNG of the final map. 
- **make clean** - may be used to manually remove all saved images from the `figs/animation` sub-directory. This should be handled by all animation functions, but just a failsafe. 

## Project Layout

---

```
├── environment.yml                 <- yml file with dependencies for conda 
├── Makefile                        <- Makefile with commands for different scripts
├── README.md                       <- You are here
├── assets                          <- This directory contains sprites for Pygame implementation
│   ├── diamond.png                 <- The sprite for the game's diamond nodes.
│   └── etc...                      <- Additional game sprites.
├── figs                            <- This directory stores generated PNG & GIF files of maps.
│   ├── 2d-maps                     <- Sub-directory for simple map pngs
│   ├── 2d-maps-w-items             <- Sub-directory for map with items and enemies pngs.
│   ├── animation                   <- Sub-directory for temp pngs used to animate gifs.
│   ├── connected                   <- Sub-directory for pngs of simple connected maps.
│   ├── gifs                        <- Sub-directory for generated gifs.
│   ├── spawn-points                <- Sub-directory for pngs of maps w/ spawn and exit points.
│   └── etc...                      <- Other generated png's that aren't put in a sub-directory.
├── src                             <- This directory stores all source code.
│   ├── helpers                     <- Sub-directory containing module for helper functions
│   │   ├── __init__.py             <- To make this folder an importable module.
│   │   ├── .gitignore              <- To ignore __pycache__.
│   │   ├── animate_map_creation.py <- Helper functions for creating gif animations.
│   │   └── map_helpers.py          <- Helper functions for procedural map generation.
│   ├── pygame_game.py              <- Script that runs the Pygame implementation.
│   ├── simple_map_connected.py     <- Script for animating maps w/ connected rooms.
│   ├── simple_map_spawn_exit.py    <- Script for generating final maps w/ spawn & exit points.
│   ├── simple_map_w_items.py       <- Script for animating map creation w/ items and enemies.
│   └── simple_map.py               <- Script for animating simple map creation w/ CA rules.
```