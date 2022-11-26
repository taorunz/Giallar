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
from giallar.z3_wrapper import *
from giallar.core.spec.qgate import *
from giallar.core.spec.qcircuit import apply_circuit_on_qubit_state, apply_part_circuit_on_qubit_state
from giallar.core.spec.layout import *
# from IPython import embed

def equivalent(circuit, orig_circuit):
    qubits = fresh_array("init_qubit", IntSort(), QubitStateType)

    result = apply_circuit_on_qubit_state(qubits, circuit, circuit.size())
    orig_result = apply_circuit_on_qubit_state(qubits, orig_circuit, orig_circuit.size())

    i = fresh_int()
    return ForAll([qubits, i], result[i] == orig_result[i])

def equivalent_part(circuit, orig_circuit, n):
    qubits = fresh_array("init_qubit", IntSort(), QubitStateType)

    result = apply_circuit_on_qubit_state(qubits, circuit, circuit.size())
    orig_result = apply_circuit_on_qubit_state(qubits, orig_circuit, n)

    i = fresh_int()
    return ForAll([qubits, i], result[i] == orig_result[i])

def equivalent_middle_part(circuit, orig_circuit, m, n):
    qubits = fresh_array("init_qubit", IntSort(), QubitStateType)

    result = apply_circuit_on_qubit_state(qubits, circuit, circuit.size())
    orig_result = apply_part_circuit_on_qubit_state(qubits, orig_circuit, m + 1, n)

    i = fresh_int()
    return ForAll([qubits, i], result[i] == orig_result[i])

def equivalent_part_perm(circuit, perm, orig_circuit, n):
    qubits = fresh_array("init_qubit", IntSort(), QubitStateType)

    result = apply_circuit_on_qubit_state(qubits, circuit, circuit.size())
    orig_result = apply_circuit_on_qubit_state(qubits, orig_circuit, n) 

    i = fresh_int()
    return ForAll([qubits, i], result[perm.i2n(i)] == orig_result[i])

def equivalent_perm(circuit1, perm1, circuit2, perm2):
    qubits = Array("init_qubit", IntSort(), QubitStateType)

    result1 = apply_circuit_on_qubit_state(qubits, circuit1, circuit1.size())
    result2 = apply_circuit_on_qubit_state(qubits, circuit2, circuit2.size())

    i = Int("index")
    return ForAll([qubits, i], result1[perm1.i2n(i)] == result2[perm2.i2n(i)])

def equivalent_combine(circuit, perm, circuit2, orig_circuit):
    qubits = fresh_array("init_qubit", IntSort(), QubitStateType)

    mid_result = apply_circuit_on_qubit_state(qubits, circuit, circuit.size())
    mid_result_permed = fresh_array("init_qubit", IntSort(), QubitStateType)

    j = fresh_int()
    assertion(ForAll(j, mid_result_permed[j] == mid_result[perm.i2n(j)]))

    final_result = apply_circuit_on_qubit_state(mid_result_permed, circuit2, circuit2.size())

    orig_result = apply_circuit_on_qubit_state(qubits, orig_circuit, orig_circuit.size())

    i = fresh_int()
    return ForAll([qubits, i], final_result[perm.i2n(i)] == orig_result[i])

