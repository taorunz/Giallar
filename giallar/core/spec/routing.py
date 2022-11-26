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

from giallar.core.spec.qcircuit import *
from giallar.core.spec.invariant import *
from giallar.core.spec.layout import *
from giallar.core.spec.coupling import *

class Routing:
    def __init__(self, coupling_map):
        self.coupling_map = coupling_map  

    def run(self, circuit):
        return circuit

    @classmethod
    def test(cls):
        coup = CouplingMap()
        layout = Layout()
        mapper = cls(coup)

        # for any initial circuit
        init_circuit = QCircuit()

        input_prop = {}
        input_prop['circ'] = init_circuit
        input_prop['layout'] = layout

        # run the mapper
        output_prop = mapper.run(input_prop)

        out_circuit = output_prop['circ']
        perm = output_prop['perm']

        # verify equivalence
        certiq_prove(equivalent_part_perm(out_circuit, perm, init_circuit, init_circuit.size()),
                     msg="Equivalence between {} and {}".format(out_circuit.name, init_circuit.name))
        # certiq_prove(equivalent(out_circuit, init_circuit))
        #verify coupling
        certiq_prove(coupling(out_circuit, layout, coup), msg="Topology conformation of {}".format(out_circuit.name))

        print(cls.__name__ + " verified")


