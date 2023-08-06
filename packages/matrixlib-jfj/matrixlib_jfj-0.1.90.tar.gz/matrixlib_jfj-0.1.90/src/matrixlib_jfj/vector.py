from __future__ import annotations
from typing import Any, Union, Optional
import math


class Vector(tuple):

	def __new__(cls, x: Union[int, float], y: Union[int, float]):
		return super().__new__(Vector, (x, y))
