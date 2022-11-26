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

from giallar.core.impl.transformation import Transformation
from giallar.core.impl.qcircuit import QCircuit, empty_circuit
from giallar.core.impl.qgate import Barrier


class BarriersBeforeFinalMeasurements(Transformation):

    def __init__(self):

        pass
        #super().__init__()

    def run(self, input_prop):

        circ = input_prop['circ']
        output_prop = input_prop.copy()

        output_circ = empty_circuit()

        gates_remaining = circ.copy()

        while gates_remaining.size() > 0:
            #@ circuit: output_circ

            gate_index = 0
            gate = gates_remaining[gate_index]

            if (gate.isMeasurement()):

                sucs = gates_remaining.direct_successors(gate_index)

                if (not sucs['if_successful']):

                    output_circ = output_circ.appendBarrier(gate.arg(0))

            output_circ = output_circ.append(gate)
            gates_remaining = gates_remaining.remove(gate_index)
                    

            
        output_prop['circ'] = output_circ

        return output_prop


