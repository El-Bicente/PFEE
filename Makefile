.ONESHELL:

SHELL = /bin/bash
CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate pfee; conda activate pfee;
CONDA_DEACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda deactivate; conda deactivate;
CONDA_CREATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda env create -f environment.yml;
CONDA_ENV_REMOVE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda env remove -n pfee;

install:
	$(CONDA_CREATE)

clean:
	$(CONDA_DEACTIVATE)
	$(CONDA_ENV_REMOVE)

run:
	$(CONDA_ACTIVATE)
	export LD_LIBRARY_PATH=$PVPATH/lib/
	export PYTHONPATH=$PVPATH/lib/python3.7/site-packages/
	jupyter notebook

docker_install:
	docker build -t pfee_base -f base.dockerfile .

docker_build:
	docker build -t bicente/pfee .

docker_run:
	docker run -p 8888:8888 bicente/pfee

docker_push:
	docker login
	docker push bicente/pfee
