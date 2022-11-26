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

from z3 import *

def assertion(cond, **keywords):
    if not hasattr(assertion, 'assertions'):
        def current():
            ret = []
            for a in assertion.assertions:
                ret += a
            return ret
        def current_special():
            ret = {}
            for special in assertion.special:
                for k in special:
                    ret[k] = special[k]
            return ret
        def push():
            assertion.assertions.append([])
            assertion.special.append({})
        def pop():
            assertion.assertions.pop()
            assertion.special.pop()

        assertion.assertions = [[]]
        assertion.cur = current
        assertion.cur_sp = current_special
        assertion.push = push
        assertion.pop = pop
        assertion.special = [{}]

    if not isinstance(cond, list):
        cond = [cond]
    name = keywords.get("name", None)
    if name is None:
        assertion.assertions[-1] += cond
    else:
        assertion.special[-1][name] = cond


def certiq_prove(claims, **keywords):
    """
    Customized z3 prove function
    """
    if not isinstance(claims, list):
        claims = [claims]
    for i, claim in enumerate(claims):
        s = Solver()
        st = []
        need = keywords.get('need', [])
        for cond in assertion.cur():
            s.add(simplify(cond))
            st.append(simplify(cond))
        sp = assertion.cur_sp()
        for n in need:
            if n in sp:
                for cond in sp[n]:
                    s.add(simplify(cond))
                    st.append(simplify(cond))

        if not keywords.get('check_condition', False):
            s.add(simplify(Not(claim)))
            st.append(simplify(Not(claim)))

        if keywords.get('show', False):
            print("#"*100)
            for x in st: print(x)
        r = s.check()
        
        if keywords.get('check_condition', False) and r == unsat:

            print("Condition not possible. Quit")
            return False

        if keywords.get('check_condition', False) and r == sat:
            
            print("Condition available.")
            return True

        if r == unsat:
            if keywords.get('save', False):
                assertion(claims, name=keywords.get('name', None))
        elif r == unknown:
            if not keywords.get('mute', False):
                print("failed to prove\n" + s.model())
            exit()
        else:
            if not keywords.get('mute', False):
                print("counterexample\n" + str(s.model()))
                # assert(False)
            exit()

    print(keywords.get("msg", "")+" proved.")

    return True

# fresh variables

N_INT = 0
def fresh_int(prefix=""):
    global N_INT
    n = Int("i_" + prefix + str(N_INT))
    N_INT += 1
    return n

N_REAL = 0
def fresh_real(prefix=""):
    global N_REAL
    n = Real("r_" + prefix + str(N_REAL))
    N_REAL += 1
    return n

N_BOOL = 0
def fresh_bool(prefix=""):
    global N_BOOL
    n = Bool("b_" + prefix + str(N_BOOL))
    N_BOOL += 1
    return n

N_ARRAY = 0
def fresh_array(prefix, in_sort, out_sort):
    global N_ARRAY
    arr = Array("a_" + prefix + str(N_ARRAY), in_sort, out_sort)
    N_ARRAY += 1
    return arr

N_STRING = 0
def fresh_string(prefix=""):
    global N_STRING
    s = String("s_" + prefix + str(N_STRING))
    N_STRING += 1
    return s

N_NAME = 0
def fresh_name(prefix=""):
    global N_NAME
    s = "n_" + prefix + str(N_NAME)
    N_NAME += 1
    return s


TripleInt = Datatype('TripleInt')
TripleInt.declare('new', ('n1', IntSort()), ('n2', IntSort()), ('n3', IntSort()))
TripleInt = TripleInt.create()

class Dict_TripleInt:
    def __init__(self, default=None):
        self.data = fresh_array('dict_triple_int', TripleInt, IntSort())
        if default is not None:
            n1, n2, n3 = Ints('n1 n2 n3')
            assertion(ForAll([n1, n2, n3], self[(n1, n2, n3)] == default))
    def __getitem__(self, index):
        index = TripleInt.new(*index)
        return self.data[index]
    def __setitem__(self, index, value):
        index = TripleInt.new(*index)
        self.data = Store(self.data, index, value)

DoubleInt = Datatype('DoubleInt')
DoubleInt.declare('new', ('n1', IntSort()), ('n2', IntSort()))
DoubleInt = DoubleInt.create()

class Dict_DoubleInt:
    def __init__(self, default=None):
        self.data = fresh_array('dict_double_int', DoubleInt, IntSort())
        if default is not None:
            n1, n2 = Ints('n1 n2')
            assertion(ForAll([n1, n2], self[(n1, n2)] == default))
    def __getitem__(self, index):
        index = DoubleInt.new(*index)
        return self.data[index]
    def __setitem__(self, index, value):
        index = DoubleInt.new(*index)
        self.data = Store(self.data, index, value)

class Dict_Int2Int:
    def __init__(self, default=None):
        self.data = fresh_array('dict_int2int', IntSort(), IntSort())
        if default is not None:
            n = Int('n')
            assertion(ForAll([n], self[n] == default))
    def __getitem__(self, index):
        return self.data[index]
    def __setitem__(self, index, value):
        self.data = Store(self.data, index, value)

class Dict_Int2Bool:
    def __init__(self, default=None):
        self.data = fresh_array('dict_int2bool', IntSort(), BoolSort())
        if default is not None:
            n = Int('n')
            assertion(ForAll([n], self[n] == default))
    def __getitem__(self, index):
        return self.data[index]
    def __setitem__(self, index, value):
        self.data = Store(self.data, index, value)
