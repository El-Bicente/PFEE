# PFEE: Gradient Vector Fields of Discrete Morse Functions are Minimum Spanning Forest

This project aims to build an end-to-end visualization program that implements the algorithms of the research paper [**Discrete Morse Functions and Watersheds**](https://arxiv.org/abs/2301.03840) and visually proves that the Minimum Spanning Forest (MST) of the dual graph of a simplicial stack (or a discrete Morse function) is equivalent to the Gradient Vector Field (GVF) of the initial function. The solution is built using Python 3, VTK (Visualization Toolkit) and Paraview for the rendering.

IMAGE

---

## Architecture

IMAGE

<details><summary><b>Show CSV Format</b></summary>

Points
```csvpreview
Node Number,X,Y,Z,Weight
int,float,float,float,int
```

Lines
```csvpreview
P1,P2,Weight
Node Number,Node Number,int
```

Triangles
```csvpreview
S1,S2,S3,Weight
Node Number, Node Number, Node Number,int
```
</details>

* Python application which acts as a wrapper for the C++ app and will also show a sequence of all the images given as input and draw all the bounding boxes on them.
* A benchmark highlighting respective speed and compute relevant indicators.

## Installation

Download the python libraries listed in `requirements.txt`.
```bash
$ pip install -r requirements.txt
```

### Python

To run 
```bash
$ python main.py
```

The available options are:
* `-m` `--minimas`: specify the method.

---

> othman.elbaz@epita.fr &nbsp;&middot;&nbsp;
> william.guillet@epita.fr &nbsp;&middot;&nbsp;
> vincent.courty@epita.fr