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

from giallar.core.impl.analysis import Analysis
class CheckMap(Analysis):

    def __init__(self, coupling_map):
        # super().__init__()
        self.coupling_map = coupling_map

    def run(self, input_prop):

        qcirc = input_prop['circ']
        layout = input_prop['layout']
        output_prop = input_prop.copy()
        output_prop['checkmap'] = self._check_map(qcirc, layout)
             
        return output_prop

    def _check_map(self, qcirc, layout):

        ret = True
        for gate in qcirc.gate_list:
            if gate.is2QGate():
                physical_q0 = layout[gate.qubits[0]]
                physical_q1 = layout[gate.qubits[1]]

                if self.coupling_map.distance(physical_q0, physical_q1) != 1:
                    ret = False

        return ret