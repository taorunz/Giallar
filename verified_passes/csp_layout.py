# Copyright 2019-2020 The CertiQ authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from giallar.core.impl.error_handler import raise_error
from giallar.core.impl.analysis import Analysis
from giallar.core.impl.layout import Layout
import random
from time import time
from constraint import Problem, RecursiveBacktrackingSolver, AllDifferentConstraint

class CSPLayout(Analysis):

    def __init__(self, coupling_map):
        self.coupling_map = coupling_map

    def run(self, input_prop):
        
        qcirc = input_prop['circ']
        layout = self._generate_csp_layout(qcirc)

        input_prop['layout'] = layout

        return input_prop


    def _generate_csp_layout(self, dag):
        qubits = dag.qubits
        cxs = set()

        for gate in dag.two_qubit_ops():
            cxs.add((qubits.index(gate.qargs[0]), qubits.index(gate.qargs[1])))
        edges = set(self.coupling_map.get_edges())

        if self.time_limit is None and self.call_limit is None:
            solver = RecursiveBacktrackingSolver()
        else:
            solver = CustomSolver(call_limit=self.call_limit, time_limit=self.time_limit)

        variables = list(range(len(qubits)))
        variable_domains = list(self.coupling_map.physical_qubits)
        random.Random(self.seed).shuffle(variable_domains)

        problem = Problem(solver)
        problem.addVariables(variables, variable_domains)
        problem.addConstraint(AllDifferentConstraint())  # each wire is map to a single qubit

        if self.strict_direction:

            def constraint(control, target):
                return (control, target) in edges

        else:

            def constraint(control, target):
                return (control, target) in edges or (target, control) in edges

        for pair in cxs:
            problem.addConstraint(constraint, [pair[0], pair[1]])

        solution = problem.getSolution()

        if solution is None:
            stop_reason = "nonexistent solution"
            if isinstance(solver, CustomSolver):
                if solver.time_current is not None and solver.time_current >= self.time_limit:
                    stop_reason = "time limit reached"
                elif solver.call_current is not None and solver.call_current >= self.call_limit:
                    stop_reason = "call limit reached"
        else:
            stop_reason = "solution found"
            self.property_set["layout"] = Layout({v: qubits[k] for k, v in solution.items()})
            for reg in dag.qregs.values():
                self.property_set["layout"].add_register(reg)

        self.property_set["CSPLayout_stop_reason"] = stop_reason