from __future__ import annotations
from typing import Union, Optional
import math
import random as r
import numpy as np
"""from . import vector
from . import utils"""


class Matrix(list[list[float]]):
	"""Initialises a Matrix that can be used for numerous things

Parameters
----------
rowcols (Union[tuple, list]) : The how many rows and columns are in the matrix.

Returns
----------
Matrix: A 2D array of elements.

Methods
----------
fill(val: Union[int, float]) -> None

 	Fill the Matrix with a specified value.

set_value(row: int, col: int, n: Union[int, float]) -> None

	Set the value at a specified row and column.

get_value(row: int, col: int) -> Union[int, float]

	Gets the value at a specified row and column.

get_shape() -> tuple[int, int]

	Get the shape of the Matrix.

transpose() -> None

	Transpose the Matrix in-place.

flatten() -> list
	Flattens the Matrix into a 1-Dimensional array.

cumsum(axis: Optional[int, None]) -> list | Matrix

	Calculates the sumulative sum along a specified axis.

\_\_hash\_\_() -> int
	Calculates the hash value of the Matrix.

\_\_add\_\_(other: Union[Matrix, int, float]) -> Matrix

	Adds another Matrix or a scalar value to the Matrix.

\_\_sub\_\_(other: Union[Matrix, int, float]) -> Matrix

	Subtracts another Matrix or a scalar value from the Matrix.

\_\_mul\_\_(other: Union[Matrix, int, float]) -> Matrix

	Multiplies another Matrix (dot product) or scalar value with the Matrix.

\_\_abs\_\_() -> float

	Computes the absolute value of the Matrix.

\_\_eq\_\_(other: Union[Matrix, int, float]) -> bool

	Checks if the Matrix is equal to another object.

\_\_neq\_\_(other: Union[Matrix, int, float]) -> bool

	Checks if the Matrix is not equal to another object.

Example
----------
> matrix = Matrix((3, 3)) -> [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

> print(matrix) # Output:\n
0 0 0\n
0 0 0\n
0 0 0
"""

	def __new__(cls, rowcols: tuple | list = None, values: list = None):
		if rowcols is not None:
			return super().__new__(cls, rowcols=rowcols)
		if values is not None:
			return super().__new__(cls, values=values)

	def __init__(self, rowcols: tuple | list = None, values: list = None):
		if rowcols is not None:
			super().__init__([[0] * rowcols[1] for _ in range(rowcols[0])])
			self.shape = self.get_shape()
		if values is not None:
			super().__init__(values)
			self.shape = self.get_shape()

	def __str__(self):
		rows = self.get_shape()[0]
		max = len(str(self.max()))
		result = []
		for row in range(rows):
			result.append("|" + "   ".join(map(lambda el: f"{el:^{max}}", self[row])) +
			              "|\n")
		if len(self) == 1:
			center_space = " " * (len(result[0]) - 5)
		else:
			center_space = " " * (len(result[1]) - 5)
		result.append("+-" + center_space + "-+")
		result.insert(0, "+-" + center_space + "-+\n")
		return "".join(result)

	def __repr__(self):
		return f"{type(self).__name__}(values={super().__repr__()})"

	def rank(self):
		if self.det() != 0 and len(self) == len(self[0]):
			return len(self)
		raise NotImplementedError("Function Not Implemented.")

	def fill(self, val: float):
		"""
		Fill the Matrix with a specified value.

 		Parameters
	 	----------
	 	val (Union[int, float]) : The value to fill the Matrix with.

	 	Examples
	 	----------
	 	matrix = Matrix((3, 3))

		matrix.fill(5) # Result: [[5, 5, 5], [5, 5, 5], [5, 5, 5]]

 		matrix.fill(1) # Result: [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
 		"""
		for i in range(len(self)):
			for j in range(len(self[0])):
				self.set_value(i, j, val)

	def set_value(self, row: int, col: int, n: float):
		"""
    Sets the value at a specified row and column.

    Parameters
		----------
		row (int) : The row index of the element.

		col (int) : The Column Index Of The Element.

 		n (Union[int, float]) : The value to be set.add

		Examples
		----------
		matrix = Matrix((3, 3))

 		matrix.set_value(1, 2, 8) # Result: [[0, 8, 0], [0, 0, 0], [0, 0, 0]]

	 	matrix.set_value(3, 1, 5) # Result: [[0, 8, 0], [0, 0, 0], [5, 0, 0]]
    """
		self[row][
		 col] = n  # Subtracting 1 so if the user inputs 1, the index will be auto set to 0

	def get_value(self, row: int, col: int) -> float:
		"""
		Gets the value at a specified row and column.

		Parameters
		----------
		row (int) : The row index of the element.

		col (int) : The column index of the element.

 		Returns
	 	----------
	 	Union[int, float] : The value of the element.

		Examples
		----------
		matrix -> [[0, 0, 0], [1, 7, 0], [0, 1, 5]]

		print(matrix.get_value(2, 2)) # Output: 7

 		print(matrix.get_value(3, 2)) # Output: 1
		"""
		return self[row][col]

	def random(self, a: int = None, b: int = None):
		if a is None:
			a = 0
		if b is None:
			b = 1
		for i in range(len(self)):
			for j in range(len(self[0])):
				self.set_value(i, j, r.randint(a, b))

	def zeros(self):
		self.fill(0)

	def ones(self):
		self.fill(1)

	def identity(self):
		if self.get_shape()[1] != self.get_shape()[0]:
			raise ValueError("Matrix Needs To Be Square.")
		for i in range(len(self)):
			for j in range(len(self[0])):
				self.set_value(i, j, 0)
				if i == j:
					self.set_value(i, j, 1)

	def scalar(self, val: Union[int, float]):
		if self.get_shape()[1] != self.get_shape()[0]:
			raise ValueError("Matrix Needs To Be Square.")
		for i in range(len(self)):
			for j in range(len(self[0])):
				if i == j:
					self.set_value(i, j, val)

	def get_shape(self) -> tuple:
		"""
		Gets the shape of the Matrix.

 		Returns
	 	----------
	 	shape_tuple : A tuple containing the rows and columns of the Matrix.

		Examples
		----------
		matrix = Matrix((3, 3))

		print(matrix.get_shape()) # Output: (3, 3)

 		matrix = Matrix((2, 7))

		print(matrix.get_shape()) # Output: (2, 7)
 		"""
		return (len(self), len(self[0]))

	def get_size(self):
		return self.get_shape()[0] * self.get_shape()[0]

	def transpose(self):
		"""
		Flips the matrix over its diagonal.

		Examples
		----------
		matrix = Matrix((3, 3))

 		matrix.set_value(1, 3, 6) # Result: [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

	 	matrix.transpose() # Result: [[0, 0, 0], [0, 0, 0], [6, 0, 0]]
		"""
		self[:] = [[self[j][i] for j in range(len(self))]
		           for i in range(len(self[0]))]

	def flatten(self) -> list:
		"""
		Returns a flattened version of the matrix.

		Returns a one line list of all elements in the Matrix.

 		Returns
		----------
 		flattened_matrix: A 1-Dimensional array filled with the values from the original matrix.

		Examples
		----------
		matrix = Matrix((3, 3)) # Result: [[0, 0, 0]. [0, 0, 0], [0, 0, 0]]
	
		matrix.flatten() # Result: [0, 0, 0, 0, 0, 0, 0, 0, 0]
"""
		return [item for row in self for item in row]

	def cumsum(self, axis: Optional[int] = None) -> list | Matrix:
		"""
		Calculate the cumulative sum along a specified axis.

		Parameters
		----------
		axis (int, optional) : The axis along which to compute the Cumulative Sum.
	
			If not specified, the cumsum is calculated over the flattened array

 		Returns
	 	----------
	 	list : If the axis is not specified, returns a flattened array with the calculated cumulative sums.

	 	Matrix : the matrix with the cumulative sums along the specified axis.

		Raises
		----------
		ValueError : Raises if the axis is out of bounds

 		Examples
	 	----------
	 	matrix = Matrix((2, 2))
	 	
	 	matrix.set_value(1, 1, 1), matrix.set_value(1, 2, 2), matrix.set_value(2, 1, 3), matrix.set_value(2, 2, 4)

	 	print(matrix.cumsum()) # Output: [1, 2, 4, 6]
		"""
		if axis is None:
			flattened = self.flatten()
			cumsum = 0
			for i, value in enumerate(flattened):
				cumsum += value
				flattened[i] = cumsum
			return flattened
		elif axis == 0:
			result = Matrix(self.get_shape())
			for j in range(1, self.get_shape()[1] + 1):
				cumsum = 0
				for i in range(1, self.get_shape()[0] + 1):
					cumsum += self.get_value(i, j)
					result.set_value(i, j, cumsum)
			return result
		elif axis == 1:
			result = Matrix(self.get_shape())
			for i in range(1, self.get_shape()[0] + 1):
				cumsum = 0
				for j in range(1, self.get_shape()[1] + 1):
					cumsum += self.get_value(i, j)
					result.set_value(i, j, cumsum)
			return result
		else:
			raise ValueError("Axis Out Of Bounds")

	def get_submatrix(self, current_col: int = 0) -> Matrix:
		if len(self) != len(self[0]):
			raise ValueError("Matrix Must Be Square")
		result = Matrix((self.shape[0] - 1, self.shape[1] - 1))
		for i in range(1, len(self)):
			k = 0
			for j in range(len(self[0])):
				# print(i, j, self[i][j])
				if j != current_col:
					result.set_value(i - 1, k, self.get_value(i, j))
					k += 1

		return result

	def det(self) -> int | float:
		if len(self) != len(self[0]):
			raise ValueError("Matrix Must Be Square")
		if self.shape == (1, 1):
			return self[0][0]

		det = 0
		sign = 1

		for i in range(len(self[0])):
			submatrix = self.get_submatrix(i)

			sub_det = submatrix.det()

			det += sign * (self[0][i] * sub_det)

			sign *= -1

		return det

	def __hash__(self) -> int | float:
		return hash(tuple(map(tuple, self)))

	def __add__(self, other: Matrix | float) -> Matrix:
		if isinstance(other, Matrix):
			if self.get_shape() != other.get_shape():
				raise ValueError(
				 f"Cannot Add Matrix Of Shape {self.get_shape()} To Matrix Of Shape {other.get_shape()}"
				)

			result = Matrix(self.get_shape())
			for i in range(len(self)):
				for j in range(len(self[0])):
					result.set_value(i, j, self.get_value(i, j) + other.get_value(i, j))

			return result
		else:
			result = Matrix(self.get_shape())
			for i in range(len(self)):
				for j in range(len(self[0])):
					result.set_value(i, j, self.get_value(i, j) + other)

			return result

	def __radd__(self, other: Matrix | float) -> Matrix:
		return self + other

	def __iadd__(self, other: Matrix | float) -> Matrix:
		return self + other

	def __sub__(self, other: Matrix | float) -> Matrix:
		if isinstance(other, Matrix):
			if self.get_shape() != other.get_shape():
				raise ValueError(
				 f"Cannot Subtract Matrix Of Shape {self.get_shape()} From Matrix Of Shape {other.get_shape()}"
				)

			result = Matrix(self.get_shape())
			for i in range(len(self)):
				for j in range(len(self[0])):
					result.set_value(i, j, self.get_value(i, j) - other.get_value(i, j))

			return result
		else:

			result = Matrix(self.get_shape())
			for i in range(len(self)):
				for j in range(len(self[0])):
					result.set_value(i, j, self.get_value(i, j) - other)

			return result

	def __isub__(self, other: Matrix | float) -> Matrix:
		return self - other

	def __rsub__(self, other: Matrix | float) -> Matrix:
		return self - other

	def __mul__(self, other: int | float) -> Matrix:
		if isinstance(other, Matrix):
			return self @ other
		result = Matrix(self.get_shape())
		for i in range(len(self)):
			for j in range(len(self[0])):
				result.set_value(i, j, self.get_value(i, j) * other)

		return result

	def __rmul__(self, other: float) -> Matrix:
		return self * other

	def __imul__(self, other: float) -> Matrix:
		return self * other

	def __matmul__(self, other: Matrix):
		if isinstance(other, Matrix):
			if len(self) != len(self[0]):
				raise ValueError("Not A Square Matrix.")
			if len(self[0]) != len(other):
				raise ValueError(
				 f"Cannot Multiply Matrix Of Shape {self.get_shape()} With Matrix Of Shape {other.get_shape()}"
				)

			result = Matrix((len(self), len(other[0])))
			for i in range(len(self)):
				for j in range(len(other[0])):
					dot_product = sum(
					 self.get_value(i, k) * other.get_value(k, j) for k in range(len(other)))
					result.set_value(i, j, dot_product)

			return result
		else:
			return self * other

	def __imatmul__(self, other: Matrix) -> Matrix:
		return self @ other

	def __rmatmul__(self, other: Matrix) -> Matrix:
		return self @ other

	def __pow__(self, power: int) -> Matrix:
		#if power < 0:
		#raise ValueError("Power Must Be Greater Than 0")
		if not isinstance(power, int):
			raise ValueError("Power Must Be An Integer")

		result = Matrix(self.get_shape())
		if power == 0:
			result.fill(1)
		else:
			result = self
			for _ in range(power - 1):
				result *= self

		return result

	def __ipow__(self, power: int) -> Matrix:
		return self**power

	def __rpow__(self, power: int) -> Matrix:
		return self**power

	def __truediv__(self, other: float) -> Matrix:
		if isinstance(other, Matrix):
			raise ValueError("Cannot Divide A Matrix By Another Matrix.")
		result = Matrix(self.get_shape())
		for i in range(len(self)):
			for j in range(len(self[0])):
				result.set_value(i, j, round(self.get_value(i, j) / other, 2))
		return result

	def __itruediv__(self, other: float) -> Matrix:
		return self / other

	def __rtruediv__(self, other: float) -> Matrix:
		return self / other

	def __floordiv__(self, other: float) -> Matrix:
		if isinstance(other, Matrix):
			raise ValueError("Cannot Divide A Matrix By Another Matrix.")
		result = Matrix(self.get_shape())
		for i in range(len(self)):
			for j in range(len(self[0])):
				result.set_value(i, j, self.get_value(i, j) // other)
		return result

	def __rfloordiv__(self, other: float) -> Matrix:
		return self / other

	def __ifloordiv__(self, other: float) -> Matrix:
		return self / other

	def __neg__(self) -> Matrix:
		result = Matrix(self.get_shape())
		for i in range(len(self)):
			for j in range(len(self[0])):
				result.set_value(i, j, self.get_value(i, j) * -1)
		return result

	def __abs__(self) -> float:
		result = 0
		for i in range(len(self)):
			for j in range(len(self[0])):
				result += self.get_value(i, j)**2

		return math.sqrt(result)

	def __eq__(self, other: Matrix | float) -> bool:
		if isinstance(other, Matrix):
			if self.get_shape() != other.get_shape():
				return False
			for i in range(len(self)):
				for j in range(len(self[0])):
					if self[i][j] != other[i][j]:
						return False
			return True
		else:
			return False

	def __neq__(self, other: Matrix | float) -> bool:
		if isinstance(other, Matrix):
			if self.get_shape() != other.get_shape():
				return True
			for i in range(len(self)):
				for j in range(len(self[0])):
					if self[i][j] == other[i][j]:
						return False
			return True
		else:
			return False

	def max(self):
		return max(max(self, key=max))
