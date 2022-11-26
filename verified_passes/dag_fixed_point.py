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
from copy import deepcopy

class DAGFixedPoint(Analysis):

    def __init__(self):
        pass

    def run(self, input_prop):
        
        qcirc = input_prop['circ']
        input_prop['dag_fixed_point'] = self._dag_fixed_point(input_prop)

        return input_prop

    def _dag_fixed_point(self, input_prop):
        if input_prop["_dag_fixed_point_previous_dag"] is None:
            input_prop["_dag_fixed_point_previous_dag"] = deepcopy(input_prop["circ"])
            return False
        else:
            ret = input_prop["circ"] == input_prop["_dag_fixed_point_previous_dag"]
            input_prop["_dag_fixed_point_previous_dag"] = deepcopy(input_prop["circ"])
            return ret
