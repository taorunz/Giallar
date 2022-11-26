
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

from giallar.core.impl.qgate import *

from qiskit.dagcircuit.dagcircuit import DAGCircuit
from qiskit.dagcircuit.dagnode import DAGNode
from qiskit.circuit.quantumregister import QuantumRegister, Qubit

# from qiskit.circuit.library.standard_gates.x import XGate, CXGate
# from qiskit.circuit.library.standard_gates.y import YGate
# from qiskit.circuit.library.standard_gates.z import ZGate
# from qiskit.circuit.library.standard_gates.h import HGate
# from qiskit.circuit.library.standard_gates.t import TGate
# from qiskit.circuit.library.standard_gates.s import SGate
# from qiskit.circuit.library.standard_gates.swap import SwapGate
# from qiskit.circuit.library.standard_gates.iswap import iSwapGate
from qiskit.circuit.library.standard_gates.ms import MSGate
# from qiskit.circuit.barrier import Barrier
from qiskit.circuit.reset import Reset

def qiskit_node_to_certiq_gate(node):
    
    if node.type != "op":
        return None
        
    if node.name == 'swap':        
        ret_gate = SwapGate(node.qargs[0].__repr__(), node.qargs[1].__repr__())
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0], node.qargs[1]]
        return ret_gate
         
    if node.name == 'cx':        
        ret_gate =  CNOTGate(node.qargs[0].__repr__(), node.qargs[1].__repr__())
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0], node.qargs[1]]
        return ret_gate

    if node.name == 'cy':        
        ret_gate =  CYGate(node.qargs[0].__repr__(), node.qargs[1].__repr__())
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0], node.qargs[1]]
        return ret_gate


    if node.name == 'cz':        
        ret_gate =  CZGate(node.qargs[0].__repr__(), node.qargs[1].__repr__())
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0], node.qargs[1]]
        return ret_gate


    if node.name == 'iswap':        
        ret_gate =  ISWAPGate(node.qargs[0].__repr__(), node.qargs[1].__repr__())
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0], node.qargs[1]]
        return ret_gate


    if node.name == 'ms':        
        ret_gate =  MSGate(node.qargs[0].__repr__(), node.qargs[1].__repr__())
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0], node.qargs[1]]
        return ret_gate

    if node.name == 'barrier':
        ret_gate = Barrier([x.__repr__() for x in node.qargs])
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0], node.qargs[1]]
        return ret_gate

    if node.name == 'x':
        ret_gate =  X(node.qargs[0].__repr__())
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0]]
        return ret_gate

    if node.name == 'y':
        ret_gate =  Y(node.qargs[0].__repr__())
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0]]
        return ret_gate

    if node.name == 'z':
        ret_gate =  Z(node.qargs[0].__repr__())
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0]]
        return ret_gate

    if node.name == 't' or node.name == 'tdg':
        ret_gate =  T(node.qargs[0].__repr__())
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0]]
        return ret_gate

    if node.name == 's':
        ret_gate =  S(node.qargs[0].__repr__())
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0]]
        return ret_gate

    if node.name == 'h':
        ret_gate =  H(node.qargs[0].__repr__())
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0]]
        return ret_gate

    if node.name == 'rx': 
        ret_gate =  RXGate(node.qargs[0].__repr__(), node.op.params[0])
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0]]
        ret_gate.qiskit_info['params'] = node.op.params
        return ret_gate

    if node.name == 'ry': 
        ret_gate =  RYGate(node.qargs[0].__repr__(), node.op.params[0])
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        #  ret_gate.qiskit_info['qargs'] = [node.qargs[0]]
        ret_gate.qiskit_info['params'] = node.op.params
        return ret_gate
    
    if node.name == 'rz': 
        ret_gate =  RZGate(node.qargs[0].__repr__(), node.op.params[0])
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0]]
        ret_gate.qiskit_info['params'] = node.op.params
        return ret_gate

    if node.name == 'u1': 
        ret_gate =  U1Gate(node.qargs[0].__repr__(), node.op.params[0])
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0]]
        ret_gate.qiskit_info['params'] = node.op.params
        return ret_gate

    if node.name == 'u2': 
        ret_gate =  U2Gate(node.qargs[0].__repr__(), node.op.params)
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0]]
        ret_gate.qiskit_info['params'] = node.op.params
        return ret_gate

    if node.name == 'u3': 
        ret_gate =  U2Gate(node.qargs[0].__repr__(), node.op.params)
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0]]
        ret_gate.qiskit_info['params'] = node.op.params
        return ret_gate
    
    if node.name == 'measure':
        ret_list = []
        for i, qarg in enumerate(node.qargs):
            ret_gate = Measure(qarg.__repr__())
            ret_gate.qiskit_info['op'] = node.op
            ret_gate.qiskit_info['cbit'] = node.cargs[i]
            ret_gate.qiskit_info['params'] = node.op.params
            ret_list.append(ret_gate)
            
        return ret_list
    
    if node.name == 'id': 
        ret_gate =  IdGate(node.qargs[0].__repr__())
        # ret_gate.qiskit_info['compatible'] = True
        ret_gate.qiskit_info['op'] = node.op
        # ret_gate.qiskit_info['qargs'] = [node.qargs[0]]
        return ret_gate

    ret_gate = QGate(node.name, [x.__repr__() for x in node.qargs], node.op.params)
    ret_gate.qiskit_info['op'] = node.op
    ret_gate.qiskit_info['params'] = node.op.params
    return ret_gate

def dag_to_certiq_circ(dag):
    
    qubits = []
    for registername, register in dag.qregs.items():
        for i in range(register.size):
            qubits.append(Qubit(register, i).__repr__())
    
    from giallar.core.impl.qcircuit import QCircuit

    qcirc = QCircuit(qubits=qubits)
    qcirc.name = dag.name

    qcirc.qiskit_registers = dag.qregs
    qcirc.qiskit_cregisters = dag.cregs

    for node in dag.topological_op_nodes():
        ng = qiskit_node_to_certiq_gate(node)
        if not isinstance(ng, list):
            qcirc.append(ng)
        else:
            for gate in ng:
                qcirc.append(gate)

    return qcirc

def certiq_circ_to_dag(qcirc):

    dag = DAGCircuit()
    dag.name = qcirc.name
    #print(qcirc.qiskit_registers)
    #dag.qregs = qcirc.qiskit_registers
    #dag.cregs = qcirc.qiskit_cregisters
    
    for register in qcirc.qiskit_registers.keys():
        dag.add_qreg(qcirc.qiskit_registers[register])

    for register in qcirc.qiskit_cregisters.keys():
       dag.add_creg(qcirc.qiskit_cregisters[register])
    
    for i, gate in enumerate(qcirc.gate_list):
        # print(gate.name, gate.qubits, gate.qiskit_info['compatible'])
        if not gate.qiskit_info['compatible']:
            print(gate.qubits)
            raise TypeError("There's a gate in the circuit that's not compatible with Qiskit.") 

        op = gate.qiskit_info['op']
        qargs = gate.qiskit_info['qargs']
        if gate.qiskit_info['cbit']:
            cargs = gate.qiskit_info['cbit']
            if not isinstance(cargs, list):
                cargs = [cargs]
            # print(cargs)
        else:
            cargs = None
        
        dag.apply_operation_back(op, qargs=qargs, cargs=cargs)

    return dag

