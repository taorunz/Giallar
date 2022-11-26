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

class RemoveFinalMeasurements(Transformation):

    def __init__(self):
        
        pass

    def run(self, input_prop):

        circ = input_prop['circ']
        output_prop = input_prop.copy()

        out_circ = empty_circuit()

        gates_remaining = circ.copy()

        while gates_remaining.size() > 0:
            #@ circuit: out_circ
            
            if gates_remaining.start_with_final_measurement():
                # Final measurement
                gates_remaining = gates_remaining.remove(0)

            else:

                out_circ = out_circ.append(gates_remaining[0])
                gates_remaining = gates_remaining.remove(0)


        output_prop['circ'] = out_circ

        return output_prop
