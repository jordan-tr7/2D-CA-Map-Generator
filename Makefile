
HEIGHT = 100
WIDTH = 100
DENSITY = 65
ITERATIONS = 12
SEED = 69420
PROB_ITEM = 0.3
PROB_ENEMY = 0.05

environment:
	conda env create -n ca-map -f environment.yml

simple_map:
	python src/simple_2d_map.py --height $(HEIGHT) --width $(WIDTH) --density $(DENSITY) --iterations $(ITERATIONS) --seed $(SEED)

enhanced_map:
	python src/simple_map_w_items.py --height $(HEIGHT) --width $(WIDTH) --density $(DENSITY) --iterations $(ITERATIONS) --seed $(SEED) --prob_item $(PROB_ITEM) --prob_enemy $(PROB_ENEMY)

height_map:
	python src/diamond_square_height_map.py

test:
	python src/test.py

clean:
	rm figs/*
