from z3 import *
from giallar.z3_wrapper import *
from giallar.gate_info import gate_info

# Symbolic setup for qubit(s) type
QubitStateType = DeclareSort("QubitState")
QubitType = ArraySort(IntSort(), QubitStateType)

# Symbolic setup for gate type
GateType = Datatype('Gate')
GateType.declare('new',('gid', IntSort()), ('arg0', IntSort()),  ('arg1', IntSort()), ('arg2', IntSort()),  ('param', RealSort()))
GateType = GateType.create()

# Symbolic setup for circuit type
CircuitType = ArraySort(IntSort(), GateType)



#######################
# Symbolic simulation
#######################

emul_gate = Function('emul_gate', IntSort(), QubitStateType, QubitStateType)
emul_gate_1 = Function('emul_gate_1', IntSort(), QubitStateType, QubitStateType, QubitStateType)
emul_gate_2 = Function('emul_gate_2', IntSort(), QubitStateType, QubitStateType, QubitStateType)

def apply_on_qubit_state(qubits, gate):
    
    gid = gate.gid()  # gate's name
    op1 = gate.arg(0)   # 1st logical operand
    op2 = gate.arg(1)   # 2nd logical operand
    
    try:
        set_option(timeout=500)
        certiq_prove(gid == 0, mute=True, msg="SwapGate")

    except:
        out1 = emul_gate_1(gid, qubits[op1], qubits[op2])
        out2 = emul_gate_2(gid, qubits[op1], qubits[op2])

    else:
        out1 = qubits[op2]
        out2 = qubits[op1]

    qubits = Store(Store(qubits, op1, out1), op2, out2)

    return simplify(qubits)

q1 = Const('any_q1', QubitStateType)
assertion(ForAll([q1], emul_gate_2(13, q1, q1) == q1))

def apply_swap_on_qubit_state(qubits, gate):
    
    gid = gate.gid()  # gate's name
    op1 = gate.arg(0)   # 1st logical operand
    op2 = gate.arg(1)   # 2nd logical operand
    
    out1 = qubits[op2]
    out2 = qubits[op1]

    qubits = Store(Store(qubits, op1, out1), op2, out2)

    return simplify(qubits)


