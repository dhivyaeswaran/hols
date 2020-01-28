PYTHON = python3
MATLAB = matlab

all: compile run

compile:
		gcc src/kClist.c -O3 -o kClist

run: holh hols

holh:
	$(PYTHON) -m src.enumerate_cliques $(DATASET)
	$(PYTHON) -W ignore -m src.label_homogeneity $(DATASET)

hols:
	$(PYTHON) -m src.construct_clique_matrices $(DATASET)
	$(MATLAB) -nodisplay -nodesktop -nosplash -r "addpath('src/'); grid_search('$(DATASET)'); exit;"
	$(PYTHON) -W ignore -m src.accuracy_vs_parameters $(DATASET)

clean:
	rm -rf results/holh/*
	rm -rf results/hols/*

spotless: clean
	rm -rf data/*/*clique*
	rm -rf kClist
