FROM continuumio/miniconda3 AS conda
LABEL Description="ParaView Notebook base container."

SHELL ["/bin/bash", "-c"]

USER root

WORKDIR /root

RUN apt-get update && \
    apt-get install -y --no-install-recommends libgl1-mesa-dev

RUN conda install --quiet --yes -c conda-forge \
    ipywidgets \
    jupyter \
    jupyterlab \
    ipython \
    paraview \
    numpy