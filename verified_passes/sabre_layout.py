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

from giallar.core.impl.error_handler import raise_error
from giallar.core.impl.analysis import Analysis
from giallar.core.impl.layout import Layout
import random
from time import time
from constraint import Problem, RecursiveBacktrackingSolver, AllDifferentConstraint

class SabreLayout(Analysis):

    def __init__(self, coupling_map):
        self.coupling_map = coupling_map

    def run(self, input_prop):
        
        qcirc = input_prop['circ']
        layout = self._generate_sabre_layout(qcirc)

        input_prop['layout'] = layout

        return input_prop


    def _generate_sabre_layout(self, dag):
        """Run the SabreLayout pass on `dag`.

        Args:
            dag (DAGCircuit): DAG to find layout for.

        Raises:
            TranspilerError: if dag wider than self.coupling_map
        """
        if len(dag.qubits) > self.coupling_map.size():
            raise TranspilerError("More virtual qubits exist than physical.")

        # Choose a random initial_layout.
        if self.seed is None:
            self.seed = np.random.randint(0, np.iinfo(np.int32).max)
        rng = np.random.default_rng(self.seed)

        physical_qubits = rng.choice(self.coupling_map.size(), len(dag.qubits), replace=False)
        physical_qubits = rng.permutation(physical_qubits)
        initial_layout = Layout({q: dag.qubits[i] for i, q in enumerate(physical_qubits)})

        if self.routing_pass is None:
            self.routing_pass = SabreSwap(self.coupling_map, "decay", seed=self.seed, fake_run=True)
        else:
            self.routing_pass.fake_run = True

        # Do forward-backward iterations.
        circ = dag_to_circuit(dag)
        rev_circ = circ.reverse_ops()
        for _ in range(self.max_iterations):
            for _ in ("forward", "backward"):
                pm = self._layout_and_route_passmanager(initial_layout)
                new_circ = pm.run(circ)

                # Update initial layout and reverse the unmapped circuit.
                pass_final_layout = pm.property_set["final_layout"]
                final_layout = self._compose_layouts(
                    initial_layout, pass_final_layout, new_circ.qregs  # pylint: disable=no-member
                )
                initial_layout = final_layout
                circ, rev_circ = rev_circ, circ

            # Diagnostics
            logger.info("new initial layout")
            logger.info(initial_layout)

        for qreg in dag.qregs.values():
            initial_layout.add_register(qreg)

        self.property_set["layout"] = initial_layout
        self.routing_pass.fake_run = False


    def _layout_and_route_passmanager(self, initial_layout):
        """Return a passmanager for a full layout and routing.

        We use a factory to remove potential statefulness of passes.
        """
        layout_and_route = [
            SetLayout(initial_layout),
            FullAncillaAllocation(self.coupling_map),
            EnlargeWithAncilla(),
            ApplyLayout(),
            self.routing_pass,
        ]
        pm = PassManager(layout_and_route)
        return pm

    def _compose_layouts(self, initial_layout, pass_final_layout, qregs):
        """Return the real final_layout resulting from the composition
        of an initial_layout with the final_layout reported by a pass.

        The routing passes internally start with a trivial layout, as the
        layout gets applied to the circuit prior to running them. So the
        "final_layout" they report must be amended to account for the actual
        initial_layout that was selected.
        """
        trivial_layout = Layout.generate_trivial_layout(*qregs)
        qubit_map = Layout.combine_into_edge_map(initial_layout, trivial_layout)
        final_layout = {
            v: pass_final_layout[qubit_map[v]] for v, _ in initial_layout.get_virtual_bits().items()
        }
        return Layout(final_layout)