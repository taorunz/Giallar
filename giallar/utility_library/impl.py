from giallar.core.impl.error_handler import raise_error
from giallar.core.impl.qgate import U1Gate, U2Gate, U3Gate, IdGate, QGate, UnitaryGate
from giallar.core.impl.qcircuit import QCircuit, empty_circuit
from giallar.core.impl.layout import Layout
from giallar.gate_info import GateMasterDef, flip_matrix
from qiskit.quantum_info import Quaternion
import numpy as np
import networkx as nx

_CHOP_THRESHOLD = 1E-4

def next_gate(circ, x):
    for i in range(x + 1, circ.size()):
        if len(set(circ[i].qubits).intersection(circ[x].qubits)) >= 1:
            return i
    return -1

def shortest_undirected_path(coupling_map, physical_qubit1, physical_qubit2):
    try:
        return nx.shortest_path(coupling_map.graph.to_undirected(as_view=True), source=physical_qubit1,
                                target=physical_qubit2)
    except nx.exception.NetworkXNoPath:
        raise raise_error(
            "Nodes %s and %s are not connected" % (str(physical_qubit1), str(physical_qubit2)))

def apply_swap(circ, perm, swap, layout, coup):
    q0 = layout._p2v[swap[0]]
    q1 = layout._p2v[swap[1]]
    circ.swap(q0, q1)
    perm.swap(q0, q1)
    return circ, perm

def update_layout_with_perm(initial_layout, perm):
    layout = Layout()
    for keys in initial_layout._v2p:
        p_key = initial_layout._v2p[keys]
        layout._v2p[perm._n2i[keys]] = p_key
        layout._p2v[p_key] = perm._n2i[keys]
    return layout

def map_free_gates(gates_remaining, new_circ, layout, current_perm, coupling_map):
    # print(current_perm._i2n)
    blocked_qubits = set()
    remaining_gates = empty_circuit()
    for gate in gates_remaining:
        if gate.isBarrier():
            new_gate = QGate(gate.name, [current_perm._i2n[q] for q in gate.qubits], param=gate.param)
            new_circ = new_circ.append(new_gate)
            continue
        if gate.isMultiQGate():
            raise_error(f"The input circuit gate {gate.name} is not unrolled.")
        if blocked_qubits.intersection(gate.qubits):
            blocked_qubits.update(gate.qubits)
            remaining_gates = remaining_gates.append(gate)
        elif gate.is1QGate():
            new_gate = QGate(gate.name, [current_perm._i2n[gate.qubits[0]]], param=gate.param)
            new_circ = new_circ.append(new_gate)
            # print(f"mapped {new_gate.name} {new_gate.qubits}")
        else:
            phys0 = layout[current_perm._i2n[gate.qubits[0]]]
            phys1 = layout[current_perm._i2n[gate.qubits[1]]]
            if coupling_map.distance(phys0, phys1) == 1:
                new_gate = QGate(gate.name, [current_perm._i2n[gate.qubits[0]], current_perm._i2n[gate.qubits[1]]], param=gate.param)
                new_circ = new_circ.append(new_gate)
                # print(f"mapped {gate.name} {gate.qubits} -> {new_gate.qubits}")
            else:
                blocked_qubits.update(gate.qubits)
                # print(f"failed {gate.name} {gate.qubits}")
                remaining_gates = remaining_gates.append(gate)
    return new_circ, remaining_gates

def swap_along_a_path(circ, perm, layout, path):
    l = len(path)
    for i in range(l-2):
        v0 = layout._p2v[path[i]]
        v1 = layout._p2v[path[i+1]]
        circ.swap(v0, v1)
        perm.swap(v0, v1)
    return circ, perm

def merge_1q_gates(g1, g2):
    gate_name = ""
    if not (g1.isRotationGate() and g2.isRotationGate()):
        raise_error("merge_1q_gates invalid parameters. Rotation gates required.")
    if g1.name == "u1" and g2.name == "u1":
        new_angle = g1.param + g2.param
        gate_name = "u1"
    elif g1.name == "u1" and g2.name == "u2":
        new_angle = [g1.param+g2.param[0], g2.param[1]]
        gate_name = "u2"
    elif g1.name == "u2" and g2.name == "u1":
        new_angle = [g2.param+g1.param[0], g1.param[1]]
        gate_name = "u2"
    elif g1.name == "u1" and g2.name == "u3":
        new_angle = [g2.param[0], g1.param + g2.param[1], g2.param[2]]
        gate_name = "u3" 
    elif g1.name == "u3" and g2.name == "u1":
        new_angle = [g1.param[0], g2.param + g1.param[1], g1.param[2]]
        gate_name = "u3"
    elif g1.name == "u2" and g2.name == "u2":
        new_angle = [np.pi - g1.param[1] - g2.param[0], g1.param[0] + np.pi * 0.5, g2.param[1]  + 0.5 * np.pi]
        gate_name = "u3"
    else:
        g1_angle = g1.param if len(g1.param) == 3 else [0.0] + g1.param
        g2_angle = g2.param if len(g2.param) == 3 else [0.0] + g2.param
        new_angle = compose_u3(g1_angle[0], g1_angle[1], g1_angle[2],
                           g2_angle[0], g2_angle[1], g2_angle[2])
        gate_name = "u3"
    if abs(np.mod(new_angle[0] if isinstance(new_angle, list) else new_angle,
                  (2 * np.pi))) < 1E-8 and gate_name != "u1":
        gate_name = "u1"
        new_angle = new_angle[1] + new_angle[2] + new_angle[0]
    if gate_name == "u3":
        right_angle = new_angle[0] - np.pi / 2
        if abs(right_angle) < 1E-8:
            right_angle = 0
        if abs(np.mod((right_angle),
                      2 * np.pi)) < 1E-8:
            gate_name = "u2"
            new_angle = [new_angle[1], new_angle[2] + (new_angle[0] - np.pi / 2)]
        right_angle = new_angle[0] + np.pi / 2
        if abs(right_angle) < 1E-8:
            right_angle = 0
        if abs(np.mod(right_angle,
                      2 * np.pi)) < 1E-8:
            gate_name = "u2"
            new_angle = [new_angle[1] + np.pi, new_angle[2] - np.pi + (new_angle[0] + np.pi / 2)]
    if gate_name == "u1" and abs(np.mod(new_angle,
                                         2 * np.pi)) < 1E-8:
        gate_name = "id"
        return IdGate(g1.qubits[0])
    if gate_name =="u1":
        return U1Gate(g1.qubits[0], new_angle)
    if gate_name =="u2":
        return U2Gate(g1.qubits[0], new_angle)
    if gate_name =="u3":
        return U3Gate(g1.qubits[0], new_angle)

    def compose_u3(theta1, phi1, lambda1, theta2, phi2, lambda2):
        thetap, phip, lambdap = yzy_to_zyz((lambda1 + phi2), theta1, theta2)
        (theta, phi, lamb) = (thetap, phi1 + phip, lambda2 + lambdap)
        return (theta, phi, lamb)

    def yzy_to_zyz(xi, theta1, theta2, eps=1e-9):  
        quaternion_yzy = Quaternion.from_euler([theta1, xi, theta2], 'yzy')
        euler = quaternion_yzy.to_zyz()
        quaternion_zyz = Quaternion.from_euler(euler, 'zyz')
        out_angles = (euler[1], euler[0], euler[2])
        abs_inner = abs(quaternion_zyz.data.dot(quaternion_yzy.data))
        if not np.allclose(abs_inner, 1, eps):
            raise raise_error('YZY and ZYZ angles do not give same rotation matrix.')
        out_angles = tuple(0 if np.abs(angle) < _CHOP_THRESHOLD else angle
                        for angle in out_angles)
        return out_angles

def consolidate_2q_block(block, q0, q1):
    if block.size() == 1:
        return block
    matrix = np.identity(4)
    for gate in block:
        gate_matrix = GateMasterDef(gate.name, gate.param)
        if len(gate.qubits) == 1:
            if gate.qubits[0] == q0:
                gate_matrix = np.kron(gate_matrix, np.identity(2))
            else:
                gate_matrix = np.kron(np.identity(2), gate_matrix)
        if len(gate.qubits) == 2:
            if gate.qubits[0] == q1:
                gate_matrix = flip_matrix(gate_matrix)
        matrix = matrix.dot(gate_matrix)
    ret_circ = empty_circuit()
    ret_circ = ret_circ.append(UnitaryGate(q0, q1, matrix))
    return ret_circ

def cancel_gates(block):
    gate_set = ["CX", "X", "Z", "H", "T", "Y"]
    gate_count = dict()
    for gate in block:
        if (gate.name, tuple(gate.qubits)) not in gate_count:
            gate_count[(gate.name, tuple(gate.qubits))] = 1
        else:
            gate_count[(gate.name, tuple(gate.qubits))] += 1
    ret_circ = empty_circuit()
    for gate_data, count in gate_count:
        if count % 2 == 1:
            ret_circ = ret_circ.append(QGate(gate_data[0], list(gate_data[1])))
    return ret_circ