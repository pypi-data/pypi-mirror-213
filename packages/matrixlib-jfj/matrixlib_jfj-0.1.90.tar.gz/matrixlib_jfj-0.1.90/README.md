# Matrixlib

---
### A basic library for matrix and vector operations. Any feedback is highly encouraged. I enjoy trying to create modules and programs that work with mathematical functions and data. I also like looking into higher end modules and researching the processes and programs they use to perform tasks. Any feedback will be taken and acted upon.
<br>
<br>

# Installation

---
### Use the package manager pip to install matrixlib_jfj.

### Release Versions:

``` bash
pip install matrixlib_jfj
```

### Test Versions:

``` bash
pip install -i https://test.pypi.org/simple matrixlib-jfj
```
<br>
<br>

# General Usage

---
``` python
import matrixlib_jfj as ml

# matrix = ml.matrix.Matrix(rowcols=(x, y) or values=[[nested list(s) with values assigned]]) Initialises the matrix.
Example:
matrix = ml.matrix.Matrix(rowcols=(3, 3))
>>> [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

print(matrix)
    +-       -+
    | 0  0  0 |
>>> | 0  0  0 |
    | 0  0  0 |
    +-       -+

# matrix.random(a, b) Adds random values to the entire matrix
Example:
matrix.random(1, 10)
    +-          -+
    |7    10   7 |
>>> |1    1    7 |
    |10   5    8 |
    +-          -+

# matrix.identity() Creates an identity matrix from an existing square matrix
    +-       -+
    |1   0   0|
>>> |0   1   0|
    |0   0   1|
    +-       -+

### Adding ###
matrix1 = ml.matrix.Matrix(values=[
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

matrix2 = ml.matrix.Matrix(values=[
    [9, 8, 7],
    [6, 5, 4],
    [3, 2, 1]
])

    +-          -+
    |10   10   10|
>>> |10   10   10|
    |10   10   10|
    +-          -+
```
<br>
<br>

# Updates

---
## Update 0.0.7
Added "get_submatrix" function that gets the submatrix of any square matrix, added the "det" function which gets the determinant of a square matrix.

<br>

## Update 0.0.8
Fixed bug where an external program would run when the user of the package would run their own program.
<br>

## Update 0.0.81
Updated README file to reflect certain information.
<br>

## Update 0.0.82
Fixed Type Annotations.
<br>

## Update 0.1.82
Removed Deprecations, Removed functionality in utils.py (Temporary) added better typing, improved cumsum function.
<br>

## Update 0.1.90
Added temporary base case to Matrix.rank() function.
<br>

# Contributing

---
Any and All feedback and help is highly encouraged. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
<br>
<br>

# License

---
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/#)