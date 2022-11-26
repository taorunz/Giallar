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
from giallar.core.impl.coupling import CouplingMap
from giallar.core.impl.qcircuit import empty_circuit, decompose_with_basis, length, to_list, empty_dict, empty_frozenset, empty_set
from giallar.core.impl.qgate import QGate
from giallar.core.impl.transformation import Transformation
from giallar.core.impl.error_handler import raise_error

class BasisTranslator(Transformation):

    def __init__(self, basis):
        # super.__init__()
        self.basis = basis

    def run(self, input_prop):
        
        qcirc = input_prop['circ']
        output_prop = input_prop.copy()

        instr_map = _calculate_basis_transform(qcirc, self.basis, _basis_heuristic)

        new_qcirc = empty_circuit()

        for gate in qcirc.gate_list:
            #@ circuit: new_qcirc

            if gate.name not in self.basis:

                gate_circ = decompose_with_basis(gate, instr_map)
                new_qcirc = new_qcirc.extend(gate_circ)

            else:
                new_qcirc = new_qcirc.append(gate)
       
        output_prop['circ'] = new_qcirc

        return output_prop

def _basis_heuristic(basis, target):
    """Simple metric to gauge distance between two bases as the number of
    elements in the symmetric difference of the circuit basis and the device
    basis.
    """
    return length({gate_name for gate_name, _ in basis} ^ target)


def _calculate_basis_transform(equiv_lib, basis, heuristic):
    """Search for a set of transformations from source_basis to target_basis.

    Args:
        equiv_lib (EquivalenceLibrary): Source of valid translations
        source_basis (Set[Tuple[gate_name: str, gate_num_qubits: int]]): Starting basis.
        target_basis (Set[gate_name: str]): Target basis.
        heuristic (Callable[[source_basis, target_basis], int]): distance heuristic.

    Returns:
        Optional[List[Tuple[gate, equiv_params, equiv_circuit]]]: List of (gate,
            equiv_params, equiv_circuit) tuples tuples which, if applied in order
            will map from source_basis to target_basis. Returns None if no path
            was found.
    """

    source_basis = empty_frozenset(source_basis)
    target_basis = empty_frozenset(target_basis)

    open_set = empty_set()  # Bases found but not yet inspected.
    closed_set = empty_set()  # Bases found and inspected.

    # Priority queue for inspection order of open_set. Contains Tuple[priority, count, basis]
    open_heap = []

    # Map from bases in closed_set to predecessor with lowest cost_from_source.
    # Values are Tuple[prev_basis, gate_name, params, circuit].
    came_from = {}

    basis_count = iter_count()  # Used to break ties in priority.

    open_set.add(source_basis)
    heappush(open_heap, (0, next(basis_count), source_basis))

    # Map from basis to lowest found cost from source.
    cost_from_source = defaultdict(lambda: np.inf)
    cost_from_source[source_basis] = 0

    # Map from basis to cost_from_source + heuristic.
    est_total_cost = defaultdict(lambda: np.inf)
    est_total_cost[source_basis] = heuristic(source_basis, target_basis)

    logger.debug('Begining basis search from %s to %s.',
                 source_basis, target_basis)

    while open_set:
        _, _, current_basis = heappop(open_heap)

        if current_basis in closed_set:
            # When we close a node, we don't remove it from the heap,
            # so skip here.
            continue

        if {gate_name for gate_name, gate_num_qubits in current_basis}.issubset(target_basis):
            # Found target basis. Construct transform path.
            rtn = []
            last_basis = current_basis
            while last_basis != source_basis:
                prev_basis, gate_name, gate_num_qubits, params, equiv = came_from[last_basis]

                rtn.append((gate_name, gate_num_qubits, params, equiv))
                last_basis = prev_basis
            rtn.reverse()

            logger.debug('Transformation path:')
            for gate_name, gate_num_qubits, params, equiv in rtn:
                logger.debug('%s/%s => %s\n%s', gate_name, gate_num_qubits, params, equiv)
            return rtn

        logger.debug('Inspecting basis %s.', current_basis)
        open_set.remove(current_basis)
        closed_set.add(current_basis)

        for gate_name, gate_num_qubits in current_basis:
            equivs = equiv_lib._get_equivalences((gate_name, gate_num_qubits))

            basis_remain = current_basis - {(gate_name, gate_num_qubits)}
            neighbors = [
                (empty_frozenset(basis_remain | {(inst.name, inst.num_qubits)
                                           for inst, qargs, cargs in equiv.data}),
                 params,
                 equiv)
                for params, equiv in equivs]

            # Weight total path length of transformation weakly.
            tentative_cost_from_source = cost_from_source[current_basis] + 1e-3

            for neighbor, params, equiv in neighbors:
                if neighbor in closed_set:
                    continue

                if tentative_cost_from_source >= cost_from_source[neighbor]:
                    continue

                open_set.add(neighbor)
                came_from[neighbor] = (current_basis, gate_name, gate_num_qubits, params, equiv)
                cost_from_source[neighbor] = tentative_cost_from_source
                est_total_cost[neighbor] = tentative_cost_from_source \
                    + heuristic(neighbor, target_basis)
                heappush(open_heap, (est_total_cost[neighbor],
                                     next(basis_count),
                                     neighbor))

    return None


def _compose_transforms(basis_transforms, source_basis, source_dag):
    """Compose a set of basis transforms into a set of replacements.

    Args:
        basis_transforms (List[Tuple[gate_name, params, equiv]]): List of
            transforms to compose.
        source_basis (Set[Tuple[gate_name: str, gate_num_qubits: int]]): Names
            of gates which need to be translated.
        source_dag (DAGCircuit): DAG with example gates from source_basis.
            (Used to determine num_params for gate in source_basis.)

    Returns:
        Dict[gate_name, Tuple(params, dag)]: Dictionary mapping between each gate
            in source_basis and a DAGCircuit instance to replace it. Gates in
            source_basis but not affected by basis_transforms will be included
            as a key mapping to itself.
    """

    example_gates = {(node.op.name, node.op.num_qubits): node.op
                     for node in source_dag.op_nodes()}
    mapped_instrs = {}

    for gate_name, gate_num_qubits in source_basis:
        # Need to grab a gate instance to find num_qubits and num_params.
        # Can be removed following https://github.com/Qiskit/qiskit-terra/pull/3947 .
        example_gate = example_gates[gate_name, gate_num_qubits]
        num_params = length(example_gate.params)

        placeholder_params = ParameterVector(gate_name, num_params)
        placeholder_gate = Gate(gate_name, gate_num_qubits, to_list(placeholder_params))
        placeholder_gate.params = to_list(placeholder_params)

        dag = DAGCircuit()
        qr = QuantumRegister(gate_num_qubits)
        dag.add_qreg(qr)
        dag.apply_operation_back(placeholder_gate, qr[:], [])
        mapped_instrs[gate_name, gate_num_qubits] = placeholder_params, dag

    for gate_name, gate_num_qubits, equiv_params, equiv in basis_transforms:
        logger.debug('Composing transform step: %s/%s %s =>\n%s',
                     gate_name, gate_num_qubits, equiv_params, equiv)

        for mapped_instr_name, (dag_params, dag) in mapped_instrs.items():
            doomed_nodes = [node for node in dag.op_nodes()
                            if (node.op.name, node.op.num_qubits) == (gate_name, gate_num_qubits)]

            if doomed_nodes and logger.isEnabledFor(logging.DEBUG):
                from qiskit.converters import dag_to_circuit
                logger.debug('Updating transform for mapped instr %s %s from \n%s',
                             mapped_instr_name, dag_params, dag_to_circuit(dag))

            for node in doomed_nodes:
                from qiskit.converters import circuit_to_dag

                replacement = equiv.assign_parameters(
                    empty_dict(zip_longest(equiv_params, node.op.params)))

                replacement_dag = circuit_to_dag(replacement)

                dag.substitute_node_with_dag(node, replacement_dag)

            if doomed_nodes and logger.isEnabledFor(logging.DEBUG):
                from qiskit.converters import dag_to_circuit
                logger.debug('Updated transform for mapped instr %s %s to\n%s',
                             mapped_instr_name, dag_params, dag_to_circuit(dag))

    return mapped_instrs
