#from qiskit.transpiler.passes.routing.lookahead_swap import LookaheadSwap
from giallar.core.impl.passmanager import PassManager
from verified_passes.look_ahead import LookaheadSwap
from verified_passes.cx_cancellation import CXCancellation
from verified_passes.sabre_swap import SabreSwap
from verified_passes.trivial_layout import TrivialLayout
import sys
# We can construct a quantum circuit from a qasm file
import qiskit.converters
import qiskit.circuit
# qp = qiskit.circuit.QuantumCircuit.from_qasm_file("qasm/Adder1024.qasm")
qp = qiskit.circuit.QuantumCircuit.from_qasm_file(sys.argv[1])
dag = qiskit.converters.circuit_to_dag(qp)

import giallar.qiskit_wrapper.converter as converter
qc = converter.dag_to_certiq_circ(dag)
qc.simplify_qubits()
# print(qc.simplified_qubit)
# Initiate the Quantum Circuit
# qc = QCircuit(qp.qubits)
# for g in qp.gates:
#         qc.append(g)

# print(qc)

num_qubits = qp.num_qubits
coupling_list = [[i, i + 1] for i in range(num_qubits - 1)]
coup = qiskit.transpiler.CouplingMap(couplinglist = coupling_list)
import time
# pm = PassManager([TrivialLayout(coup)])
# pm2 = PassManager([SabreSwap(coup)])

pm = PassManager([TrivialLayout(coup), LookaheadSwap(coup)])
cur_time = time.time()
output_prop = pm.run(qc)
# layout = output_prop["layout"]


# output_prop_final = pm2.run(qc, layout = layout)
print(time.time() - cur_time)
