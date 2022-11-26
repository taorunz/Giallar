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
import random
from time import time
from constraint import Problem, RecursiveBacktrackingSolver, AllDifferentConstraint

class NoiseAdaptiveLayout(Analysis):

    def __init__(self, coupling_map):
        self.coupling_map = coupling_map

    def run(self, input_prop):
        
        qcirc = input_prop['circ']
        layout = self._generate_layout(qcirc)

        input_prop['layout'] = layout

        return input_prop
        
    def _initialize_backend_prop(self):
        """Extract readout and CNOT errors and compute swap costs."""
        backend_prop = self.backend_prop
        edge_list = []
        for ginfo in backend_prop.gates:
            if ginfo.gate == "cx":
                for item in ginfo.parameters:
                    if item.name == "gate_error":
                        g_reliab = 1.0 - item.value
                        break
                    g_reliab = 1.0
                swap_reliab = pow(g_reliab, 3)
                # convert swap reliability to edge weight
                # for the Floyd-Warshall shortest weighted paths algorithm
                swap_cost = -math.log(swap_reliab) if swap_reliab != 0 else math.inf
                edge_list.append((ginfo.qubits[0], ginfo.qubits[1], swap_cost))
                edge_list.append((ginfo.qubits[1], ginfo.qubits[0], swap_cost))
                self.cx_reliability[(ginfo.qubits[0], ginfo.qubits[1])] = g_reliab
                self.gate_list.append((ginfo.qubits[0], ginfo.qubits[1]))
        self.swap_graph.extend_from_weighted_edge_list(edge_list)
        idx = 0
        for q in backend_prop.qubits:
            for nduv in q:
                if nduv.name == "readout_error":
                    self.readout_reliability[idx] = 1.0 - nduv.value
                    self.available_hw_qubits.append(idx)
            idx += 1
        for edge in self.cx_reliability:
            self.gate_reliability[edge] = (
                self.cx_reliability[edge]
                * self.readout_reliability[edge[0]]
                * self.readout_reliability[edge[1]]
            )

        swap_reliabs_ro = rx.digraph_floyd_warshall_numpy(self.swap_graph, lambda weight: weight)
        for i in range(swap_reliabs_ro.shape[0]):
            self.swap_reliabs[i] = {}
            for j in range(swap_reliabs_ro.shape[1]):
                if (i, j) in self.cx_reliability:
                    self.swap_reliabs[i][j] = self.cx_reliability[(i, j)]
                elif (j, i) in self.cx_reliability:
                    self.swap_reliabs[i][j] = self.cx_reliability[(j, i)]
                else:
                    best_reliab = 0.0
                    for n in self.swap_graph.neighbors(j):
                        if (n, j) in self.cx_reliability:
                            reliab = math.exp(-swap_reliabs_ro[i][n]) * self.cx_reliability[(n, j)]
                        else:
                            reliab = math.exp(-swap_reliabs_ro[i][n]) * self.cx_reliability[(j, n)]
                        if reliab > best_reliab:
                            best_reliab = reliab
                    self.swap_reliabs[i][j] = best_reliab

    def _qarg_to_id(self, qubit):
        """Convert qarg with name and value to an integer id."""
        return self.qarg_to_id[qubit]

    def _create_program_graph(self, dag):
        """Program graph has virtual qubits as nodes.

        Two nodes have an edge if the corresponding virtual qubits
        participate in a 2-qubit gate. The edge is weighted by the
        number of CNOTs between the pair.
        """
        idx = 0
        for q in dag.qubits:
            self.qarg_to_id[q] = idx
            idx += 1
        edge_list = []
        for gate in dag.two_qubit_ops():
            qid1 = self._qarg_to_id(gate.qargs[0])
            qid2 = self._qarg_to_id(gate.qargs[1])
            min_q = min(qid1, qid2)
            max_q = max(qid1, qid2)
            edge_weight = 1
            if self.prog_graph.has_edge(min_q, max_q):
                edge_weight = self.prog_graph[min_q][max_q]["weight"] + 1
            edge_list.append((min_q, max_q, edge_weight))
        self.prog_graph.extend_from_weighted_edge_list(edge_list)
        return idx

    def _select_next_edge(self):
        """Select the next edge.

        If there is an edge with one endpoint mapped, return it.
        Else return in the first edge
        """
        for edge in self.pending_program_edges:
            q1_mapped = edge[0] in self.prog2hw
            q2_mapped = edge[1] in self.prog2hw
            assert not (q1_mapped and q2_mapped)
            if q1_mapped or q2_mapped:
                return edge
        return self.pending_program_edges[0]

    def _select_best_remaining_cx(self):
        """Select best remaining CNOT in the hardware for the next program edge."""
        candidates = []
        for gate in self.gate_list:
            chk1 = gate[0] in self.available_hw_qubits
            chk2 = gate[1] in self.available_hw_qubits
            if chk1 and chk2:
                candidates.append(gate)
        best_reliab = 0
        best_item = None
        for item in candidates:
            if self.gate_reliability[item] > best_reliab:
                best_reliab = self.gate_reliability[item]
                best_item = item
        return best_item

    def _select_best_remaining_qubit(self, prog_qubit):
        """Select the best remaining hardware qubit for the next program qubit."""
        reliab_store = {}
        if prog_qubit not in self.prog_neighbors:
            self.prog_neighbors[prog_qubit] = self.prog_graph.neighbors(prog_qubit)
        for hw_qubit in self.available_hw_qubits:
            reliab = 1
            for n in self.prog_neighbors[prog_qubit]:
                if n in self.prog2hw:
                    reliab *= self.swap_reliabs[self.prog2hw[n]][hw_qubit]
            reliab *= self.readout_reliability[hw_qubit]
            reliab_store[hw_qubit] = reliab
        max_reliab = 0
        best_hw_qubit = None
        for hw_qubit in reliab_store:
            if reliab_store[hw_qubit] > max_reliab:
                max_reliab = reliab_store[hw_qubit]
                best_hw_qubit = hw_qubit
        return best_hw_qubit

    def _generate_layout(self, dag):
        """Run the NoiseAdaptiveLayout pass on `dag`."""
        self.swap_graph = rx.PyDiGraph()
        self.cx_reliability = {}
        self.readout_reliability = {}
        self.available_hw_qubits = []
        self.gate_list = []
        self.gate_reliability = {}
        self.swap_reliabs = {}
        self.prog_graph = rx.PyGraph()
        self.prog_neighbors = {}
        self.qarg_to_id = {}
        self.pending_program_edges = []
        self.prog2hw = {}

        self._initialize_backend_prop()
        num_qubits = self._create_program_graph(dag)
        if num_qubits > len(self.swap_graph):
            raise TranspilerError("Number of qubits greater than device.")

        # sort by weight, then edge name for determinism (since networkx on python 3.5 returns
        # different order of edges)
        self.pending_program_edges = sorted(
            self.prog_graph.weighted_edge_list(), key=lambda x: [x[2], -x[0], -x[1]], reverse=True
        )

        while self.pending_program_edges:
            edge = self._select_next_edge()
            q1_mapped = edge[0] in self.prog2hw
            q2_mapped = edge[1] in self.prog2hw
            if (not q1_mapped) and (not q2_mapped):
                best_hw_edge = self._select_best_remaining_cx()
                if best_hw_edge is None:
                    raise TranspilerError(
                        "CNOT({}, {}) could not be placed "
                        "in selected device.".format(edge[0], edge[1])
                    )
                self.prog2hw[edge[0]] = best_hw_edge[0]
                self.prog2hw[edge[1]] = best_hw_edge[1]
                self.available_hw_qubits.remove(best_hw_edge[0])
                self.available_hw_qubits.remove(best_hw_edge[1])
            elif not q1_mapped:
                best_hw_qubit = self._select_best_remaining_qubit(edge[0])
                if best_hw_qubit is None:
                    raise TranspilerError(
                        "CNOT({}, {}) could not be placed in selected device. "
                        "No qubit near qr[{}] available".format(edge[0], edge[1], edge[0])
                    )
                self.prog2hw[edge[0]] = best_hw_qubit
                self.available_hw_qubits.remove(best_hw_qubit)
            else:
                best_hw_qubit = self._select_best_remaining_qubit(edge[1])
                if best_hw_qubit is None:
                    raise TranspilerError(
                        "CNOT({}, {}) could not be placed in selected device. "
                        "No qubit near qr[{}] available".format(edge[0], edge[1], edge[1])
                    )
                self.prog2hw[edge[1]] = best_hw_qubit
                self.available_hw_qubits.remove(best_hw_qubit)
            new_edges = [
                x
                for x in self.pending_program_edges
                if not (x[0] in self.prog2hw and x[1] in self.prog2hw)
            ]
            self.pending_program_edges = new_edges
        for qid in self.qarg_to_id.values():
            if qid not in self.prog2hw:
                self.prog2hw[qid] = self.available_hw_qubits[0]
                self.available_hw_qubits.remove(self.prog2hw[qid])
        layout = Layout()
        for q in dag.qubits:
            pid = self._qarg_to_id(q)
            hwid = self.prog2hw[pid]
            layout[q] = hwid
        for qreg in dag.qregs.values():
            layout.add_register(qreg)
        self.property_set["layout"] = layout