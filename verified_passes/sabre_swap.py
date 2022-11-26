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
from giallar.core.impl.qcircuit import QCircuit, empty_circuit, to_tuple, to_list, empty_dict, empty_frozenset, empty_set
from giallar.core.impl.routing import Routing 
from giallar.utility_library.impl import map_free_gates, apply_swap
from giallar.core.impl.error_handler import raise_error
import numpy as np
from copy import deepcopy
from collections import defaultdict

EXTENDED_SET_SIZE = 20  # Size of lookahead window. TODO: set dynamically to len(current_layout)
EXTENDED_SET_WEIGHT = 0.5  # Weight of lookahead window compared to front_layer.

DECAY_RATE = 0.001  # Decay coefficient for penalizing serial swaps.
DECAY_RESET_INTERVAL = 5  # How often to reset all decay rates to 1.

class SabreSwap(Routing):
    
    def __init__(self, coupling, heuristic = "basic", seed = 0):
        self.coupling = coupling
        self.heuristic = heuristic
        self.seed = seed
        self.rng = np.random.default_rng(self.seed)


    def run(self, input_prop):

        circ = input_prop['circ']
        initial_layout = input_prop["layout"]

        layout = initial_layout.copy()

        current_perm = Permutation(circ.qubits)
        output_prop = input_prop.copy()
        new_circ = empty_circuit()
        
        if circ.width() > self.coupling.size():
            raise_error("The qcircuit cannot fit into the coupling map")

        gates_remaining = circ.copy()

        while gates_remaining.size() > 0:
            # print(gates_remaining.gate_list)
            new_circ, gates_remaining = map_free_gates(gates_remaining, new_circ, layout, current_perm, self.coupling)
            best_swap = self._get_best_swap(gates_remaining, layout, current_perm, self.coupling)
            new_circ, current_perm = apply_swap(new_circ, current_perm, best_swap, layout, self.coupling)
            new_circ, gates_remaining = map_free_gates(gates_remaining, new_circ, layout, current_perm, self.coupling)


        output_prop['circ'] = new_circ
        output_prop['perm'] = current_perm
        return output_prop

    def _get_best_swap(self, gates, layout, perm, coup):
        #@external
        #@ return coupled_swap(layout, coup) 
        front_layer = gates.front_layer()
        extended_set = self._obtain_extended_set(gates, front_layer)
        swap_scores = {}
        for swap in self._obtain_swaps(front_layer, layout, perm):
            trial_perm = deepcopy(perm)
            trial_perm.swap(*swap)
            score = self._calculate_score(self.heuristic, front_layer, extended_set, layout, trial_perm, swap)
            swap_scores[swap] = score
        # print(f"swap_scores = {swap_scores}")
        min_score = min(swap_scores.values())
        best_swaps = [k for k, v in swap_scores.items() if v == min_score]
        best_swaps.sort()
        best_swap = self.rng.choice(best_swaps)
        # print(f"best swap = {best_swap}")
        return best_swap

    def _obtain_extended_set(self, circ, front_layer):
        """Populate extended_set by looking ahead a fixed number of gates.
        For each existing element add a successor until reaching limit.
        """
        extended_set = []
        incremented = []
        applied_predecessors = defaultdict(int)
        tmp_front_layer = front_layer
        done = False
        while tmp_front_layer and not done:
            new_tmp_front_layer = []
            for i, node in tmp_front_layer:
                for successor_id in circ.successors(i):
                    successor = circ[successor_id]
                    incremented.append(successor_id)
                    applied_predecessors[successor_id] += 1
                    if applied_predecessors[successor_id] == length(successor.qubits):
                        new_tmp_front_layer.append((successor_id, successor))
                        if successor.is2QGate():
                            extended_set.append(successor)
                if length(extended_set) >= EXTENDED_SET_SIZE:
                    done = True
                    break
            tmp_front_layer = new_tmp_front_layer
        return extended_set

    def _obtain_swaps(self, front_layer, layout, perm):
        """Return a set of candidate swaps that affect qubits in front_layer.

        For each virtual qubit in front_layer, find its current location
        on hardware and the physical qubits in that neighborhood. Every SWAP
        on virtual qubits that corresponds to one of those physical couplings
        is a candidate SWAP.

        Candidate swaps are sorted so SWAP(i,j) and SWAP(j,i) are not duplicated.
        """
        candidate_swaps = empty_set()
        for i, node in front_layer:
            for virtual in node.qubits:
                physical = layout[perm._i2n[virtual]]
                for neighbor in self.coupling.neighbors(physical):
                    # virtual_neighbor = layout[perm._i2n[neighbor]]
                    swap = sorted([physical, neighbor])
                    candidate_swaps.add(to_tuple(swap))
        return candidate_swaps

    def _compute_cost(self, layer, layout, perm):
        cost = 0
        layout_map = layout._v2p
        # print(layout_map, perm._i2n)
        for _, node in layer:
            if node.is2QGate():
                cost += self.coupling.distance(layout_map[perm._i2n[node.qubits[0]]], layout_map[perm._i2n[node.qubits[1]]])
        return cost

    def _calculate_score(self, heuristic, front_layer, extended_set, layout, perm, swap_qubits=None):
        """Return a heuristic score for a trial layout.

        Assuming a trial layout has resulted from a SWAP, we now assign a cost
        to it. The goodness of a layout is evaluated based on how viable it makes
        the remaining virtual gates that must be applied.
        """
        first_cost = self._compute_cost(front_layer, layout, perm)
        if heuristic == "basic":
            return first_cost

        first_cost /= length(front_layer)
        second_cost = 0
        if extended_set:
            second_cost = self._compute_cost(extended_set, layout, perm) / length(extended_set)
        total_cost = first_cost + EXTENDED_SET_WEIGHT * second_cost
        if heuristic == "lookahead":
            return total_cost

        if heuristic == "decay":
            return (
                max(self.qubits_decay[swap_qubits[0]], self.qubits_decay[swap_qubits[1]])
                * total_cost
            )

        # raise_error("Heuristic %s not recognized." % heuristic)