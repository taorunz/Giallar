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
from copy import deepcopy

class Layout:
    def __init__(self):
        self._p2v = fresh_array("layout_p2v", IntSort(), IntSort())
        self._v2p = fresh_array("layout_v2p", IntSort(), IntSort())
        i = Int("qubit")
        assertion(ForAll([i], self.p2v(self.v2p(i)) == i))
        assertion(ForAll([i], self.v2p(self.p2v(i)) == i))
    def p2v(self, p):
        return self._p2v[p]

    def copy(self):

        l = Layout()
        i = Int("layout_copy")
        assertion(ForAll([i], self.p2v(i) == l.p2v(i)))
        assertion(ForAll([i], self.v2p(i) == l.v2p(i)))

        return l

    def v2p(self, v):
        return self._v2p[v]

    def __getitem__(self, v):
        return self._v2p[v]

    @staticmethod
    def generate_trivial_layout(qubits):
        trivial_layout = Layout()
        i = Int("qubit")
        assertion(ForAll([i], trivial_layout.p2v(i) == i))
        assertion(ForAll([i], trivial_layout.v2p(i) == i))
        return trivial_layout

class Permutation:
    def __init__(self, qubits):
        self._n2i = fresh_array("perm_n2i", IntSort(), IntSort())
        self._i2n = fresh_array("perm_i2n", IntSort(), IntSort())
        i = Int("qubit")
        assertion(ForAll([i], self.n2i(self.i2n(i)) == i))
        assertion(ForAll([i], self.i2n(self.n2i(i)) == i))
        assertion(ForAll([i], self.n2i(i) == i))
        assertion(ForAll([i], self.i2n(i) == i))
    
    def n2i(self, p):
        return self._n2i[p]

    def i2n(self, v):
        return self._i2n[v]

    def swap_now(self, x, y):
        new = deepcopy(self)
        a = new._n2i[x]
        b = new._n2i[y]
        new._i2n = Store(new._i2n, a, y)
        new._i2n = Store(new._i2n, b, x)
        new._n2i = Store(new._n2i, x, b)
        new._n2i = Store(new._n2i, y, a)

        i = Int("qubit")
        assertion(ForAll([i], new.n2i(new.i2n(i)) == i))
        assertion(ForAll([i], new.i2n(new.n2i(i)) == i))

        return new

def update_layout_with_perm(initial_layout, perm):

    l = Layout()
    i = Int('update_layout')
    assertion(ForAll([i], l._v2p[perm._i2n[i]] == initial_layout._v2p[i]))
    assertion(ForAll([i], l._v2p[i] == initial_layout._v2p[perm._i2n[i]]))

    return l
