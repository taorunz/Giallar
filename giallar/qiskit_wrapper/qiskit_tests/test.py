from z3 import *
from giallar.core.spec.qcircuit import *
from giallar.utility_library.impl import *
from giallar.core.spec.qgate import *
from giallar.z3_wrapper import *
from giallar.core.spec.invariant import *

def loop_body0(gate, new_qcirc):
    new_qcirc = new_qcirc.append(gate)
    return new_qcirc

def iterate_all_gates_transform(circuit, func):
    i = fresh_int()
    n = circuit.size()
    cur_circuit = QCircuit()

    assertion(i >= 0)
    assertion(i + 1 < n)

    #invariant: in i-th step, currently processed circuit is coupled and 
    #           equivalent to the first i gates in the original circuit
    #           according to the given permutation

    assertion(equivalent_part(cur_circuit,  circuit, i))

    new_circuit = func(circuit[i], cur_circuit)

    # induction
    certiq_prove(equivalent_part(new_circuit,  circuit, i+1), msg="iterate all gates induction")

    # pop the current environment 
    assertion.pop()

    ret_circuit = QCircuit()

    assertion(equivalent(ret_circuit, circuit))

    return ret_circuit

qcirc = QCircuit()
new_qcirc = QCircuit()

new_qcirc = iterate_all_gates_transform(qcirc, loop_body0)

