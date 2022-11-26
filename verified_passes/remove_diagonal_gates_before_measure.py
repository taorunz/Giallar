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

from giallar.core.impl.qcircuit import QCircuit, empty_circuit
from giallar.core.impl.qgate import QGate
from giallar.core.impl.transformation import Transformation
from giallar.core.impl.qcircuit import QCircuit, empty_circuit

class RemoveDiagonalGatesBeforeMeasure(Transformation):

    def __init__(self):
        
        pass

    def run(self, input_prop):

        circ = input_prop['circ']
        output_prop = input_prop.copy()

        out_circ = empty_circuit() 
        
        gates_remaining = circ.copy()

        while gates_remaining.size() > 0:
            #@ circuit: out_circ

            gate_index = 0 # start from the first gate of the remaining gates
            gate = gates_remaining[gate_index]
            sucs = gates_remaining.direct_successors(gate_index)
            
            if (gate.isDiagonal() and
                sucs['gates'].isOnlyMeasurements()):

                gates_remaining = gates_remaining.remove(gate_index)

            else:

                out_circ = out_circ.append(gate)
                gates_remaining = gates_remaining.remove(gate_index)


        output_prop['circ'] = out_circ

        return output_prop
