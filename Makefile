HEIGHT = 100  
WIDTH = 100  
DENSITY = 63   
ITERATIONS = 11  
SEED = 1100011  
ANIMATE = 1
PROB_ITEM = 0.3
PROB_ENEMY = 0.01


environment:
	conda env create -n ca-map -f environment.yml

simple_map:
	python src/simple_map.py --height $(HEIGHT) --width $(WIDTH) --density $(DENSITY) --iterations $(ITERATIONS) --seed $(SEED) --animate $(ANIMATE)

connect_map:
	python src/simple_map_connected.py --height $(HEIGHT) --width $(WIDTH) --density $(DENSITY) --iterations $(ITERATIONS) --seed $(SEED) --animate $(ANIMATE)

enhanced_map:
	python src/simple_map_w_items.py --height $(HEIGHT) --width $(WIDTH) --density $(DENSITY) --iterations $(ITERATIONS) --seed $(SEED) --prob_item $(PROB_ITEM) --prob_enemy $(PROB_ENEMY) --animate $(ANIMATE)

complete_map:
	python src/simple_map_spawn_exit.py --height $(HEIGHT) --width $(WIDTH) --density $(DENSITY) --iterations $(ITERATIONS) --seed $(SEED) --prob_item $(PROB_ITEM) --prob_enemy $(PROB_ENEMY)

game:
	python src/pygame_game.py --height $(HEIGHT) --width $(WIDTH) --density $(DENSITY) --iterations $(ITERATIONS) --seed $(SEED) --prob_item $(PROB_ITEM) --prob_enemy $(PROB_ENEMY)

clean:
	rm figs/animation/*
