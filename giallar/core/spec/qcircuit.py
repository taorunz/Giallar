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

"""
Specification for quantum circuits in CertiQ 
"""

from sympy import Equivalent
from giallar.core.spec.z3_base import *
from giallar.core.spec.qgate import *
from giallar.z3_wrapper import fresh_int, certiq_prove, fresh_name
# from certiq.certiq_core.certiq_spec.invariant import equivalent_middle_part

# Declare Z3 data structure for quantum circuit

class QCircuit:

    def __init__(self, gates=None, size=None, name=""):
        
        self.name = fresh_name("circuit") if name=="" else name
        self.gates = Array(self.name+"_gates", IntSort(), GateType) if gates is None else gates

        if size is None:
            self_size = fresh_int("circuit_size")
            assertion(self_size>=0)

        else:
            self_size = size

        self.self_size = self_size
        self.qubits = Array(self.name+"_qubits", IntSort(), QubitType)

    @classmethod
    def as_circuit(cls, gates, size, name=""):
        return cls(gates=gates, size=size, name=name)
        
    def size(self):
        return self.self_size

    def depth(self):
        return fresh_int()

    def is_empty(self):
        return self.size() == 0

    def __getitem__(self, i):
        return QGate.as_gate(self.gates[i])

    def __eq__(self, cb):

        return And(self.gates == cb.gates, self.self_size == cb.self_size)
    
    def copy(self):
        
        circ = QCircuit()
        assertion(self.gates == circ.gates)
        assertion(self.self_size == circ.self_size)

        return circ

    def append(self, gate):
        gates = Store(self.gates, self.size(), gate.data)
        name = "{}_append_{}".format(self.name, gate.name)
        size = self.self_size + 1

        ret_circ = QCircuit(gates=gates, size=size, name=name)

        return ret_circ
    
    def appendBarrier(self, qubit):
        return self

    def extend(self, circ, self_lemmas=2):
    
        new_size = self.size() + circ.size()

        i = fresh_int()
        out_circ = QCircuit(size = new_size, name=self.name+circ.name+"_extend")

        """
        print("proving sizes")
        certiq_prove(out_circ.size()>=self.size())
        certiq_prove(out_circ.size()>=circ.size())
        print("finished proving sizes")
        """ 

        assertion(ForAll([i], Implies(And(i<self.size(), i>=0), out_circ[i] == self[i])))
        assertion(ForAll([i], Implies(And(i<new_size, i>=self.size()), out_circ[i] == circ[i-self.size()])))
        # assertion(ForAll([i], Implies(And(i<new_size-self.size(), i>=0), out_circ[i+self.size()] == circ[i])))

        i = fresh_int()
        qubits = fresh_array("init_qubit", IntSort(), QubitStateType)
        
        part1 = out_circ.partial_circuit(0, self.size())
        part2 = out_circ.partial_circuit(self.size(), out_circ.size())

        """
        # The proof of the following assertions
        # certiq_prove(part1.size() == self.size())
        # certiq_prove(part2.size() == circ.size())
        # certiq_prove(ForAll([i], Implies(And(i<self.size(), i>=start), out_circ[i] == self[i-start])))
        # certiq_prove(ForAll([i], Implies(And(i<self.size(), i>=start), out_circ[i] == part1[i-start])))
        # certiq_prove(ForAll([i], Implies(And(i>=0, i<self.size()), part1[i] == self[i])))
        # certiq_prove(ForAll([i], Implies(And(i<circ.size(), i>=start), out_circ[i+self.size()] == part2[i])))
        # certiq_prove(ForAll([i], Implies(And(i<circ.size(), i>=start), out_circ[i+self.size()] == circ[i])))
        # certiq_prove(ForAll([i], Implies(And(i<circ.size(), i>=start), part2[i] == circ[i])))
        """ 
        
        assertion(ForAll([i], Implies(And(i>=0, i<self.size()), part1[i] == self[i])))
        assertion(ForAll([i], Implies(And(i<circ.size(), i>=0), part2[i] == circ[i])))

        result1 = apply_circuit_on_qubit_state(qubits, part1, part1.size())
        self_result = apply_circuit_on_qubit_state(qubits, self, self.size())

        result2 = apply_circuit_on_qubit_state(qubits, part2, part2.size())
        circ_result = apply_circuit_on_qubit_state(qubits, circ, circ.size())
    
        assertion(ForAll([qubits], result1 == self_result))
        assertion(ForAll([qubits], result2 == circ_result))

        result = apply_circuit_on_qubit_state(apply_circuit_on_qubit_state(qubits, self, self.size()), circ, circ.size())
        out_result = apply_circuit_on_qubit_state(qubits, out_circ, out_circ.size())
        
        qubits = fresh_array("init_qubit", IntSort(), QubitStateType)

        assertion(ForAll([qubits], out_result == result)) 

        if self.name == "empty_circuit":

            out_circ = circ

        return out_circ

    def isDiagonalBeforeMeasurements(self, i):
        
        sucs = self.direct_successors(i)['gates']
        remove_i = self.remove[i]

        is_dbfm = And(sucs.isOnlyMeasurements(), self[i].isDiagonal())

        qubits = fresh_array("init_qubit", IntSort(), QubitStateType)
        j = fresh_int()

        assertion(Implies(is_dbfm, ForAll([qubits, j], remove_i[j] == self[j])))

        return is_dbfm


    def isOnlyMeasurements(self):
        
        i = fresh_int()

        return ForAll([i], Implies(And(i>=0, i<self.size()), GateType.gid(self[i].data) == 16))
                
    def direct_successors(self, i):
       
        input_ind = i

        # certiq_prove(And(input_ind<self.size(), input_ind>=0), msg="Direct successor size return size for circuit {}".format(self.name))

        if_successful = Bool(self.name+str(i)+'ds_successful')

        size = Int(self.name+str(i)+'ds_circuit_size')

        assertion(Implies(self[i].is1QGate(), size==1))
        assertion(Implies(self[i].is2QGate(), size<=2))
        assertion(And(size>=0, size<self.size() - input_ind))

        assertion(Implies(if_successful, size == 0))

        ret_suc = {}

        ret_suc['indices'] = Array(self.name+str(i)+"indices", IntSort(), IntSort())
        ret_suc['if_successful'] = if_successful

        ret_ind_i = fresh_int()
        assertion(ForAll([ret_ind_i], And(ret_suc['indices'][ret_ind_i]>input_ind, ret_suc['indices'][ret_ind_i] <self.size())))

        ret_circuit = empty_circuit()
        ret_circuit = ret_circuit.append(self[ret_suc['indices'][0]])
        ret_circuit = ret_circuit.append(self[ret_suc['indices'][1]])
        # ret_circuit = ret_circuit.extend(QCircuit()) # TODO: support 3-qubit gates
        ret_suc['gates'] = ret_circuit

        self._suc_lemmas(input_ind, ret_suc['indices'][0])
        self._suc_lemmas(input_ind, ret_suc['indices'][1])
        
        removed_i = self.remove(i) 
        qubits = fresh_array("init_qubits", IntSort(), QubitStateType)
        assertion(Implies(And(self[i].isDiagonal(), ret_suc['gates'].isOnlyMeasurements()),
                          ForAll([qubits], apply_circuit_on_qubit_state(qubits, removed_i, removed_i.size()) ==
                                           apply_circuit_on_qubit_state(qubits, self, self.size()))))

        return ret_suc
    
    def has_direct_successors(self, i):
        
        return self.direct_successors(i)['if_successful']
    
    def next_gate(self, i):
        x = fresh_int()
        assertion(x > i)
        assertion(x < self.size())
        return self[x]
    
    def cancelStartingCX(self):
        ret = QCircuit()
        from giallar.core.spec.invariant import equivalent
        assertion(equivalent(self, ret))
        return ret

    def mergeBarriers(self):
        ret = QCircuit()
        from giallar.core.spec.invariant import equivalent
        assertion(equivalent(self, ret))
        return ret
        
    def start_with_final_measurement(self):
        from giallar.core.spec.invariant import equivalent
        ret = fresh_bool()
        assertion(Implies(ret, equivalent(self, self.remove(0))))
        return ret

    def isZeroState(self, gate):
        from giallar.core.spec.invariant import equivalent
        ret = fresh_bool()
        assertion(Implies(And(ret, gate.isReset()), equivalent(self, self.append(gate))))
        return ret
    
    def isAll2Q(self):
        return fresh_bool()
        
    
    def pairwiseCommute(self):
        return fresh_bool()

    def consolidate(self):
        ret = QCircuit()
        from giallar.core.spec.invariant import equivalent
        assertion(equivalent(self, ret))
        return ret
    
    def cancelGates(self):
        ret = QCircuit()
        from giallar.core.spec.invariant import equivalent
        assertion(equivalent(self, ret))
        return ret

    def _suc_lemmas(self, i, j):
        
        """
        if isinstance(i, int):
            i_z3 = Int(self.name + "suc_lemma_i")
            assertion(i_z3 == i)
        else:
            i_z3 = i
        if isinstance(j, int):
            j_z3 = Int(self.name + "suc_lemma_j")
            assertion(j_z3 == j)
        else:
            j_z3 = j
        """

        # certiq_prove(i_z3 < j_z3, msg="Precondition 1 in successor lemmas for gate {} in circuit {}".format(i, self.name))
        # certiq_prove(j_z3 <self.size(), msg="Precondition 2 in sucessor lemmasfor gate {} in circuit {}".format(i, self.name))


        """ 
        # jth gate can be moved to the front
        combine_1_part_1 = self.partial_circuit(0, i+1).append(suc_gate)
        combine_1_part_2 = self.remove(j).partial_circuit(i+1, self.size()-1)

        qubits = fresh_array("init_qubits", IntSort(), QubitStateType)
        k = fresh_int()
        
        assertion(ForAll([qubits, k], apply_circuit_on_qubit_state(qubits, combine_1_part_1.extend(combine_1_part_2, lemmas=False), self.size())[k]
                                   == apply_circuit_on_qubit_state(qubits, self, self.size())[k]))

        # 0-(i-1) and (i, j) and the rest equal to the original circuit
        combine_2_part_1 = self.partial_circuit(0, i)

        combine_2_part_2_size = fresh_int("size")
        assertion(combine_2_part_2_size==2)

        combine_2_part_2 = QCircuit(size=combine_2_part_2_size, lemmas=False, name=self.name+str(i)+str(j)+"_combine_part_2")
        assertion(combine_2_part_2[0] == self[i])
        assertion(combine_2_part_2[1] == self[j])
        
        combine_2_part_3 = self.remove(j).partial_circuit(i+1, self.size()-1)
        
        assertion(ForAll([qubits, k], 
                  apply_circuit_on_qubit_state(qubits, 
                                               combine_2_part_1.extend(combine_2_part_2, lemmas=False).extend(combine_2_part_3, lemmas=False), 
                                               self.size())[k]
                  == apply_circuit_on_qubit_state(qubits, self, self.size())[k]))
        """

        # The followings are simple cases where i = 0. 

        qubits = fresh_array("init_qubits", IntSort(), QubitStateType)
        k = fresh_int()

        gate = self[i]
        suc_gate = self[j]

        if isinstance(i, int) and i == 0:
            ij_circuit = empty_circuit()
            ij_circuit = ij_circuit.append(gate)
            ij_circuit = ij_circuit.append(suc_gate)

            rest_circuit = self.remove(j).remove(i)
            new_circ = ij_circuit.extend(rest_circuit)

            assertion(ForAll([qubits, k], 
                      apply_circuit_on_qubit_state(qubits,
                                                   new_circ,
                                                   new_circ.size())[k] == 
                      apply_circuit_on_qubit_state(qubits, 
                                                   self, 
                                                   self.size())[k]))
        

        return 

    def remove(self, x):
        
        ind = x

        new_circuit = QCircuit(name=self.name+str(x)+"_removed")
        
        if isinstance(x, int) and x == 0:
            new_circuit = self.partial_circuit(1, self.size())

        else:
            new_circuit = self.partial_circuit(0, x).extend(self.partial_circuit(x+1, self.size()))

        return new_circuit
            
        """
        i = fresh_int()
        assertion(new_circuit.size() == self.size() - 1)
        assertion(ForAll([i], Implies(And(0 <= i, i < ind), new_circuit[i] == self[i])))
        assertion(ForAll([i], Implies(And(ind <= i, i < new_circuit.size()), new_circuit[i] == self[i + 1])))
        
        part_1 = self.partial_circuit(0, ind)
        part_2 = self.partial_circuit(ind+1, self.size())

        new_part_1 = new_circuit.partial_circuit(0, ind)
        new_part_2 = new_circuit.partial_circuit(ind, new_circuit.size())
        assertion(ForAll([i], Implies(And(0 <= i, i<new_part_1.size()), new_part_1[i] == part_1[i])))
        assertion(ForAll([i], Implies(And(0 <= i, i<new_part_2.size()), new_part_2[i] == part_2[i])))
            
        qubits = fresh_array("init_qubits", IntSort(), QubitStateType)
        j = fresh_int()
        result_new_part_1 = apply_circuit_on_qubit_state(qubits, new_part_1, new_part_1.size())
        result_new_part_2 = apply_circuit_on_qubit_state(qubits, new_part_2, new_part_2.size())
        result_part_1 = apply_circuit_on_qubit_state(qubits, part_1, part_1.size())
        result_part_2 = apply_circuit_on_qubit_state(qubits, part_2, part_2.size())

        result_new = apply_circuit_on_qubit_state(qubits, new_circuit, new_circuit.size())

        assertion(ForAll([qubits, j], result_new_part_1[j] == result_part_1[j]))
        assertion(ForAll([qubits, j], result_new_part_2[j] == result_part_2[j]))

        assertion(ForAll([qubits, j], Implies(ind==0, result_part_2[j] == result_new[j])))
        """
        """ 
        # Simply test
        certiq_prove(ForAll([j], apply_circuit_on_qubit_state(result_new_part_1, new_part_2, new_part_2.size())[j] ==
                                 apply_circuit_on_qubit_state(result_part_1, part_2, part_2.size())[j]))
        """
        """
        ind_size = fresh_int('size')
        assertion(ind_size == 1)
        ind_circ = QCircuit(size=ind_size, lemmas=False, name=self.name+str(x)+"remove_ind_circ") 

        ind_ind = fresh_int('ind')
        assertion(ind_ind == 0)
        assertion(ind_circ[ind_ind] == self[ind])
        
        mid_qubit_state = apply_circuit_on_qubit_state(result_part_1, ind_circ, ind_size)

        assertion(ForAll([qubits,j], apply_circuit_on_qubit_state(mid_qubit_state, part_2, part_2.size())[j] ==
                                     apply_circuit_on_qubit_state(qubits, self, self.size())[j]))
        """

        return new_circuit

    def push_front(self, gate):
        n = self.size()
        new_circuit = QCircuit()
        assertion(new_circuit.size() == n + 1)
        i = fresh_int()
        assertion(ForAll([i], Implies(And(1 <= i, i < new_circuit.size()), new_circuit[i] == self[i-1])))
        assertion(new_circuit[0] == gate)
        return new_circuit

    def partial_circuit(self, start, end):

        if isinstance(start, int) and isinstance(end, int) and end == start:
            return empty_circuit()
        
        try:
            certiq_prove(start==end, mute=True, msg="partial_circuit precondition for {}".format(self.name))
        except:
            pass
        else:
            return empty_circuit()

        out_circ_size = end - start
        out_circ = QCircuit(size=out_circ_size, name=self.name+"partial_circuit"+str(start)+str(end))

        i = fresh_int("partial_circuit")
        assertion(ForAll([i], Implies(And(i<end, i>=start), out_circ[i-start] == self[i])))

        qubits = fresh_array("init_qubit", IntSort(), QubitStateType)
        i = fresh_int()

        orig_result = apply_circuit_on_qubit_state(qubits, self, self.size())
        part_result = apply_circuit_on_qubit_state(qubits, self, start)
        result = apply_circuit_on_qubit_state(part_result, out_circ, out_circ.size())

        assertion(ForAll([qubits], result == orig_result))

        return out_circ

    def width(self):
        return fresh_int()

    def count_ops(self):
        return fresh_int()

    def count_ops_longest_path(self):
        return fresh_int()

    def num_tensor_factors(self):
        return fresh_int()

    def dag_longest_path(self):
        return fresh_int()
    
def empty_circuit():
        return QCircuit(size=0, name="empty_circuit")

def apply_circuit_on_qubit_state(qubits, circuit, t):
    return f_apply_circuit(qubits, circuit.gates, t)

def definition(qgate):

    ret_circ = QCircuit(name = "gatedef") 
    qubits = fresh_array("init_qubit", IntSort(), QubitStateType)
    k = fresh_int("k")

    self_result = apply_on_qubit_state(qubits, qgate)
    def_result = apply_circuit_on_qubit_state(qubits, ret_circ, ret_circ.size())
    
    assertion(ForAll([qubits, k], def_result[k] == self_result[k]))

    return ret_circ

def register_custom_definition(gate_name, gate_list):
    pass

def custom_definition(qgate):
    
    assertion(qgate.isMultiQGate())
    ret_circ = QCircuit(name = "gatedef") 
    qubits = fresh_array("init_qubit", IntSort(), QubitStateType)
    k = fresh_int("k")

    self_result = apply_on_qubit_state(qubits, qgate)
    def_result = apply_circuit_on_qubit_state(qubits, ret_circ, ret_circ.size())
    
    assertion(ForAll([qubits, k], def_result[k] == self_result[k]))

    return ret_circ

def decompose_with_basis(qgate, basis):
    
    assertion(qgate.isMultiQGate())
    ret_circ = QCircuit(name = "gatedef") 
    qubits = fresh_array("init_qubit", IntSort(), QubitStateType)
    k = fresh_int("k")

    self_result = apply_on_qubit_state(qubits, qgate)
    def_result = apply_circuit_on_qubit_state(qubits, ret_circ, ret_circ.size())
    
    assertion(ForAll([qubits, k], def_result[k] == self_result[k]))

    return ret_circ

def collect2Q():
    pass

def commutation():
    pass

def to_list(x):
    return list(x)

#######################
# "ForAll" variables
#######################

qubits = Array("any_qubits", IntSort(), QubitStateType)
circuit = Array("any_circuit_gates", IntSort(), GateType)
size = Int("any_circuit_size")
t = Int("n")


########################

def apply_part_circuit_on_qubit_state(qubits, circuit, m, n):

    l = circuit.size()
    # certiq_prove(n >= m, msg="Partial circuit symbolic execution precondition 1 for {}".format(circuit.name))
    # certiq_prove(n <= l, msg="Partial circuit symbolic execution precondition 2 for {}".format(circuit.name))


    return f_apply_part_circuit(qubits, circuit.gates, m, n)

f_apply_circuit = Function('apply_circuit', QubitType, CircuitType, IntSort(), QubitType)
f_apply_part_circuit = Function('apply_part_circuit', QubitType, CircuitType, IntSort(), IntSort(), QubitType)
# f_apply_circuit(qubits, circuit, 0) == qubits
assertion(ForAll([qubits, circuit], f_apply_circuit(qubits, circuit, 0) == qubits))

# f_apply_circuit(qubits, circuit, n) == apply_gate(f_apply_circuit(qubits, circuit, n-1), circuit[n-1])
assertion(ForAll([qubits, circuit, t], 
          Implies(t > 0,
                  f_apply_circuit(qubits, circuit, t) == 
                  apply_on_qubit_state(f_apply_circuit(qubits, circuit, t-1), 
                                       QGate.as_gate(circuit[t-1])))))
"""
assertion(ForAll([qubits, circuit], 
                  f_apply_circuit(qubits, circuit, 2) == 
                  apply_on_qubit_state(f_apply_circuit(qubits, circuit, 1), 
                                       QGate.as_gate(circuit[1]))))

assertion(ForAll([qubits, circuit], 
                  f_apply_circuit(qubits, circuit, 1) == 
                  apply_on_qubit_state(f_apply_circuit(qubits, circuit, 0), 
                                       QGate.as_gate(circuit[0]))))
"""
assertion(ForAll([qubits, circuit, t], 
                  Implies(GateType.gid(circuit[t-1])==0, 
                  f_apply_circuit(qubits, circuit, t) == 
                  apply_swap_on_qubit_state(f_apply_circuit(qubits, circuit, t-1), 
                                       QGate.as_gate(circuit[t-1])))))


# circuit lemmma

circuit0 = fresh_array("circuit_gates", IntSort(), GateType)
circuit1 = fresh_array("circuit_gates", IntSort(), GateType)
size = fresh_int("circuit_size")
size2 = fresh_int("circuit_size")

t = fresh_int()
i = fresh_int()

assertion(ForAll([qubits, circuit0, circuit1, t],
                  Implies(ForAll([i], Implies(And(i >= 0, i < t), circuit0[i] == circuit1[i])),
                  f_apply_circuit(qubits, circuit0, t) == f_apply_circuit(qubits, circuit1, t))))

assertion(ForAll([qubits, circuit0, circuit1, t],
                  Implies(circuit0 == circuit1,
                  f_apply_circuit(qubits, circuit0, t) == f_apply_circuit(qubits, circuit1, t))))






"""
# apply_circuit definition
qubits = Array("any_qubits", IntSort(), QubitStateType)
gates = Array("any_circuit_gates", IntSort(), GateType)
size = Int("any_circuit_size")
circuit = QCircuit(gates, size, lemmas=False)
t = Int("n")

# f_apply_circuit(qubits, circuit, 0) == qubits
assertion(ForAll([qubits, gates, size], f_apply_circuit(qubits, circuit.data, 0) == qubits))

# f_apply_circuit(qubits, circuit, n) == apply_gate(f_apply_circuit(qubits, circuit, n-1), circuit[n-1])
assertion(ForAll([qubits, gates, size, t], 
            Implies(And(t > 0, t <= size),
                    f_apply_circuit(qubits, circuit.data, t) == 
                    apply_on_qubit_state(f_apply_circuit(qubits, circuit.data, t-1), 
                                        QGate.as_gate(gates[t-1])))))

# f_apply_part_circuit definition
m = Int("any int")
assertion(ForAll([qubits, m, gates, size], f_apply_part_circuit(qubits, circuit.data, m, m) == qubits))

assertion(ForAll([qubits, gates, size, m, t], 
            Implies(And(t > m, t <= size),
                    f_apply_part_circuit(qubits, circuit.data, m, t) == 
                    apply_on_qubit_state(f_apply_part_circuit(qubits, circuit.data, m, t-1), 
                                        QGate.as_gate(gates[t-1])))))

assertion(ForAll([qubits, gates, size, m], 
    f_apply_part_circuit(qubits, circuit.data, 0, m) == f_apply_circuit(qubits, circuit.data, m)))

assertion(ForAll([qubits, gates, size, m], f_apply_part_circuit(f_apply_part_circuit(qubits, circuit.data, 0, m), circuit.data, m, circuit.size()) == f_apply_circuit(qubits, circuit.data, circuit.size())))
"""
"""
# test assertion

gs = Array("some circuit gates", IntSort(), GateType)
s = Int("Any circuit size")
c = QCircuit(gs, s)
a = Int('a')
i = Int('i')

certiq_prove(f_apply_part_circuit(f_apply_part_circuit(qubits, c.data, 0, a), c.data, a, c.size()) == f_apply_circuit(qubits, c.data, c.size()))
certiq_prove(ForAll([i], f_apply_part_circuit(f_apply_part_circuit(qubits, c.data, 0, a), c.data, a, c.size())[i] == f_apply_circuit(qubits, c.data, c.size())[i]))
certiq_prove(
ForAll([qubits, gates, size, m], f_apply_part_circuit(f_apply_circuit(qubits, circuit.data, m), circuit.data, m, circuit.size()) == f_apply_circuit(qubits, circuit.data, circuit.size())))

"""
"""
# circuit lemmma

qubits = fresh_array("qubits", IntSort(), QubitStateType)
gates = fresh_array("circuit_gates", IntSort(), GateType)
gates2 = fresh_array("circuit_gates", IntSort(), GateType)
size = fresh_int("circuit_size")
size2 = fresh_int("circuit_size")
circuit0 = CircuitType.new(gates, size)
circuit1 = CircuitType.new(gates2, size2)

t = fresh_int()
i = fresh_int()
a = fresh_int()
b = fresh_int()

assertion(ForAll([qubits, gates, gates2, size, size2, t],
                  Implies(ForAll([i], Implies(And(i >= 0, i < t), gates[i] == gates2[i])),
                  f_apply_circuit(qubits, circuit0, t) == f_apply_circuit(qubits, circuit1, t))))

assertion(ForAll([qubits, gates, gates2, size, size2, t],
                  Implies(ForAll([i], Implies(And(i >= size, i < size2, size <= size2), gates[i-size] == gates2[i])),
                  f_apply_circuit(qubits, circuit0, t) == f_apply_part_circuit(qubits, circuit1, size, t))))
"""
"""
# Not working

circ = QCircuit()
p_i = fresh_int()
p_j = fresh_int()
p_k = fresh_int()

assertion(And(p_i>=0, p_i<=p_j, p_j<=p_k, p_k<circ.size()))

part_i = circ.partial_circuit(p_i, p_j)
part_j = circ.partial_circuit(p_j, p_k)
part_k = circ.partial_circuit(p_i, p_k)

result_i = apply_circuit_on_qubit_state(qubits, part_i, part_i.size())
result_j = apply_circuit_on_qubit_state(result_i, part_j, part_j.size())
result_k = apply_circuit_on_qubit_state(qubits, part_k, part_k.size())

assertion(ForAll([circ.data, circ.size(), p_i, p_j, p_k, i], result_j[i] == result_k[i]))
"""
