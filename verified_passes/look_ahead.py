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

from giallar.core.impl.layout import Layout, Permutation, update_layout_with_perm
from giallar.core.impl.qcircuit import QCircuit, empty_circuit, to_list
from giallar.core.impl.qgate import QGate, SwapGate
from giallar.core.impl.routing import Routing 
from giallar.utility_library.impl import map_free_gates, apply_swap
from giallar.core.impl.error_handler import raise_error
from copy import deepcopy

class LookaheadSwap(Routing):
    
    def __init__(self, coupling):
        self.coupling = coupling

    def run(self, input_prop):

        circ = input_prop['circ']
        initial_layout = input_prop["layout"]

        layout = initial_layout.copy()

        # print(layout)
        # print(circ.qubits)
        current_perm = Permutation(circ.qubits)
        output_prop = input_prop.copy()
        new_circ = empty_circuit()
        
        if circ.width() > self.coupling.size():
            raise_error("The qcircuit cannot fit into the coupling map")

        gates_remaining = circ.copy()
        # print(*[f"gate {gate.name} {gate.qubits}" for gate in gates_remaining.gate_list], sep = "\n")

        while gates_remaining.size() > 0:
            # print("++++++++start round+++++++++++++++++++++++++++")
            # # print(gates_remaining.gate_list)
            new_circ, gates_remaining = map_free_gates(gates_remaining, new_circ, layout, current_perm, self.coupling)
            best_swaps = _get_best_swaps(gates_remaining, layout, self.coupling, current_perm)
            for swap in best_swaps:
                # print(f"+++swap {swap}+++")
                new_circ, current_perm = apply_swap(new_circ, current_perm, swap, layout, self.coupling)
                # layout = update_layout_with_perm(initial_layout, current_perm)
                new_circ, gates_remaining = map_free_gates(gates_remaining, new_circ, layout, current_perm, self.coupling)
                # TODO change map_free_gates spec's return order
                # print(*[f"gate {gate.name} {gate.qubits}" for gate in gates_remaining.gate_list], sep = "\n")


        output_prop['circ'] = new_circ
        # print(*[f"new {gate.name} {gate.qubits}" for gate in new_circ.gate_list], sep = "\n")

        output_prop['perm'] = current_perm
        return output_prop

def _get_best_swaps(gates, layout, coup, perm):
    #@external
    #@ return [coupled_swap(layout, coup)] 
    best_steps = _search_forward_n_swaps(layout, gates, coup, perm, 4, 4)
    return best_steps["swaps_added"]

def _search_forward_n_swaps(layout, gates, coupling_map, perm, depth, width):

    # print(f"======== depth {depth} ========")
    # print(f"perm = {perm._i2n}")
    # print("---mapping gates---")

    gates_mapped, gates_remaining = map_free_gates(gates, empty_circuit(), layout, perm, coupling_map)
    # print("---mapping gates end---")
    base_step = { #'layout': layout,
                 'swaps_added': [],
                 'perm' : perm,
                 'gates_mapped': gates_mapped,
                 'gates_remaining': gates_remaining}

    if gates_remaining.size() == 0 or depth == 0:
        return base_step

    # Include symmetric 2q gates (e.g coupling maps with both [0,1] and [1,0])
    # as one available swap.
    possible_swaps = {to_tuple(sorted(edge))
                      for edge in coupling_map.get_edges()}


    def _score_swap(swap):
        """Calculate the relative score for a given SWAP."""
        trial_perm = deepcopy(perm)
        trial_perm.swap(*swap)
        return _calc_layout_distance(gates, coupling_map, layout, trial_perm)

    ranked_swaps = sorted(possible_swaps, key=_score_swap)
    # print("calculate swap scores")
    # print(*[f"swap: {swap}, score: {_score_swap(swap)}" for swap in ranked_swaps], sep="\n")
    # # print(ranked_swaps)
    best_swap, best_step = None, None
    for rank, swap in enumerate(ranked_swaps):
        trial_perm = deepcopy(perm)
        trial_perm.swap(*swap)
        # print(f"=== try swap {swap} ===")
        next_step = _search_forward_n_swaps(layout, gates_remaining,
                                            coupling_map, trial_perm, depth - 1, width)

        if next_step is None:
            continue
        # if depth == 4:
            # print(best_swap, best_step)
        # ranked_swaps already sorted by distance, so distance is the tie-breaker.
        if best_swap is None or _score_step(next_step) > _score_step(best_step):
            best_swap, best_step = swap, next_step

        if (
                rank >= min(width, length(ranked_swaps)-1)
                and best_step is not None
                and (
                    best_step['gates_mapped'].size() > depth
                    or best_step['gates_remaining'].size() < gates_remaining.size()
                    or (_calc_layout_distance(best_step['gates_remaining'],
                                              coupling_map,
                                              best_step['layout'], best_step['perm'])
                        < _calc_layout_distance(gates_remaining,
                                                coupling_map,
                                                layout, perm)))):
            # Once we've examined either $WIDTH swaps, or all available swaps,
            # return the best-scoring swap provided it leads to an improvement
            # in either the number of gates mapped, number of gates left to be
            # mapped, or in the score of the ending layout.
            break
    else:
        # print(f"return none depth {depth}, best_swap {best_step['swaps_added']}")
        return None

    # print(f"depth {depth}, best_swap {best_step['swaps_added']}")
    best_swap_gate = _swap_ops_from_edge(best_swap, layout)
    # swaps_added = [best_swap] + best_step['swaps_added']
    # print(swaps_added)
    return {
        # 'layout': best_step['layout'],
        'swaps_added': [best_swap] + best_step['swaps_added'],
        'gates_remaining': best_step['gates_remaining'],
        'perm' : best_step['perm'],
        'gates_mapped': gates_mapped.extend(best_swap_gate).extend(best_step['gates_mapped']),
    }

def _calc_layout_distance(gates, coupling_map, layout, perm, max_gates=None):
    """Return the sum of the distances of two-qubit pairs in each CNOT in gates
    according to the layout and the coupling.
    """
    if max_gates is None:
        max_gates = 50 + 10 * length(coupling_map.physical_qubits)
    return sum(coupling_map.distance(*[layout[perm._i2n[q]] for q in gates[i].qubits])
               for i in range(min(max_gates, gates.size()))
               if gates[i].is2QGate())


def _score_step(step):
    """Count the mapped two-qubit gates, less the number of added SWAPs."""
    # Each added swap will add 3 ops to gates_mapped, so subtract 3.
    return length([g for g in step['gates_mapped']
                if g.is2QGate()]) - 3 * length(step['swaps_added'])

def _swap_ops_from_edge(edge, layout):
    """Generate list of ops to implement a SWAP gate along a coupling edge."""

    # TODO shouldn't be making other nodes not by the DAG!!
    return [
        SwapGate(edge[0], edge[1])
    ]
