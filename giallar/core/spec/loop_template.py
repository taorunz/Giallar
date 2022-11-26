from z3 import *
import copy
from giallar.z3_wrapper import *
from giallar.core.spec.qgate import *
from giallar.core.spec.routing import *
from giallar.core.spec.invariant import *
from giallar.core.spec.layout import *
from giallar.core.spec.coupling import *
from giallar.core.spec.qcircuit import *
from giallar.utility_library.spec import *

def iterate_all_gates(circuit, layout, coup, func):
    
    # prepare new environment for induction
    assertion.push()

    # induction setting up
    i = fresh_int()
    n = circuit.size()
    cur_perm = Permutation(n)
    cur_circuit = QCircuit()

    assertion(i >= 0)
    assertion(i + 1 < n)

    #invariant: in i-th step, currently processed circuit is coupled and 
    #           equivalent to the first i gates in the original circuit
    #           according to the given permutation

    assertion(equivalent_part_perm(cur_circuit, cur_perm, circuit, i))
    assertion(coupling(cur_circuit, layout, coup))

    new_circuit, new_perm = func(circuit[i], cur_circuit, cur_perm, layout)

    # induction
    certiq_prove(equivalent_part_perm(new_circuit, new_perm, circuit, i+1), msg="iterate all gates induction")
    certiq_prove(coupling(new_circuit, layout, coup), msg="coupling constraints")

    # pop the current environment
    assertion.pop()

    ret_circuit = QCircuit()
    ret_perm = Permutation(fresh_int())

    assertion(equivalent_part_perm(ret_circuit, ret_perm, circuit, circuit.size()))
    assertion(coupling(ret_circuit, layout, coup))

    return ret_circuit, ret_perm

def iterate_all_gates_transform(circuit, func):
    
    # prepare new environment for induction
    assertion.push()

    # induction setting up
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

    assertion(equivalent_part(ret_circuit, circuit, circuit.size()))

    return ret_circuit

def iterate_all_blocks_transform(circuit, func):
    
    # prepare new environment for induction
    assertion.push()

    # induction setting up
    i = fresh_int()
    cur_circuit = QCircuit()

    new_circuit = func(cur_circuit)

    # induction
    certiq_prove(equivalent(new_circuit,  cur_circuit), msg="iterate all blocks induction")

    # pop the current environment 
    assertion.pop()

    ret_circuit = QCircuit()

    assertion(equivalent_part(ret_circuit, circuit, circuit.size()))

    return ret_circuit


def while_iterate_transformation(circuit, output_circ, func):
    
    # prove precondition
    certiq_prove(output_circ.size() == 0, msg="while transformation precondition for {}".format(output_circ.name))

    # prepare new environment for induction
    assertion.push()

    # induction setting up
    new_circuit, new_output_circ = func(circuit, output_circ)
    certiq_prove(equivalent(new_output_circ.extend(new_circuit), 
                            output_circ.extend(circuit)), 
                            msg="While loop induction for transformation/analysis pass")
   
    # pop the current environment
    assertion.pop()

    out_circ = empty_circuit() 
    ret_circ = QCircuit()
    
    set_option(timeout=250000)
    assertion(equivalent(ret_circ, circuit))

    return out_circ, ret_circ

def while_iterate_routing(circ, out_circ, layout, coup, func):
    certiq_prove(out_circ.size() == 0, msg = "While precondition")

    assertion.push()

    orig_circ = QCircuit()
    perm = Permutation(fresh_int())
    

    # assertion(equivalent_part_perm(out_circ, perm, orig_circ, orig_circ.size()))
    assertion(coupling(out_circ, layout, coup))
    assertion(pred_perm_equivalent(out_circ.gates, circ.gates, perm._i2n))
    new_circ, new_remaining, new_perm, new_layout = func(circ, out_circ, perm, layout)
    certiq_prove(pred_perm_equivalent(new_circ.gates, new_remaining.gates, new_perm._i2n), msg = "Equivalence invariant")
    # certiq_prove(equivalent_part_perm(new_circ, new_perm, orig_circ, orig_circ.size()))
    # certiq_prove(coupling(new_circ, new_layout, coup))
    certiq_prove(keep_coupling(new_circ.gates, out_circ.gates), msg = "Coupling invariant")
    assertion.pop()

    rem_circ = empty_circuit()
    ret_circ = QCircuit()
    ret_perm = Permutation(fresh_int())
    assertion(equivalent_part_perm(ret_circ, ret_perm, circ, circ.size()))
    assertion(coupling(ret_circ, layout, coup))

    return rem_circ, ret_circ, ret_perm