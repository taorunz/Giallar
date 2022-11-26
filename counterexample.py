from giallar.core.spec.qcircuit import *
from giallar.core.spec.qgate import *
from giallar.core.spec.invariant import *
from giallar.z3_wrapper import *

size = Int('size')
size2 = Int('size2')
# assertion(size==2)
assertion(size2> size)
a = QCircuit(size=size)
# a.append(a[0])

gate_index = 0
gate = a[gate_index]

sucs = a.direct_successors(gate_index)

suc_gate = sucs['gates'][0]
suc_index = sucs['indices'][0]

b = a.remove(suc_index)
b = b.remove(0)

out_circ = QCircuit(size=2)
assertion(out_circ[0] == a[0])
assertion(out_circ[1] == suc_gate)

gid = fresh_int('gid')
op = fresh_int('op')
new_gate = QGate(gid, [op, op, op])

qubits = fresh_array("qubits", IntSort(), QubitStateType)
k = fresh_int("k")

assertion(ForAll([qubits, k], apply_on_qubit_state(qubits, new_gate)[k] == apply_on_qubit_state(apply_on_qubit_state(qubits, a[0]), suc_gate)[k]))

init_circ = QCircuit()
certiq_prove(equivalent(init_circ.append(new_gate).extend(b), init_circ.extend(a)))

"""
out_circ2 = QCircuit(size=1)
assertion(equivalent(out_circ, out_circ2))

# certiq_prove(equivalent(out_circ2.extend(b), a))

circ = QCircuit()
certiq_prove(equivalent(circ.extend(out_circ2).extend(b), circ.extend(a)))
"""

"""
assertion(a[0] == c[0])
assertion(b[0] == c[0])

assertion(a[1] == c[1])
assertion(b[1] == c[1])

certiq_prove(equivalent(a, b))
"""

"""
i = fresh_int()
j = fresh_int()
k = fresh_int()

assertion(And(i<j, i>0))


part1 = a.partial_circuit(0, i)
part2 = a.partial_circuit(i, j)
part3 = a.partial_circuit(0, j)

qubits = fresh_array("init_qubit", IntSort(), QubitStateType)

r1 = apply_circuit_on_qubit_state(qubits, part1, part1.size())
r2 = apply_circuit_on_qubit_state(r1, part2, part2.size())
r3 = apply_circuit_on_qubit_state(qubits, part3, part3.size())

m = fresh_int()

"""

# certiq_prove(ForAll([m], Implies(And(m>=0, m<a.size()), r2[m] == r3[m])))
# certiq_prove(equivalent(part1.extend(part2), part3))

"""
b = a.remove(1)
b_part_1 = b.partial_circuit(0, 1)
b_part_2 = b.partial_circuit(1, b.size())

a_part_1 = a.partial_circuit(0, 1)
a_part_2 = a.partial_circuit(2, a.size())

certiq_prove(equivalent(a_part_1, b_part_1))
certiq_prove(equivalent(a_part_2, b_part_2))
"""
"""
# certiq_prove(b.size() == a.size() - 1)

c = b.partial_circuit(1, a.size() - 1)
d = a.partial_circuit(2, a.size())
# print("hihi")
# certiq_prove(c.size() == d.size())

i = fresh_int()
certiq_prove(c.size() == a.size() - 2)
# certiq_prove(ForAll([i], Implies(And(i>=0, i<a.size()-2), c[i]==b[i+1])))
# assertion(ForAll([i], Implies(And(i>=0, i<a.size()-2), c[i]==b[i+1])))

j = fresh_int()
qubits = fresh_array("init_qubit", IntSort(), QubitStateType)
# certiq_prove(ForAll([i], Implies(And(i>=0, i<a.size()-2), b[i+1] == a[i+2])))
# assertion(ForAll([i], Implies(And(i>=0, i<a.size()-2), b[i+1] == a[i+2])))
certiq_prove(ForAll([i], Implies(And(i>=0, i<a.size()-2), c[i] == a[i+2])))
certiq_prove(ForAll([i], Implies(And(i>=0, i<a.size()-2), d[i] == a[i+2])))
certiq_prove(ForAll([i], Implies(And(i>=0, i<a.size()-2), c[i] == d[i])))

result_c = apply_circuit_on_qubit_state(qubits, c, c.size())
result_d = apply_circuit_on_qubit_state(qubits, d, d.size())
result_a_part = apply_part_circuit_on_qubit_state(

print("hihi")


print("hihi")

certiq_prove(ForAll([qubits, j], result_c[j] == result_d[j]))
"""

"""
i = fresh_int()
start=Int('start')
assertion(start==0)
assertion(ForAll([i], Implies(And(i<size, i>=start), a[i-start]==ex[i])))
assertion(ForAll([i], Implies(And(i<size, i>=0), b[i]==ex[i])))

certiq_prove(ForAll([i], Implies(And(i<size, i>=0), b[i]==a[i])))
"""

#########################
"""
i = Int('i')
assertion(And(i>0, i < size))

g = a[i]
"""
# a.append(g)

# a.extend(ex)

"""
b = a.remove(i)
c = a.partial_circuit(0, 1)
# d = a.partial_circuit(2, a.size())
d = a.partial_circuit(size2, a.size())
"""
