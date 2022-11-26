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

from giallar.core.impl.layout import Layout, Permutation
from giallar.core.impl.coupling import CouplingMap
from giallar.core.impl.qcircuit import empty_circuit, definition
from giallar.core.impl.qgate import QGate
from giallar.core.impl.transformation import Transformation
from giallar.core.impl.error_handler import raise_error

class Unroller(Transformation):

    def __init__(self):
        pass
        # super.__init__()

    def run(self, input_prop):
        
        qcirc = input_prop['circ']
        output_prop = input_prop.copy()

        new_qcirc = empty_circuit()

        for gate in qcirc.gate_list:
            #@ circuit: new_qcirc

            if gate.isUnrollable():
                
                if not gate.hasDefinition():
                    raise_error("Unable to unroll. Multiqubit gate not defined.")

                gate_circ = definition(gate)
                new_qcirc = new_qcirc.extend(gate_circ)

            else:
                new_qcirc = new_qcirc.append(gate)
       
        output_prop['circ'] = new_qcirc

        return output_prop
