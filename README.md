# 2D-CA-Map-Generator
Project to generate 2D game maps using cellular automata. 


## Steps to Reproduce

You will need Python, and some kind of environment manager: I use [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main). Additionally, Make is used to execute the code in the project:

- **make environment** - this make command creates a conda environment called `ca-map` from `environment.yml`
- **conda activate ca-map** - activates our conda environment
- **make simple_map** - to generate a random noise map and use Cellular Automata to smooth it into a game map. Has optional arguments:
  - Test
