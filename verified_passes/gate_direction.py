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
from giallar.core.impl.qgate import CNOTGate, HGate, ECRGate, RZXGate

class GateDirection(Transformation):

    def __init__(self, coupling_map):
        # super().__init__()
        self.coupling_map = coupling_map

    def run(self, input_prop):

        qcirc = input_prop['circ']
        layout = input_prop['layout']

        output_prop = input_prop.copy()

        out_circ = empty_circuit()

        for gate in qcirc.gate_list:

            if gate.isCXGate():

                q0 = gate.arg(0)
                physical_q0 = layout[gate.qubits[0]]
                q1 = gate.arg(1)
                physical_q1 = layout[gate.qubits[1]]
                if not (physical_q0, physical_q1) in self.coupling_map.get_edges():
                    out_circ = out_circ.append(HGate(q0))
                    out_circ = out_circ.append(HGate(q1))
                    out_circ = out_circ.append(CNOTGate(q1, q0))
                    out_circ = out_circ.append(HGate(q0))
                    out_circ = out_circ.append(HGate(q1))
                else:   
                    out_circ = out_circ.append(gate)
            elif gate.isECRGate():

                q0 = gate.arg(0)
                physical_q0 = layout[gate.qubits[0]]
                q1 = gate.arg(1)
                physical_q1 = layout[gate.qubits[1]]
                if not (physical_q0, physical_q1) in self.coupling_map.get_edges():
                    out_circ = out_circ.append(HGate(q0))
                    out_circ = out_circ.append(HGate(q1))
                    out_circ = out_circ.append(ECRGate(q1, q0))
                    out_circ = out_circ.append(HGate(q0))
                    out_circ = out_circ.append(HGate(q1))
                else:   
                    out_circ = out_circ.append(gate)
            elif gate.isRZXGate():

                q0 = gate.arg(0)
                physical_q0 = layout[gate.qubits[0]]
                q1 = gate.arg(1)
                physical_q1 = layout[gate.qubits[1]]
                if not (physical_q0, physical_q1) in self.coupling_map.get_edges():
                    out_circ = out_circ.append(HGate(q0))
                    out_circ = out_circ.append(HGate(q1))
                    out_circ = out_circ.append(RZXGate(q1, q0))
                    out_circ = out_circ.append(HGate(q0))
                    out_circ = out_circ.append(HGate(q1))
                else:   
                    out_circ = out_circ.append(gate)
            else:
                out_circ = out_circ.append(gate)
        output_prop['circ'] = out_circ

        return output_prop

