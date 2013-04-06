#!/usr/bin/env python
#
# -*- coding: utf-8; -*-
#
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

from les.ext.coin import _osi_sym_solver_interface
from les.ext.coin import coin_utils
from les.problems.problem import Problem
from les.solvers.bilp_solver import BILPSolver

class OsiSymSolverInterface(_osi_sym_solver_interface.OsiSymSolverInterface,
                            BILPSolver):
  """This class represents OSI Solver Interface for SYMPHONY."""

  def __init__(self):
    BILPSolver.__init__(self)
    _osi_sym_solver_interface.OsiSymSolverInterface.__init__(self)

  def solve(self):
    self.branch_and_bound()

  def load_problem(self, problem):
    """Loads problem to the solver."""
    if not isinstance(problem, Problem):
      raise TypeError("Problem must be derived from Problem: %s" % type(problem))
    # Setup objective functions

    # XXX: At some point we can not set column type when there is only one
    # column in the problem. Otherwise SYMPHONY crashes with segmentation fault.

    if problem.get_num_cols() > 1:
      for i, coef in enumerate(problem.get_obj_coefs()):
        (p, v) = coef
        col = coin_utils.CoinPackedVector()
        # NOTE: fix coef because of C++ signature
        self.add_col(col, 0., 1., float(v))
        # TODO: set column type
        self.set_integer(i)
    else:
      col = coin_utils.CoinPackedVector()
      self.add_col(col, 0., 1., float(problem.get_obj_coefs().values()[0]))
      self.set_integer(1)
    # Constraints
    for p, row in enumerate(problem.get_cons_matrix()):
      if not row.getnnz():
        continue
      r = coin_utils.CoinPackedVector();
      for i, v in zip(row.indices, row.data):
        r.insert(int(i), float(v))
      # NOTE: fix coef because of C++ signature
      self.add_row(r, "L", float(problem.get_rhs()[p]), 1.)
    # Set objective function sense
    self.set_obj_sense(-1)
