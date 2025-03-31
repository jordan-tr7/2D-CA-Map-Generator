

environment:
	conda env create -n ca-map -f environment.yml

test:
	python src/test.py


clean:
	rm figs/*