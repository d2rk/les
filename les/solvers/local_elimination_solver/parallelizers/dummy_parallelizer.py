# Copyright (c) 2012-2013 Oleksandr Sviridenko
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from les.solvers.local_elimination_solver.parallelizers.parallelizer import Parallelizer
from les.solvers.local_elimination_solver.local_solver import LocalSolverFactory

class DummyParallelizer(Parallelizer):

  def __init__(self):
    Parallelizer.__init__(self)
    self._problems = []

  def put(self, problem):
    self._problems.append(problem)

  def run(self):
    for problem in self._problems:
      solver = self.get_local_solver_factory().build()
      solver.solve(problem)
