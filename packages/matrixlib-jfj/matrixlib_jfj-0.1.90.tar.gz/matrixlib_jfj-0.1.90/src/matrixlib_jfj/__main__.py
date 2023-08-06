from __future__ import annotations
import matrix, vector, utils

if __name__ == "__main__":
	matrix1 = matrix.Matrix(None, [
		[1, 2, 3, 4],
		[5, 6, 7, 8],
		[9, 10, 11, 12],
		[13, 14, 15, 16]
	])

	print(matrix1, end="\n\n")

	matrix1.transpose()