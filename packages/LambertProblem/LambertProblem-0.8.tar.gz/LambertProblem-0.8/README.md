# LambertProblem
## LambertProblem is a package that contain methods for solving the Lambert Problem in orbital mechanics 

<!-- This are visual tags that you may add to your package at the beginning with useful information on your package --> 
[![version](https://img.shields.io/pypi/v/LambertProblem?color=blue)](https://pypi.org/project/LambertProblem/)
[![downloads](https://img.shields.io/pypi/dw/LambertProblem)](https://pypi.org/project/LambertProblem/)

This package contain some methods for solve the Lambert Problem in orbital mechanics, and also have a class name Ellipse wich calculate the points of an ellipse.

The method LambertProblem solve the Lambert Equation for a value of semi mayor axis or for a value of transfer time. The method requires the distance for the focus to the two points (r1, r2) and the angle between both radio positions. 

The class Ellipse create a ellipse with center in the center of coordinates and parallel to the x axis. The class is initialized with the value of semi mayor axis from the ellipse and the eccentricity or with the semi minor axis. 


<p align="center"><img src="https://solarsystem.nasa.gov/bosf/images/05-Geostationary%20Satellite-STILL-715x415.jpg" alt="Space orbits gif""/></p>

## Download and install

If you are using `PyPI` installation it's as simple as:

```
pip install LambertProblem
```

You can also test the unstable version of the package with:

```
pip install -i https://test.pypi.org/simple/ LambertProblem
```

## Quick start

First, import the package:
```
import LambertProblem 

```

## Code examples

For creating ellipses with semi mayor value and eccentricity: 

```
elipse = LambertProblem.Ellipse(a = 2, e = 0.3)
```
For creating ellipses with semi mayor value and semi minor value: 

```
elipse = LambertProblem.Ellipse(a = 2, b = 1)
```
For solvin the lambert equation given a value of time: 

```
a = LambertProblem.LambertProblem(r1 = 1, r2 = 1.5, theta = 1.309, t = 1.978)
```
For solvin the lambert equation given a value of time: 

```
t1, t2 = LambertProblem.LambertProblem(r1 = 1, r2 = 1.5, theta = 1.309, a = 1.23)
```

Version 0.6:

- six version of the package.

------------

This package has been designed and written by juaniuwu (C) 2023
