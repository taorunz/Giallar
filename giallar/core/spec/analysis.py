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
from inspect import signature

class Analysis:
    def __init__(self):
        pass

    def run(self, prop):
        return prop

    @classmethod
    def test(cls):
        layout = Layout()
        coup = CouplingMap()

        argstr = signature(cls.__init__).__repr__()
        # print(argstr)
        if "coupling_map" in argstr:
            mapper = cls(coup)
        elif "layout" in argstr:
            mapper = cls(layout)
        elif "property" in argstr:
            mapper = cls(fresh_string())
        else:
            mapper = cls()

        # for any initial circuit
        init_circuit = QCircuit()

        input_prop = {}
        input_prop['circ'] = init_circuit
        input_prop['layout'] = layout

        # run the mapper
        output_prop = mapper.run(input_prop)

        out_circuit = output_prop['circ']

        # verify equivalence
        certiq_prove(equivalent(out_circuit, init_circuit), msg = "equivalence")

        print(cls.__name__ + " verified")
