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

class Transformation:
    def __init__(self):
        pass

    def run(self, prop):
        return prop

    @classmethod
    def test(cls):
        layout = Layout()

        argstr = signature(cls.__init__).__repr__()
        # print(argstr)
        if "gate_name" in argstr and "gate_list" in argstr:
            tpass = cls(fresh_int(), EmptySet(IntSort()))
        elif "gate_name" in argstr:
            tpass = cls(fresh_int())
        elif "basis" in argstr:
            tpass = cls(fresh_array("", IntSort(), StringSort()))
        elif "coupling_map" in argstr:
            tpass = cls(CouplingMap())
        else:
            tpass = cls()

        # for any initial circuit
        init_circuit = QCircuit()

        input_prop = {}
        input_prop['circ'] = init_circuit
        input_prop['layout'] = layout

        # run the pass 
        output_prop = tpass.run(input_prop)

        out_circuit = output_prop['circ']

        # verify equivalence
        certiq_prove(equivalent(out_circuit, init_circuit), msg="Equivalence between {} and {}".format(out_circuit.name, init_circuit.name))

        print(cls.__name__ + " verified")
