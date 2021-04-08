#!python3

"""
A valuation matrix is a matrix v in which each row represents an agent, 
   each column represents an object, and v[i][j] is the value of agent i to object j.
It is used as an input to algorithms of fair division with additive valuations,
   both of divisible and of indivisible goods.

Author: Erel Segal-Halevi
Since:  2021-03
"""

import numpy as np
from typing import *

class ValuationMatrix:
	"""
	A valuation matrix is a matrix v in which each row represents an agent, 
		each column represents an object, and v[i][j] is the value of agent i to object j.
	
	It can be initialized by:

	* A 2-dimensional numpy array (np.ndarray);
	* A list of lists;
	* Another ValuationMatrix.

	>>> v = ValuationMatrix([[1,4,7],[6,3,0]])
	>>> v[0,1]
	4
	>>> v[0][1]
	4
	>>> v[0]
	array([1, 4, 7])
	>>> v
	[[1 4 7]
 	 [6 3 0]]
	>>> for agent in v.agents(): print(v[agent])
	[1 4 7]
	[6 3 0]
	>>> v.agent_value_for_bundle(0, [0,2])
	8
	>>> v.agent_value_for_bundle(1, [1,0])
	9
	>>> v.agent_value_for_bundle(1, None)
	0
	>>> v.without_agent(0)
	[[6 3 0]]
	>>> v.without_object(1)
	[[1 7]
 	 [6 0]]
	>>> ValuationMatrix(np.ones([2,3]))
	[[1. 1. 1.]
 	 [1. 1. 1.]]
	"""
	
	num_of_agents:int
	num_of_objects:int

	def __init__(self, valuation_matrix: np.ndarray):
		if isinstance(valuation_matrix,list):
			valuation_matrix = np.array(valuation_matrix)
		elif isinstance(valuation_matrix,ValuationMatrix):
			valuation_matrix = valuation_matrix._v

		self._v = valuation_matrix
		self.num_of_agents = len(valuation_matrix)
		self.num_of_objects = len(valuation_matrix[0])

	def agents(self):
		return range(self.num_of_agents)

	def objects(self):
		return range(self.num_of_objects)

	def __getitem__(self, key):
		if isinstance(key,tuple):
			return self._v[key[0]][key[1]]  # agent's value for a single object
		else:
			return self._v[key]             # agent's values for all objects

	def agent_value_for_bundle(self, agent:int, bundle:List[int])->float:
		if bundle is None:
			return 0
		else:
			return sum([self._v[agent][object] for object in bundle])

	def without_agent(self, agent:int)->'ValuationMatrix':
		"""
		:return a copy of this valuation matrix, in which the given agent is removed.
		"""
		return ValuationMatrix(np.delete(self._v, agent, axis=0))

	def without_object(self, object:int)->'ValuationMatrix':
		"""
		:return a copy of this valuation matrix, in which the given object is removed.
		"""
		return ValuationMatrix(np.delete(self._v, object, axis=1))
	

	def equals(self, other)->bool:
		return np.array_equal(self._v, other._v)

	def __repr__(self):
		return np.array2string (self._v, max_line_width=100)		





if __name__ == '__main__':
	import doctest
	(failures, tests) = doctest.testmod(report=True)
	print("{} failures, {} tests".format(failures, tests))
