




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

import argparse
import os
import astroid
from string import Template

from giallar.config import PASS_DIR
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.transpiler.passes.routing import BasicSwap
from giallar.preprocessor.preprocessor import get_ast, expand_file, ASTWalker

class search_classname():
    """
    Handler for ASTWalker. For searching the name of the CertiQ pass
    """
    
    def __init__(self):
        self.count = 0
        self.basenames = None
        self.name = None
        self.coupling_string = ""

    def visit_default(self, node):
        return

    def leave_default(self, node):
        pass

    def visit_ClassDef(self, node):
        self.count += 1    

        if "Routing" in node.basenames or "Transformation" in node.basenames:
            self.basenames = "TransformationPass"
        elif "Analysis" in node.basenames:
            self.basenames = "AnalysisPass"

        else:
            raise_error("Base class not supported. Only supported transformation passes, analysis passes and routing passes")

        if "Routing" in node.basenames:
            self.coupling_string = "coupling = self.coupling"

        self.name = node.name
        self.doc = node.doc

        return
    
    def visit_run(self, node):
        if node.name == 'run' and node.is_method():
            self.run_doc = self.doc

        return

argParser = argparse.ArgumentParser(description='Convert a CertiQ compilation pass to Qiskit pass.')
argParser.add_argument('--file', dest='filename', default='')
args = argParser.parse_args()

filename = args.filename + ".py"

# print(PASS_DIR)
# Extract AST of the Certiq pass file
module_data = expand_file(os.path.join(PASS_DIR, filename))
file_path, modname = module_data['path'], module_data['name']
# print(file_path)
if modname is None:
    modname = "certiq.verified_passes." + filename
module_node = get_ast(file_path, modname)

classname_search = search_classname()
walker = ASTWalker(classname_search)
walker._cache[astroid.scoped_nodes.ClassDef] = [classname_search.visit_ClassDef, classname_search.leave_default]
walker._cache[astroid.scoped_nodes.FunctionDef] = [classname_search.visit_run, classname_search.leave_default]
walker.walk(module_node)

if classname_search.count != 1:
    raise ValueError("There should be one and only one class defined in the file.")

template_file = open("template/qiskit_generation.template", "r")
tmpl = Template(template_file.read())
template_file.close()



lines = []
lines.append(tmpl.substitute(
                                CLASSNAME = classname_search.name,
                                FILENAME = args.filename,
                                BASENAME = classname_search.basenames,
                                COUPLING = classname_search.coupling_string,
                                CLASSCOMMENTS = classname_search.doc if classname_search.doc != None else "",
                                RUNCOMMENTS = classname_search.run_doc if classname_search.run_doc != None else ""
                            ))

qiskit_file = open(args.filename + "_certiq.py", "w+")
qiskit_file.writelines(lines)
qiskit_file.close()

print("Generated the qiskit pass.")
