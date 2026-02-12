# L-Systems

A Python implementation of [Aristid Lindenmayer](https://en.wikipedia.org/wiki/Aristid_Lindenmayer) systems (L-Systems)
for purely pedagogical reasons.

L-Systems uses Python's [turtle graphics](https://docs.python.org/3/library/turtle.html)
for rendering the L-Systems.

| Example | L-Systems |
| :--: | :--: |
| ![treea](figures/treea.gif) | ![treec](figures/treec.gif) |
| ![treed](figures/treed.gif)  |  ![treef](figures/treef.gif) |

![settings](figures/settings_panel.gif)

## What is an L-System?

_Taken from the [wikipedia](https://en.wikipedia.org/wiki/L-system) article_:

An L-system or Lindenmayer system is a parallel [rewriting system](https://en.wikipedia.org/wiki/Rewriting) and a
type of [formal grammar](https://en.wikipedia.org/wiki/Formal_grammar).

An L-system consists of an **alphabet** of symbols that can be used to make strings, a collection of **production** rules that
expand each symbol into some larger string of symbols, an initial "**axiom**" string from which to begin construction, and
a mechanism for translating the generated strings into geometric structures.

L-systems were introduced and developed in 1968 by Aristid Lindenmayer, a Hungarian theoretical biologist and botanist at the University of Utrecht.
Lindenmayer used L-systems to describe the behaviour of plant cells and to model the growth processes of plant
development. L-systems have also been used to model the morphology of a variety of organisms and can be used to
generate self-similar fractals.

## Prerequisites

- Python 3.12
- [Poetry](https://python-poetry.org/)

On macOS I have to additionally install [python-tk](https://formulae.brew.sh/formula/python-tk@3.12):
```shell
$ brew install python-tk
```

## Installation
To install `L-Systems` run:
```shell
$ poetry install
```

## Run the Tests
To execute all the unit-tests run:
```shell
$ poetry run pytest tests
```

## Build the Documentation
To build and view the project's documentation:
```shell
$ poetry run mkdocs serve
```

## Run the Examples
Example implementations of L-Systems can be found under the `src/examples/` directory.

By default, a `Dragon Curve` is rendered.
Users may select pre-defined examples by selecting `File > Examples`.

All examples have been taken from the book by Przemyslaw Prusinkiewicz, Aristid Lindenmayer –
    [The Algorithmic Beauty of Plants](https://en.wikipedia.org/wiki/The_Algorithmic_Beauty_of_Plants).
```shell
$ poetry run python src/l_system/
```

Following `poetry install` a script entrypoint is provided with `l-system`. For instance,
```shell
$ l-system --help
usage: l-system [-h] [--animate]

Render L-systems with turtle graphics.

options:
  -h, --help     show this help message and exit
  --animate, -a  If provided, animate turtle movement. (default: False)
```

## Licence 
The content of this site is distributed under [MIT NON-AI License](License.md).
