from z3 import *
from giallar.core.spec.qcircuit import *
from giallar.utility_library.library import *
from giallar.core.spec.qgate import *
from giallar.z3_wrapper import *
from giallar.core.spec.invariant import *

qcirc = QCircuit()
new_qcirc = QCircuit()

i = Int('i')

assertion(equivalent(new_qcirc, qcirc.partial_circuit(0, i)))

new_qcirc = new_qcirc.append(qcirc[i])

certiq_prove(equivalent(new_qcirc, qcirc.partial_circuit(0, i+1)))

