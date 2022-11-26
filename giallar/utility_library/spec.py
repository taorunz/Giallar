
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

from z3 import *
import copy
from giallar.z3_wrapper import *
from giallar.core.spec.qgate import *
from giallar.core.spec.routing import *
from giallar.core.spec.invariant import *
from giallar.core.spec.layout import *
from giallar.core.spec.coupling import *
from giallar.core.spec.qcircuit import *

pred_perm_equivalent = Function("perm_equivalent", CircuitType, CircuitType, ArraySort(IntSort(), IntSort()), BoolSort())
keep_coupling = Function("keep_coupling", CircuitType, CircuitType, BoolSort())
c1 = QCircuit()
c2 = QCircuit()
c3 = QCircuit()
assertion(ForAll([c1.gates], keep_coupling(c1.gates, c1.gates)))
assertion(ForAll([c1.gates, c2.gates], Implies(keep_coupling(c1.gates, c2.gates), keep_coupling(c2.gates, c1.gates))))
assertion(ForAll([c1.gates, c2.gates, c3.gates],
    Implies(
        And(keep_coupling(c1.gates, c2.gates), keep_coupling(c2.gates, c3.gates)),
        keep_coupling(c1.gates, c3.gates)
    )
))

'''
Behavior:
 for i in range(len - 2):
        v1 = path[i]
        v2 = path[i + 1]
        circuit.append(SwapGate(layout.p2v[v1], layout.p2v[v2]))
        perm.swap_now(v1, v2)
'''

def swap_along_a_path(circuit, perm, layout, path):

    dist = path.len
    x = path[0]
    y = path[dist - 1]

    coup = path.coup

    l = dist
    certiq_prove(l > 2, msg="swap condition")
    a = layout.p2v(x)
    b = layout.p2v(y)

    # prepare new environment for induction
    assertion.push()

    # assume case i
    i = fresh_int()
    assertion(i >= 0)
    assertion(i < l - 2)
    cur_perm = Permutation(fresh_int())
    cur_circuit = QCircuit()

    # one iteration
    v1 = layout.p2v(path[i])
    v2 = layout.p2v(path[i+1])
    sg = SwapGate(v1, v2)
    new_circuit = cur_circuit.append(sg)
    qubits = Array("any_qubit", IntSort(), QubitStateType)
    certiq_prove(ForAll([qubits], apply_swap_on_qubit_state(apply_circuit_on_qubit_state(qubits, cur_circuit, cur_circuit.size()), sg) ==

                                  apply_circuit_on_qubit_state(qubits, new_circuit, new_circuit.size())), msg="inserted assertion")
    new_perm = cur_perm.swap_now(v1, v2)

    #invariant: the processed circuit is equivalent to the original circuit
    #           according to a permutation, and the two qubits a and b is 
    #           mapped to the i-th and (l-1)-th qubits on the path
    assertion(equivalent_perm(circuit, perm, cur_circuit, cur_perm))
    assertion(coupling(cur_circuit, layout, coup))
    assertion(cur_perm.i2n(a) == layout.p2v(path[i]))
    assertion(cur_perm.i2n(b) == layout.p2v(path[l - 1]))

    # certiq_prove(equivalent_perm(cur_circuit, cur_perm, new_circuit, new_perm), msg="swap_along_a_path induction")
    certiq_prove(equivalent_perm(new_circuit, new_perm, cur_circuit, cur_perm), msg="swap_along_a_path induction")
    certiq_prove(coupling(new_circuit, layout, coup), msg="swap_along_a_path topology conformation")
    certiq_prove(new_perm.i2n(a) == layout.p2v(path[i+1]), msg="swap_along_a_path permutation 1st condition")
    certiq_prove(new_perm.i2n(b) == layout.p2v(path[l-1]),  msg="swap_along_a_path permutation 2nd condition")

    # complete induction
    assertion.pop()

    out_circuit = QCircuit()
    out_perm = Permutation(fresh_int())
    assertion(equivalent_perm(circuit, perm, out_circuit, out_perm))
    assertion(Implies(coupling(circuit, layout, coup), coupling(out_circuit, layout, coup)))
    assertion(out_perm.i2n(a) == layout.p2v(path[l - 2]))
    assertion(out_perm.i2n(b) == layout.p2v(path[l - 1]))

    return out_circuit, out_perm



def map_free_gates(gates_remaining, new_circ, layout, perm, coup):
    ret_remain = QCircuit()
    ret_circ = QCircuit()
    assertion(Implies(pred_perm_equivalent(new_circ.gates, gates_remaining.gates, perm._i2n), pred_perm_equivalent(ret_circ.gates, ret_remain.gates, perm._i2n)))
    assertion(keep_coupling(ret_circ.gates, new_circ.gates))
    return ret_circ, ret_remain 

def apply_swap(circ, perm, swap, layout, coup):
    remain = QCircuit()
    ret_circ = QCircuit()
    new_perm = Permutation(fresh_int())
    # certiq_prove(coup.distance(layout.v2p(swap[0]), layout.v2p(swap[1])) == 1, msg = "Swap coupling condition")
    assertion(ForAll([remain.gates], Implies(pred_perm_equivalent(circ.gates, remain.gates, perm._i2n), pred_perm_equivalent(ret_circ.gates, remain.gates, new_perm._i2n))))
    assertion(keep_coupling(ret_circ.gates, circ.gates))
    return ret_circ, new_perm


def coupled_swap(layout, coup):
    v0 = fresh_int()
    v1 = fresh_int()
    assertion(coup.distance(layout.v2p(v0), layout.v2p(v1)) == 1)
    return (v0, v1)

def merge_1q_gates(g1, g2):
    
    certiq_prove(And(g1.isRotationGate(), g2.isRotationGate()), msg="merge_1q_gate precondition")

    gid = fresh_int('gid')
    op = fresh_int('op')
    new_gate = QGate(gid, [op, op, op])

    qubits = fresh_array("qubits", IntSort(), QubitStateType)
    k = fresh_int("k")

    assertion(ForAll([qubits], apply_on_qubit_state(qubits, new_gate) == apply_on_qubit_state(apply_on_qubit_state(qubits, g1), g2)))

    new_circ = empty_circuit()
    new_circ = new_circ.append(new_gate)

    new_circ1 = empty_circuit()
    new_circ1 = new_circ.append(g1)
    new_circ1 = new_circ.append(g2)

    assertion(equivalent(new_circ, new_circ1))

    return new_gate

def hasDefinition(qgate):
    
    return Bool(str(qgate.gid())+"_has_def")

def definition(qgate):
    
    ret_circ = QCircuit(lemmas=False, name=str(qgate.name)+"def")

    qubits = fresh_array("qubits", IntSort(), QubitStateType)
    k = fresh_int("k")

    qgate_result = apply_on_qubit_state(qubits, qgate)
    ret_result = apply_circuit_on_qubit_state(qubits, ret_circ, ret_circ.size())

    assertion(ForAll([qubits, k], qgate_result[k] == ret_result[k]))

    return ret_circ

