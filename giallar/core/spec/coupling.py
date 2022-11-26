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

from z3 import *
from giallar.z3_wrapper import *

class Path:
    def __init__(self, length, coup):
        self.path = fresh_array("path", IntSort(), IntSort())
        self.len = length
        self.coup = coup
        certiq_prove(length >= 0, msg="Path precondition")
    def length(self):
        return self.len
    def __getitem__(self, i):
        return self.path[i]

class CouplingMap:
    def __init__(self):
        self.map = fresh_array("coupling", IntSort(), ArraySort(IntSort(), IntSort()))
        i = Int("qubit")
        j = Int("qubit2")
        assertion(ForAll([i,j], self.map[i][j] >= 0))
        assertion(ForAll([i], self.map[i][i] == 0))
        assertion(ForAll([i,j], self.map[i][j] == self.map[j][i]))
    def distance(self, x, y):
        return self.map[x][y]
    def shortest_undirected_path(self, x, y):
        dist = self.distance(x, y)
        path = Path(dist, self)
        i = Int("qubit")
        j = Int("qubit2")
        assertion(ForAll([i,j], Implies(And(0 <= i, i < dist, 0 <= j, j < dist, i != j), 
                                            path[i] != path[j])))
        assertion(ForAll([i], Implies(And(0 <= i, i < dist-1), 
                                        self.distance(path[i], path[i+1]) == 1)))
        assertion(path[0] == x)
        assertion(path[dist-1] == y)
        return path
    def size(self):
        return fresh_int()

def coup_gate(gate, layout, coup):
    p1 = layout.v2p(gate.arg(0))
    p2 = layout.v2p(gate.arg(1))
    return If(gate.is2QGate(), coup.distance(p1, p2) <= 1, True)

def coupling(circuit, layout, coup):
    n = circuit.size()
    i = Int("index")
    return ForAll([i], Implies(And(0 <= i, i < n), coup_gate(circuit[i], layout, coup)))
