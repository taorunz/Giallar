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

class PassManager():

    def __init__(self, pass_list=[]):

        self.pass_list = pass_list

    
    def append(self, cpass):

        self.pass_list.append(cpass)

    
    def run(self, circ, dag = None, layout = None):
        
        prop = {}
        prop['circ'] = circ
        prop['dag'] = dag
        prop['layout'] = layout
        for cpass in self.pass_list:
            prop = cpass.run(prop)
            # output_circ = prop['circ']

        return prop
