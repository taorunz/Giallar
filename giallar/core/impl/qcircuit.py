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

import re
from collections import OrderedDict
from giallar.gate_info import *
from giallar.core.impl.error_handler import raise_error
from qiskit.circuit.quantumregister import QuantumRegister, Qubit
from copy import deepcopy


class QCircuit(object):
    """
    - Circuit class for the CertiQ compilation functionality
    - and denotational semantics
    """

    def __init__(self, qubits=None, gates=None, size=None):

        self.name = ""
        self.qubits = qubits if qubits is not None else []
        self.gates_on_qubits = {} # Maintain the list of gates on each qubit
        self.qbit2idx = {} # Indexing the qubits

        for qubit_num, qubit in enumerate(self.qubits):
            self.gates_on_qubits[qubit] = []
            self.qbit2idx[qubit] = qubit_num + 1

        self.gate_list = []
        self.layers = []
        self.layer_dict = dict()

        self.qiskit_registers = OrderedDict()
        self.qiskit_cregisters = OrderedDict()

    def __eq__(self, qc):

        self.apply_circuit() == qc.apply_circuit()

    def copy(self):
        return deepcopy(self)

    def width(self):
        return len(self.qubits)

    def depth(self):
        return len(self.layers)

    def size(self):
        return len(self.gate_list)

    def count_ops(self):
        op_dict = {}
        for g in self.gate_list:
            name = g.name
            if name not in op_dict:
                op_dict[name] = 1
            else:
                op_dict[name] += 1
        return op_dict

    def num_tensor_factors(self):
        from giallar.qiskit_wrapper.converter import certiq_circ_to_dag

        qc = certiq_circ_to_dag(self)
        return qc.num_tensor_factors()

    def count_ops_longest_path(self):
        from giallar.qiskit_wrapper.converter import certiq_circ_to_dag

        qc = certiq_circ_to_dag(self)
        return qc.count_ops_longest_path()

    def append(self, qgate):

        # print('In QCircuit.append')
        if qgate.name == "id":

            return self


        self.gate_list.append(qgate)
        self.layer_dict[len(self.gate_list)-1] = 1
        
        for qb in qgate.qubits:
            if qb not in self.qubits:
                """
                error_msg = (qb, qgate.id, qgate.name + " " + qb)
                raise_error('CertiQ compilation error: no qubit {0} for gate # {1}: {2}'\
                         .format(error_msg[0], error_msg[1], error_msg[2]))
                """
                self.qubits.append(qb)
                self.gates_on_qubits[qb] = []
                self.qbit2idx[qb] = len(self.qubits)

            if len(self.gates_on_qubits[qb]) == 0:
                layer = 1

            else:
                last_gate = self.gate_list[self.gates_on_qubits[qb][-1]]
                layer = self.layer_dict[self.gates_on_qubits[qb][-1]] + 1


            self.gates_on_qubits[qb].append(len(self.gate_list)-1)

            if layer > self.layer_dict[len(self.gate_list)-1]:
                self.layer_dict[len(self.gate_list)-1] = layer
            if layer > len(self.layers):
                self.layers.append([])
            
            if len(self.gate_list)-1 not in self.layers[self.layer_dict[len(self.gate_list)-1]-1]:
                self.layers[self.layer_dict[len(self.gate_list)-1]-1].append(len(self.gate_list)-1)
        
            # print('qb:', qb)
            if not isinstance(qb, str):
                sqb = str(qb)
            else:
                sqb = qb
            match = re.compile("(\w+)\(QuantumRegister\((\d+),\s'(\w+)'\),\s(\d+)").search(sqb)
            # print('sqb:', sqb)
            
            if match and match.group(1) == "Qubit":

                q = QuantumRegister(int(match.group(2)), name = match.group(3))

                if match.group(3) not in self.qiskit_registers:
                    self.qiskit_registers[match.group(3)] = q
        
        return self
    
    def simplify_qubits(self):
        self.qiskit_qubit = {}
        self.simplified_qubit = {}
        for i, qb in enumerate(self.qubits):
            self.qiskit_qubit[i] = qb
            self.simplified_qubit[qb] = i
        
        for gate in self.gate_list:
            gate.qubits = [self.simplified_qubit[qb] for qb in gate.qubits]
        self.qiskit_qubits = gate.qubits
        self.qubits = [i for i in range(len(self.qubits))]
        self.gates_on_qubits = {self.simplified_qubit[qb] : gates for qb, gates in self.gates_on_qubits.items()}

    def apply_qcircuit(self):
        # Calculate the detonational semantics of the circuit,
        # i.e., the matrix representation
        
        return Simulator.apply_circuit(self)

    def __getitem__(self, i):
        return self.gate_list[i]

    def direct_successors(self, ind):
        
        ds = dict()
        gate = self.gate_list[ind]
        
        ds['gates'] = QCircuit()
        ds['indices'] = []
          
        candidates = []
        for q in gate.qubits:
            # print(self.gates_on_qubits)
            qi = self.gates_on_qubits[q].index(ind)

            if qi == len(self.gates_on_qubits[q]) - 1:
                continue

            else:
                suc_gate = self.gate_list[self.gates_on_qubits[q][qi+1]]
                if gate.is1QGate() or suc_gate.is1QGate():
                    ds['gates'].append(suc_gate)
                    ds['indices'].append(self.gates_on_qubits[q][qi+1])

                else:
                    if len(shared_qubits(gate, suc_gate)) == 1:
                        ds['gates'].append(suc_gate)
                        ds['indices'].append(self.gates_on_qubits[q][qi+1])
                    else:
                        candidates.append(self.gates_on_qubits[q][qi+1])

        for i in candidates:
            if_ds = True
            for q in shared_qubits(gate, self.gate_list[i]):
                qi = self.gates_on_qubits[q].index(ind)
                qds = self.gates_on_qubits[q].index(i)
                if qi + 1 != qds:
                    if_ds = False
            if if_ds:
                ds['gates'].append(self.gate_list[i])
                ds['indices'].append(i)

        ds['if_successful'] = True if ds['gates'].size() > 0 else False

        return ds
    
    def successors(self, ind):
        return self.direct_successors(ind)['indices']
    
    def has_direct_successors(self, i):
        return self.direct_successors(i)['if_successful']

    def canceltwo(self, x1, x2):
        pass

    def extend(self, qcirc):

        for qgate in qcirc:
            self.append(qgate)
        
        return self  

    def remove(self, i):
        
        if i>=self.size() or i<0:
            raise_error("Invalid index to remove for circuit.")

        ret_circuit = QCircuit()

        for j in range(0, i):
            ret_circuit.append(self[j])
        
        for j in range(i+1, self.size()):
            ret_circuit.append(self[j])
        
        return ret_circuit

    def isOnlyMeasurements(self):
        
        for g in self.gate_list:
            if g.name != "measure":
                return False

        return True


    def isDiagonalBeforeMeasurements(self, i):
        return self[i].isDiagonal() and self[i].direct_successors()['gates'].ifOnlyMeasurements()

    def isOnlyMeasurements(self):
        return all([x.isMeasurements() for x in self.gate_list])

    def is_empty(self):
        return len(self.gate_list) == 0

    def cx(self, ctrl, targ):
        from giallar.core.impl.qgate import CNOTGate
        return self.append(CNOTGate(ctrl, targ))

    def cy(self, ctrl, targ):
        from giallar.core.impl.qgate import CYGate
        return self.append(CYGate(ctrl, targ))

    def cz(self, ctrl, targ):
        from giallar.core.impl.qgate import CZGate
        return self.append(CZGate(ctrl, targ))

    def swap(self, op1, op2):
        from giallar.core.impl.qgate import SwapGate
        return self.append(SwapGate(op1, op2))

    def rz(self, op):
        from giallar.core.impl.qgate import RZGate
        return self.append(RZGate(op))

    def rx(self, op):
        from giallar.core.impl.qgate import RXGate
        return self.append(RXGate(op))

    def measure(self, op):
        from giallar.core.impl.qgate import Measure
        return self.append(Measure(op))
    
    def front_layer(self):
        used_qubits = set()
        front = []
        for i, gate in enumerate(self.gate_list):
            if len(used_qubits.intersection(gate.qubits)) > 0:
                front.append((i, gate))
            used_qubits.update(gate.qubits)
        return front



def empty_circuit():
    return QCircuit()

def shared_qubits(g1, g2):
    q1 = g1.qubits
    q2 = g2.qubits
    return list(set(q1).intersection(set(q2)))

def to_list(x):
    return list(x)

def empty_set():
    return set()

def to_tuple(x):
    return tuple(x)

def empty_frozenset(x):
    return frozenset(x)

def empty_dict(x):
    return dict(x)

def length(x):
    return len(x)
