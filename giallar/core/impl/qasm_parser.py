
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

"""
 - Parse qasm files
 - Example qasm qubit definition: qubit q1
 - Example qasm gate line: CNOT q1,q2
 - Example qasm rotation gate: Rz 0.25 q1
 - No white spaces between qubit arguments but a comma
"""

import re
from sympy import Symbol
from giallar.core.impl.qgate import QGate
from giallar.core.impl.error_handler import raise_error
from giallar.gate_info import gate_info

class QasmParser(object):
    """
    - Parser class
    """

    # pylint: disable=anomalous-backslash-in-string
    # pylint: disable=too-few-public-methods

    def __init__(self, filename):
        self.qubits = []           #list of qubit names
        self.gates = []            #list of gates
        self.comments = ''         #string to store the comments

        error_line = 0             #for printing out error line

        with open(filename) as f_handler:

            for line in f_handler:

                error_line += 1

                if line[0] == '#':
                    self.comments += line
                    continue

                # qubit declaration, ignore cbits here
                match = re.compile('\s*qubit\s+(\S+)').search(line)
                if match:
                    self.qubits.append(match.group(1))	# add name
                    continue

                # gate
                match = re.compile('^([^Rq]+)\s+(\S+)').search(line)
                if match:
                    op_name = match.group(1)
                    args = match.group(2)
                    gate_check(op_name, args, error_line)
                    self.gates.append(QGate(op_name, args.split(',')))

                # rotations
                match = re.compile('^([Rxyz]+)\s+(\S+)\s+(\S+)').search(line)
                if match:
                    op_name = match.group(1)
                    rot = match.group(2)
                    args = match.group(3)
                    gate_check(op_name, args, error_line)
                    
                    if re.compile('\d\+\.\d\+').search(rot):
                        rot = float(rot)
                    else:
                        rot = Symbol(rot)
                    self.gates.append(QGate(op_name, args.split(','), param=rot))


def gate_check(op_name, args, error_line):
    """
    - Sanity check for gates
    """

    if op_name.lower() not in gate_info:
        msg = (error_line, op_name, args)
        raise_error("[QasmParser]Line %d unknown gate op %s on %s" % msg)

    n_wires = gate_info[op_name.lower()]['argn']

    if len(args.split(',')) != n_wires:
        msg = (error_line, op_name + " " + args)
        raise_error("[QasmParser]Line %d wrong number of qubits in %s" % msg)

    # Non-cloning check
    wires = args.split(',')
    if [wires.count(qb) for qb in wires].count(1) < len(wires):
        msg = (error_line, op_name + " " + args)
        raise_error("[QasmParser]Line %d duplicate qubits in %s" % msg)

    return True
