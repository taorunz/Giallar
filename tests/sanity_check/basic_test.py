from giallar.core.impl.passmanager import PassManager
from giallar.core.impl.layout import Layout
from giallar.core.impl.coupling import CouplingMap
from giallar.verified_passes.basic_swap import BasicSwap
from giallar.verified_passes.trivial_layout import TrivialLayout
from giallar.verified_passes.set_layout import SetLayout
from giallar.core.impl.qasm_parser import QasmParser
from giallar.core.impl.qcircuit import QCircuit

# We can construct a quantum circuit from a qasm file
qp = QasmParser("tests/qasm/example2.qasm")

# Initiate the Quantum Circuit
qc = QCircuit(qp.qubits)
for g in qp.gates:
        qc.append(g)

coup = CouplingMap([[0,1],[1,2],[2,3],[3,4]])

pm = PassManager([TrivialLayout(coup), BasicSwap(coup)])

output_prop = pm.run(qc)

new_circuit = output_prop['circ']

for gate in new_circuit.gate_list:
        print(gate.name, gate.qubits)
