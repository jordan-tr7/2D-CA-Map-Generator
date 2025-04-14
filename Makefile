
HEIGHT = 100 #  25
WIDTH = 100 #  25
DENSITY = 65
ITERATIONS = 12 #  3
SEED = 42069
PROB_ITEM = 0.3
PROB_ENEMY = 0.01

environment:
	conda env create -n ca-map -f environment.yml

simple_map:
	python src/simple_2d_map.py --height $(HEIGHT) --width $(WIDTH) --density $(DENSITY) --iterations $(ITERATIONS) --seed $(SEED)

enhanced_map:
	python src/simple_map_w_items.py --height $(HEIGHT) --width $(WIDTH) --density $(DENSITY) --iterations $(ITERATIONS) --seed $(SEED) --prob_item $(PROB_ITEM) --prob_enemy $(PROB_ENEMY)

spawn_map:
	python src/spawn_and_exit_point.py --height $(HEIGHT) --width $(WIDTH) --density $(DENSITY) --iterations $(ITERATIONS) --seed $(SEED) --prob_item $(PROB_ITEM) --prob_enemy $(PROB_ENEMY)

height_map:
	python src/diamond_square_height_map.py

test:
	python src/bfs_test.py

clean:
	rm figs/*
