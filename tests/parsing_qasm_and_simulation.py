from giallar.core.impl.qasm_parser import QasmParser
from giallar.core.impl.qgate import QGate
from giallar.core.impl.qcircuit import QCircuit

# We can construct a quantum circuit from a qasm file
qp = QasmParser("qasm/example1.qasm")

# Initiate the Quantum Circuit
qc = QCircuit(qp.qubits)
for g in qp.gates:
    qc.append(g)

# We could also add gates in Python code
qc.cx(qc.qubits[0], qc.qubits[1])

# Simulate the quantum circuit and calculate the denotational semantics
print(qc.apply_qcircuit())
