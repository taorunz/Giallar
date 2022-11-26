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

from giallar.core.impl.layout import Layout, Permutation, update_layout_with_perm
from giallar.core.impl.coupling import CouplingMap
from giallar.core.impl.qcircuit import QCircuit
from giallar.utility_library.impl import swap_along_a_path
from giallar.core.impl.qgate import QGate
from giallar.core.impl.routing import Routing
from giallar.core.impl.error_handler import raise_error

class BasicSwap(Routing):

    """
    Performs basic swap routing strategy.
    The pass assumes the input circuit is unrolled, thus no multi-qubit gates included.
    """

    def __init__(self, coupling):

        self.coupling = coupling

    def run(self, input_prop):
        
        qcirc = input_prop['circ']
        initial_layout = input_prop['layout']
        print(initial_layout)
        print(self.coupling)

        layout = initial_layout.copy()

        current_perm = Permutation(qcirc.qubits)
        output_prop = input_prop.copy()

        new_qcirc = QCircuit(qcirc.qubits)

        for gate in qcirc.gate_list:
            #@ permutation: current_perm
            #@ layout: layout
            #@ circuit: new_qcirc

            if gate.isMultiQGate():
                raise_error("The input circuit is not unrolled.")
            
            if gate.is2QGate():
                phys0 = layout[gate.qubits[0]]
                phys1 = layout[gate.qubits[1]]
            
                if self.coupling.distance(phys0, phys1) > 1:
                    path = self.coupling.shortest_undirected_path(phys0, phys1)
                    new_qcirc, current_perm = swap_along_a_path(new_qcirc, current_perm, layout, path)
                    # layout = update_layout_with_perm(initial_layout, current_perm)

                new_gate = QGate(gate.name, [current_perm._i2n[gate.qubits[0]], current_perm._i2n[gate.qubits[1]]], param=gate.param)
                new_qcirc = new_qcirc.append(new_gate)

            else:
                # 1q gate
                new_gate = QGate(gate.name, [current_perm._i2n[gate.qubits[0]]], param=gate.param)
                new_qcirc = new_qcirc.append(new_gate)

        output_prop['circ'] = new_qcirc
        output_prop['perm'] = current_perm

        return output_prop
