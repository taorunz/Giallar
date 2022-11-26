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
from copy import deepcopy
# from IPython import embed

from giallar.z3_wrapper import *
from giallar.gate_info import gate_info

QubitStateType = DeclareSort("QubitState")
QubitType = ArraySort(IntSort(), QubitStateType)

GateType = Datatype('Gate')
GateType.declare('new',('gid', IntSort()), ('arg0', IntSort()),  ('arg1', IntSort()), ('arg2', IntSort()),  ('param', RealSort()))
GateType = GateType.create()

MAX_GATE_ID = 20
Z_ROTATION = 6
X_ROTATION = 7

def gid(name): return gate_info[name]['id']

gate_argn = Array("gate_argn", IntSort(), IntSort())
gate_type = Array("gate_type", IntSort(), IntSort())

for name, info in gate_info.items():
    assertion(gate_argn[info['id']] == info['argn'])
    assertion(gate_type[info['id']] == info['type'])

class QGate:
    def __init__(self, gid, args, param=0):

        arg0 = args[0]
        if len(args) == 1:
            arg1 = arg0
            arg2 = arg0
        elif len(args) == 2:
            arg1 = args[1]
            arg2 = arg1
        elif len(args) == 3:
            arg1 = args[1]
            arg2 = args[2]
        else:
            raise NotImplementedError

        self.data = GateType.new(gid, arg0, arg1, arg2, param)
        self.param = param
        self.qubits = [self.arg(0), self.arg(1)]
        
    @classmethod
    def as_gate(cls, gate_data):
        return cls(GateType.gid(gate_data),
                    [GateType.arg0(gate_data),
                    GateType.arg1(gate_data)],
                    GateType.param(gate_data))

    def is1QGate(self):
        return GateType.arg0(self.data) == GateType.arg1(self.data)
    
    def is2QGate(self):
        return GateType.arg0(self.data) != GateType.arg1(self.data)

    def isMultiQGate(self):
        return GateType.arg1(self.data) != GateType.arg2(self.data)

    def isUnrollable(self):
        return And(fresh_bool(), self.isMultiQGate())
    
    def hasDefinition(self):
        return fresh_bool()
 
    def gid(self):
        return GateType.gid(self.data)

    @property
    def name(self):
        return GateType.gid(self.data)

    def argn(self):
        return gate_argn[self.gid()]

    def arg(self, index):
        if index == 0:
            return GateType.arg0(self.data)
        elif index == 1:
            return GateType.arg1(self.data)
        elif index == 2:
            return GateType.arg2(self.data)
        else:
            return None

    def isMeasurement(self):
        return GateType.gid(self.data) == 16

    def isBarrier(self):
        return GateType.gid(self.data) == 13

    def isReset(self):
        return GateType.gid(self.data) == 17
    
    def isCXGate(self):
        qubits = fresh_array("init_qubit", IntSort(), QubitStateType)
        from giallar.core.spec.qcircuit import empty_circuit, apply_circuit_on_qubit_state, apply_on_qubit_state
        k = fresh_int("k")
        q0 = self.arg(0)
        q1 = self.arg(1)
        ret_circ = empty_circuit()
        ret_circ = ret_circ.append(HGate(q0))
        ret_circ = ret_circ.append(HGate(q1))
        ret_circ = ret_circ.append(CNOTGate(q1, q0))
        ret_circ = ret_circ.append(HGate(q0))
        ret_circ = ret_circ.append(HGate(q1))
        self_result = apply_on_qubit_state(qubits, self)
        def_result = apply_circuit_on_qubit_state(qubits, ret_circ, ret_circ.size())

        assertion(Implies(GateType.gid(self.data) == 1, ForAll([qubits, k], def_result[k] == self_result[k])))
        return GateType.gid(self.data) == 1
    
    def isECRGate(self):
        qubits = fresh_array("init_qubit", IntSort(), QubitStateType)
        from giallar.core.spec.qcircuit import empty_circuit, apply_circuit_on_qubit_state, apply_on_qubit_state
        k = fresh_int("k")
        q0 = self.arg(0)
        q1 = self.arg(1)
        ret_circ = empty_circuit()
        ret_circ = ret_circ.append(HGate(q0))
        ret_circ = ret_circ.append(HGate(q1))
        ret_circ = ret_circ.append(CNOTGate(q1, q0))
        ret_circ = ret_circ.append(HGate(q0))
        ret_circ = ret_circ.append(HGate(q1))
        self_result = apply_on_qubit_state(qubits, self)
        def_result = apply_circuit_on_qubit_state(qubits, ret_circ, ret_circ.size())

        assertion(Implies(GateType.gid(self.data) == 1, ForAll([qubits, k], def_result[k] == self_result[k])))
        return GateType.gid(self.data) == 1
    
    def isRZXGate(self):
        qubits = fresh_array("init_qubit", IntSort(), QubitStateType)
        from giallar.core.spec.qcircuit import empty_circuit, apply_circuit_on_qubit_state, apply_on_qubit_state
        k = fresh_int("k")
        q0 = self.arg(0)
        q1 = self.arg(1)
        ret_circ = empty_circuit()
        ret_circ = ret_circ.append(HGate(q0))
        ret_circ = ret_circ.append(HGate(q1))
        ret_circ = ret_circ.append(CNOTGate(q1, q0))
        ret_circ = ret_circ.append(HGate(q0))
        ret_circ = ret_circ.append(HGate(q1))
        self_result = apply_on_qubit_state(qubits, self)
        def_result = apply_circuit_on_qubit_state(qubits, ret_circ, ret_circ.size())

        assertion(Implies(GateType.gid(self.data) == 1, ForAll([qubits, k], def_result[k] == self_result[k])))
        return GateType.gid(self.data) == 1

    def isDiagonal(self):
        return Or(
                  GateType.gid(self.data) == 6,
                  GateType.gid(self.data) == 7,
                  GateType.gid(self.data) == 8,
                  GateType.gid(self.data) == 9,
                  GateType.gid(self.data) == 10)

    def isRotationGate(self):
        return Or(
                  GateType.gid(self.data) == 4,
                  GateType.gid(self.data) == 5,
                  GateType.gid(self.data) == 6,
                  GateType.gid(self.data) == 7,
                  GateType.gid(self.data) == 8,
                  GateType.gid(self.data) == 9,
                  GateType.gid(self.data) == 10,
                  GateType.gid(self.data) == 11,
                  GateType.gid(self.data) == 12,
                  GateType.gid(self.data) == 18,
                  GateType.gid(self.data) == 19,
                  GateType.gid(self.data) == 20)


    def param(self):
        return GateType.param(self.data)

    def __eq__(self, gateb):
        return self.data == gateb.data

    def qiskit_info(self):
        return None

class SwapGate(QGate):
    def __init__(self, op1, op2):
        gid = gate_info["swap"]["id"]
        self.data = GateType.new(gid, op1, op2, op2, RealVal(0))

    def is2QGate(self): return True

class CNOTGate(QGate):
    def __init__(self, op1, op2):
        gid = gate_info["cnot"]["id"]
        self.data = GateType.new(gid, op1, op2, op2, RealVal(0))

    def is2QGate(self): return True

class ECRGate(QGate):
    def __init__(self, op1, op2):
        gid = gate_info["cnot"]["id"]
        self.data = GateType.new(gid, op1, op2, op2, RealVal(0))

    def is2QGate(self): return True

class RZXGate(QGate):
    def __init__(self, op1, op2):
        gid = gate_info["cnot"]["id"]
        self.data = GateType.new(gid, op1, op2, op2, RealVal(0))

    def is2QGate(self): return True

class HGate(QGate):
    def __init__(self, op):
        gid = gate_info["h"]["id"]
        self.data = GateType.new(gid, op, op, op, RealVal(0))

class U1Gate(QGate):
    def __init__(self, op, angle):
        gid = gate_info["u1"]["id"]
        self.data = GateType.new(gid, op, op, op, angle)

    def is2QGate(self): return False

class RXGate(QGate):
    def __init__(self, op, angle):
        gid = gate_info["rx"]["id"]
        self.data = GateType.new(gid, op, op, op, angle)

    def is2QGate(self): return False

class RZGate(QGate):
    def __init__(self, op, angle):
        gid = gate_info["rz"]["id"]
        self.data = GateType.new(gid, op, op, op, angle)

    def is2QGate(self): return False

class Measure(QGate):
    def __init__(self, qbit, cbit):
        gid  = gate_info["measure"]["id"]
        self.data = GateType.new(gid, op, op, op, RealVal(0)) 

class Barrier(QGate):
    def __init__(self, op):
        gid  = gate_info["barrier"]["id"]
        self.data = GateType.new(gid, op, op, op, RealVal(0))

def valid_gate(gate):
    return And(gate.gid() >= 0, gate.gid() <= MAX_GATE_ID)
"""
emul_gate = Function('emul_gate', IntSort(), QubitStateType, QubitStateType)
emul_gate_1 = Function('emul_gate_1', IntSort(), QubitStateType, QubitStateType,QubitStateType, QubitStateType)
emul_gate_2 = Function('emul_gate_2', IntSort(), QubitStateType, QubitStateType, QubitStateType, QubitStateType)
emul_gate_3 = Function('emul_gate_3', IntSort(), QubitStateType, QubitStateType, QubitStateType, QubitStateType)

def apply_on_qubit_state(qubits, gate):
    gid = gate.gid()  # gate's name
    op1 = gate.arg(0)   # 1st logical operand
    op2 = gate.arg(1)   # 2nd logical operand
    op3 = gate.arg(2)   # 3rd logical operand

    out1 = If(gid == 0, qubits[op2],
                emul_gate_1(gid, qubits[op1], qubits[op2], qubits[op3]))  # 1st gate's output
    out2 = If(gid == 0, qubits[op1],
                emul_gate_2(gid, qubits[op1], qubits[op2], qubits[op3]))  # 2nd gate's output
    out = emul_gate(gid, qubits[op1])
    qubits = If(gate.argn() == 2, Store(qubits, op1, out1), Store(qubits, op1, out))
    qubits = If(gate.argn() == 2, Store(qubits, op2, out2), qubits)
    qubits = If(gate.argn() == 3, Store(qubits, op2, emul_gate(gid, qubits[op2])), qubits)
    qubits = If(gate.argn() == 3, Store(qubits, op3, emul_gate(gid, qubits[op3])), qubits)

    return qubits

def share_wire(gate1, gate2):
    # This function only has to consider 1q and 2q gates
    return Or(gate1.arg(0) == gate2.arg(0),
              And(gate2.argn() == 2, gate1.arg(0) == gate2.arg(1)),
              And(gate1.argn() == 2, gate1.arg(1) == gate2.arg(0)), 
              And(gate1.argn() == 2, gate2.argn() == 2, gate1.arg(1) == gate2.arg(1)))

"""
