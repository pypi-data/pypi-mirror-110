<p align="center"><h1>vizcovidfr</h1></p>


## A python package to visualize spatial evolution of Covid19 cases in France

[![Documentation Status](https://readthedocs.org/projects/vizcovidfr/badge/?version=latest)](https://vizcovidfr.readthedocs.io/en/latest/?badge=latest)
![Python package](https://github.com/AmelieVernay/vizcovidfr/workflows/Python%20package/badge.svg?branch=main)
[![PyPI version](https://badge.fury.io/py/vizcovidfr.svg)](https://badge.fury.io/py/vizcovidfr)

The documentation of vizcovidfr is available [here](https://vizcovidfr.readthedocs.io/en/latest/index.html).

<p align="center">
<img src="./doc/source/_static/vizcovidfr_transfer_map.png" style="vertical-align:middle" width="600" height='400' class='center' alt='logo'>
</p>

## Project description

As part of our course [HMMA238](https://github.com/bcharlier/HMMA238) 'Software Development' at the university of Montpellier, we worked on a team project, and the result is a python package that can be installed by entering the following line in a terminal:

```{bash}
$ pip install git+https://github.com/AmelieVernay/vizcovidfr/
```
You can also use the command

```{bash}
$ pip install vizcovidfr==0.0.5
```
but this version might not have the very last changes, even though we are doing our best to maintain it up to date.


The goal of our project was to analyze the spreading of the covid19 disease in France.
The main idea was to provide a python package for Covid data visualization.
The package contains several sub-modules, each of which containing several functions for specific visualization purpose. One should be able to use these by passing arguments corresponding to the desired output. We wanted our package to be easy to use and tried to build a [documentation](https://vizcovidfr.readthedocs.io/en/latest/index.html) as clear and detailed as possible.


We use Covid-related [datasets available on data.gouv.fr](https://www.data.gouv.fr/en/datasets/).

## Oral presentation (due date : April 25, 2021)

Our beamer presentation for **vizcovidfr** is available on GitHub (`./beamer` folder) and [here on YouTube](https://www.youtube.com/watch?v=8RLse3MGTMU).

### Members

- Foux Quentin, quentin.foux@etu.umontpellier.fr
- Llinares Laurent, laurent.llinares@etu.umontpellier.fr
- Nicolas Alexandre, alexandre.nicolas@etu.umontpellier.fr
- Vernay Amelie, amelie.vernay@etu.umontpellier.fr

### Roles

- Foux Quentin: line charts / piecharts / maps (vacmap)
- Llinares Laurent: line charts / bar plots / heatmap
- Nicolas Alexandre: bar plots / regression / prediction
- Vernay Amelie: maps / sparse matrices / plots / time efficiency

- Everyone: module architecture, documentation, unit tests...

## Sources

During our work, we found help on many different places, in addition to our [HMMA238](https://github.com/bcharlier/HMMA238).

#### For the package structure and the documentation

- the package [chaoseverywhere](https://github.com/tanglef/chaoseverywhere) built by some of our predecessors
- this [python-guide](https://docs.python-guide.org/writing/structure/) about packages
- the [Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/quickstart.html) about documentation

#### For the code part

- the documentation of all the packages that figure in the `requirement.txt` file.
- the public platform [stackoverflow](https://stackoverflow.com/) was very helpful.
