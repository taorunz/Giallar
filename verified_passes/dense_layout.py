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

from giallar.core.impl.error_handler import raise_error
from giallar.core.impl.analysis import Analysis
from giallar.core.impl.layout import Layout
import numpy as np
import scipy.sparse as sp
import scipy.sparse.csgraph as cs

class DenseLayout(Analysis):

    def __init__(self, coupling_map):
        self.coupling_map = coupling_map

    def run(self, input_prop):
        
        qcirc = input_prop['circ']
        layout = self._generate_dense_layout(qcirc)

        input_prop['layout'] = layout

        return input_prop


    def _generate_dense_layout(self, qcirc):
        num_dag_qubits = len(qcirc.qubits)
        if num_dag_qubits > self.coupling_map.size():
            raise_error("Number of qubits greater than device")
        
        # Get ave number of cx and meas per qubit
        ops = qcirc.cout_ops()
        if "cx" in ops.keys():
            self.num_cx = ops["cx"]
        if "measure" in ops.keys():
            self.num_meas = ops["measure"]
        
        # Compute the sparse cx_err matrix and meas array
        # In CertiQ, we do not have backend_prop

        best_sub = self._best_subset(num_dag_qubits)
        layout = Layout()
        map_iter = 0
        for qb in qcirc.qubits():
            layout[qb] = int(best_sub[map_iter])
            map_iter += 1
        
        return layout
    
    def _best_subset(self, num_qubits):
        if num_qubits == 1:
            return np.array([0])
        if num_qubits == 0:
            return []
        
        device_qubits = self.coupling_map.size()

        cmap = np.asarray(self.coupling_map.get_edges())
        data = np.ones_like(cmap[: 0])
        sp_cmap = sp.coo_matrix((data, (cmap[:, 0], cmap[:, 1])), 
            shape = (device_qubits, device_qubits)
        ).tocsr()
        
        best = 0
        best_map = None
        best_error = np.inf
        best_sub = None
        # do bfs with each node as starting point
        for k in range(sp_cmap.shape[0]):
            bfs = cs.breadth_first_order(
                sp_cmap, i_start = k, directed = False, return_predecessors = False
            )

            connection_count = 0
            sub_graph = []
            for i in range(num_qubits):
                node_idx = bfs[i]
                for j in range(sp_cmap.indptr[node_idx], sp_cmap.indptr[node_idx + 1]):
                    node = sp_cmap.indices[j]
                    for counter in range(num_qubits):
                        if node == bfs[counter]:
                            connection_count += 1
                            sub_graph.append([node_idx, node])
                            break
            
            # In CertiQ, we do not have backend_prop
            if connection_count > best:
                best = connection_count
                best_map = bfs[0:num_qubits]
                best_sub = sub_graph
        
        # Return a best mapping that has reduced bandwidth
        mapping = {}
        for edge in range(best_map.shape[0]):
            mapping[best_map[edge]] = edge
        new_cmap = [[mapping[c[0]], mapping[c[1]]] for c in best_sub]
        rows = [edge[0] for edge in new_cmap]
        cols = [edge[1] for edge in new_cmap]
        data = [1] * len(rows)
        sp_sub_graph = sp.coo_matrix((data, (rows, cols)),
            shape = (num_qubits, num_qubits)
        ).tocsr()
        perm = cs.reverse_cuthill_mckee(sp_sub_graph)
        best_map = best_map[perm]
        return best_map

