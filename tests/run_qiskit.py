from qiskit.transpiler.passes import LookaheadSwap, BasicSwap
from qiskit.transpiler.layout import Layout
import qiskit.converters
import qiskit.circuit
import sys

# qp = ("qasm/example2.qasm")
circ = qiskit.circuit.QuantumCircuit.from_qasm_file(sys.argv[1])

# dag = qiskit.converters.circuit_to_dag(circ)
# regs = dag.qregs["q"]
# layout = Layout.generate_trivial_layout(regs)

# print(layout)

num_qubits = circ.num_qubits
coupling_list = [[i, i + 1] for i in range(num_qubits - 1)]
coupling_map = qiskit.transpiler.CouplingMap(couplinglist = coupling_list)

pass_ = LookaheadSwap(coupling_map = coupling_map)

pm = qiskit.transpiler.PassManager(pass_)

new_circ = pm.run(circ)