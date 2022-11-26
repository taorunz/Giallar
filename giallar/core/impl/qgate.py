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

import qiskit.circuit.library.standard_gates.x 
import qiskit.circuit.library.standard_gates.y 
import qiskit.circuit.library.standard_gates.z
import qiskit.circuit.library.standard_gates.rx 
import qiskit.circuit.library.standard_gates.ry
import qiskit.circuit.library.standard_gates.rz
import qiskit.circuit.library.standard_gates.u1
import qiskit.circuit.library.standard_gates.u2
import qiskit.circuit.library.standard_gates.u3
import qiskit.circuit.library.standard_gates.h
import qiskit.circuit.library.standard_gates.t
import qiskit.circuit.library.standard_gates.s
import qiskit.circuit.library.standard_gates.swap 
import qiskit.circuit.library.standard_gates.iswap
import qiskit.circuit.library.standard_gates.ms
from qiskit.circuit.barrier import Barrier
from qiskit.circuit.measure import Measure
from qiskit.circuit.quantumregister import QuantumRegister

from giallar.gate_info import GateMasterDef

class QGate():

    def __init__(self, op, args, param = 0.):

        self.name = op.lower() # Gate name
        self.qubits = args
        self.id = -1
        self.param = param
        self.layer = 0 
        self.matrix = GateMasterDef(name = op, para = param)
        self.qiskit_info = {}

        self.initialize_qiskit_op()

        self.qiskit_info['compatible'] = True
        self.qiskit_info['qargs'] = []
        self.qiskit_info['cbit'] = None
        self.definition = []

        for wire in self.qubits:
            
            qiskit_qubit = qubit_string_to_qiskit_qubit(wire)
            if qiskit_qubit:
                self.qiskit_info['qargs'].append(qiskit_qubit)
            else:
                self.qiskit_info['compatible'] = False

    def is1QGate(self):
        return len(self.qubits) == 1

    def is2QGate(self):
        return len(self.qubits) == 2

    def isCXGate(self):
        return self.name in ["cx", "cnot"]

    def isMeasurement(self):
        return self.name == "measure"

    def isBarrier(self):
        return self.name == "barrier"

    def isDiagonal(self):
        return self.name in ['z', 'rz', 't', 's', 'u1']

    def isMultiQGate(self):
        return len(self.qubits) > 2

    def isRotationGate(self):
        return self.name in ['u1', 'u2', 'u3']

    def hasDefinition(self):
        return len(self.definition) > 0

    def param(self):
        return self.param

    def definition(self):
        return self.qiskit_info['op'].definition.data

    def __copy__(self):

        n_qg = QGate(self.name, self.wires, param=self.param)

        return n_qg

    def initialize_qiskit_op(self):

        if self.name.lower() == 'swap':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.swap.SwapGate()

        if self.name.lower() == 'ms':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.ms.MSGate()

        if self.name.lower() == 'iswap':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.iswap.iSwapGate()

        if self.name.lower() == 'barrier':
            self.qiskit_info['op'] = qiskit.circuit.barrier.Barrier(len(self.qubits))

        if self.name.lower() in ['cx', 'cnot']:
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.x.CXGate()

        if self.name.lower() == 'cy':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.y.CYGate()

        if self.name.lower() == 'cz':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.z.CZGate()

        if self.name.lower() == 'x':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.x.XGate()

        if self.name.lower() == 'y':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.y.YGate()

        if self.name.lower() == 'z':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.z.ZGate()

        if self.name.lower() == 'h':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.h.HGate()

        if self.name.lower() == 't':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.t.TGate()

        if self.name.lower() == 's':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.s.SGate()

        if self.name.lower() == 'rx':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.rx.RXGate(self.param)

        if self.name.lower() == 'ry':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.ry.RYGate(self.param)

        if self.name.lower() == 'rz':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.rz.RZGate(self.param)

        if self.name.lower() == 'u1':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.u1.U1Gate(self.param)

        if self.name.lower() == 'u2':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.u2.U2Gate(*self.param)

        if self.name.lower() == 'u3':
            self.qiskit_info['op'] = qiskit.circuit.library.standard_gates.u3.U3Gate(*self.param)

        if self.name.lower() == 'measure':
            self.qiskit_info['op'] = qiskit.circuit.measure.Measure()

        return

class SwapGate(QGate):
    def __init__(self, op1, op2):
        super().__init__("swap", [op1, op2])


class IdGate(QGate):
    def __init__(self, op1):
        super().__init__("id", [op1])

class U1Gate(QGate):
    def __init__(self, op, angle):
        super().__init__("u1", [op], param=angle)

class U2Gate(QGate):
    def __init__(self, op, angle):
        super().__init__("u2", [op], param=angle)

class U3Gate(QGate):
    def __init__(self, op, angle):
        super().__init__("u3", [op], param=angle)

class X(QGate):
    def __init__(self, op):
        super().__init__("x", [op])

class Y(QGate):
    def __init__(self, op):
        super().__init__("y", [op])

class Z(QGate):
    def __init__(self, op):
        super().__init__("z", [op])

class H(QGate):
    def __init__(self, op):
        super().__init__("h", [op])

class S(QGate):
    def __init__(self, op):
        super().__init__("s", [op])

class T(QGate):
    def __init__(self, op):
        super().__init__("t", [op])

class RXGate(QGate):
    def __init__(self, op, angle):
        super().__init__("rx", [op], param=angle)

class RYGate(QGate):
    def __init__(self, op, angle):
        super().__init__("ry", [op], param=angle)

class RZGate(QGate):
    def __init__(self, op, angle):
        super().__init__("rz", [op], param=angle)

class CNOTGate(QGate):
    def __init__(self, op1, op2):
        super().__init__("cnot", [op1, op2])

class CYGate(QGate):
    def __init__(self, op1, op2):
        super().__init__("cy", [op1, op2])

class CZGate(QGate):
    def __init__(self, op1, op2):
        super().__init__("cz", [op1, op2])

class MSGate(QGate):
    def __init__(self, op1, op2):
        super().__init__("ms", [op1, op2])

class ISWAPGate(QGate):
    def __init__(self, op1, op2):
        super().__init__("iswap", [op1, op2])

class Barrier(QGate):
    def __init__(self, ops):
        super().__init__("barrier", ops)

class Measure(QGate):
    def __init__(self, op):
        super().__init__("measure", [op])

class UnitaryGate(QGate):
    def __init__(self, op1, op2, matrix):
        super().__init__("unitary", [op1, op2])
        self.matrix = matrix
class Reset(QGate):
    def __init__(self, op):
        super().__init__("reset", [op])
    

def qubit_string_to_qiskit_qubit(st):
    # print(st)
    if not isinstance(st, str):
        st = str(st)

    match = re.compile("(\w+)\(QuantumRegister\((\d+),\s'(\w+)'\),\s(\d+)").search(st)
    
    if match and match.group(1) == "Qubit":

        q = QuantumRegister(int(match.group(2)), name = match.group(3))
        return q[int(match.group(4))]
    
    else:
        return None
