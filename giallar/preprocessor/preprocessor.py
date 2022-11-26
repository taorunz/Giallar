# Copyright 2019-2020 The giallar authors.
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

import os
from os.path import dirname, basename, splitext, exists, isdir, join, normpath
import errno
import tokenize
import collections
from functools import lru_cache
import copy
import re
import argparse
# from giallar.giallar_core.giallar_spec.gate import Gate
from giallar.core.impl.error_handler import raise_error

from astroid import parse, extract_node, modutils
import astroid

MANAGER = astroid.MANAGER

import enum
class VarType(enum.Enum):
    Circuit = 0
    Perm = 1
    Layout = 2
    Other = 3

class ASTWalker:
    """a walker visiting a tree in preorder, calling on the handler:
    * visit_<class name> on entering a node, where class name is the class of
    the node in lower case
    * leave_<class name> on leaving a node, where class name is the class of
    the node in lower case
    """

    def __init__(self, handler):
        self.handler = handler 
        self._cache = {}

    def walk(self, node, _done=None):
        """walk on the tree from <node>, getting callbacks from handler"""
        if _done is None:
            _done = set()
        if node in _done:
            raise AssertionError((id(node), node, node.parent))
        _done.add(node)
        self.visit(node)
        for child_node in node.get_children():
            assert child_node is not node
            self.walk(child_node, _done)
        self.leave(node)
        assert node.parent is not node

    def get_callbacks(self, node):
        """get callbacks from handler for the visited node"""
        klass = node.__class__
        methods = self._cache.get(klass)
        if methods is None:
            handler = self.handler
            kid = klass.__name__.lower()
            e_method = getattr(handler, 'visit_%s' % kid,
                               getattr(handler, 'visit_default', None))
            l_method = getattr(handler, 'leave_%s' % kid,
                               getattr(handler, 'leave_default', None))
            self._cache[klass] = (e_method, l_method)
        else:
            e_method, l_method = methods
        return e_method, l_method

    def visit(self, node):
        """walk on the tree from <node>, getting callbacks from handler"""
        method = self.get_callbacks(node)[0]
        if method is not None:
            method(node)

    def leave(self, node):
        """walk on the tree from <node>, getting callbacks from handler"""
        method = self.get_callbacks(node)[1]
        if method is not None:
            method(node)

class TransformVisitor:
    """A visitor for handling transforms.

    The standard approach of using it is to call
    :meth:`~visit` with an *astroid* module and the class
    will take care of the rest, walking the tree and running the
    transforms for each encountered node.
    """

    TRANSFORM_MAX_CACHE_SIZE = 10000

    def __init__(self):
        self.transforms = collections.defaultdict(list)

    @lru_cache(maxsize=TRANSFORM_MAX_CACHE_SIZE)
    def _transform(self, node):
        """Call matching transforms for the given node if any and return the
        transformed node.
        """
        cls = node.__class__
        if cls not in self.transforms:
            # no transform registered for this class of node
            return node

        transforms = self.transforms[cls]
        for transform_func, predicate in transforms:
            if predicate is None or predicate(node):
                ret = transform_func(node)
                # if the transformation function returns something, it's
                # expected to be a replacement for the node
                if ret is not None:
                    node = ret
                if ret.__class__ != cls:
                    # Can no longer apply the rest of the transforms.
                    break
        return node

    def _visit(self, node):
        if hasattr(node, "_astroid_fields"):
            for name in node._astroid_fields:
                value = getattr(node, name)
                visited = self._visit_generic(value)
                if visited != value:
                    setattr(node, name, visited)
        return self._transform(node)

    def _visit_generic(self, node):
        if isinstance(node, list):
            return [self._visit_generic(child) for child in node]
        if isinstance(node, tuple):
            return tuple(self._visit_generic(child) for child in node)
        if not node or isinstance(node, str):
            return node

        return self._visit(node)

    def register_transform(self, node_class, transform, predicate=None):
        """Register `transform(node)` function to be applied on the given
        astroid's `node_class` if `predicate` is None or returns true
        when called with the node as argument.

        The transform function may return a value which is then used to
        substitute the original node in the tree.
        """
        self.transforms[node_class].append((transform, predicate))

    def unregister_transform(self, node_class, transform, predicate=None):
        """Unregister the given transform."""
        self.transforms[node_class].remove((transform, predicate))

    def visit(self, module):
        """Walk the given astroid *tree* and transform each encountered node

        Only the nodes which have transforms registered will actually
        be replaced or changed.
        """
        module.body = [self._visit(child) for child in module.body]
        return self._transform(module)

class annotate_if():
    """
    Handler for ASTWalker. For counting the number of if statements
    that user doesn't provide a 'conditional invariant'.
    """
    
    def __init__(self, comment_dict):
        self.if_counter = 0
        self.for_counter = 0
        self.while_counter = 0
        self.comment_dict = comment_dict
        self.module_name = ""
        self.base_name = None
        self.var_dict = {}

    def visit_default(self, node):
        if type(node) == astroid.node_classes.For:
            if not hasattr(node, '__for_num__'):
                node.__for_num__ = self.for_counter
                self.for_counter += 1

        if type(node) == astroid.nodes.ClassDef:

            if self.module_name == "":
                if ("Routing" in node.basenames or
                    "Transformation" in node.basenames or
                    "Analysis" in node.basenames):

                    self.module_name = node.name
                    self.base_name = node.basenames[0]

                else:
                    raise_error("giallar supports the verification of Routing, Transformation and Analysis passes only.")

        if type(node) == astroid.nodes.While:
            if if_circuit_while(node):
                if not hasattr(node, '__while_num__'):
                    node.__while_num__ = self.while_counter
                    self.while_counter += 1

        if type(node) == astroid.nodes.Assign:
            if len(node.targets) == 1 and type(node.targets[0]) == astroid.nodes.AssignName: 
                name = node.targets[0].name
                if name not in self.var_dict:
                    # print(f"find initial assignment on Line {node.lineno}, target: {name}")
                    self.var_dict[name] = {"lineno": node.lineno, "value": node.value.as_string()}


    def leave_default(self, node):
        pass

    def visit_if(self, node):

        if type(node) == astroid.node_classes.If:
            
            # print(node.test.func)
            if not hasattr(node, '__invariant_if__'):
                node.__invariant_if__ = False
                node.__raise_error_if__ = False
            if not hasattr(node, '__if_num__'):
                node.__invariant_if__ = False
                node.__if_num__ = -1
            
            comment_lineno = node.lineno + 1

            try:
                if node.body[0].value.func.name == 'raise_error':
                    if len(node.body) == 1:
                        node.__raise_error_if__ = True
                    else:
                        raise AssertionError("raise_error can only be used alone.")
            except:
                pass

            if comment_lineno in self.comment_dict and len(node.orelse) == 0:
                
                comment_content = self.comment_dict[comment_lineno]
                m = re.compile("## li: (.*)").search(comment_content)
                if (m):
                    node.__invariant_if__ = True
                    if not hasattr(node, '__if_invariant__'):
                        node.__if_invariant__ = m.group(1)
                        # print(node.__if_invariant__)
            
            else:
                node.__if_num__ = self.if_counter
                self.if_counter += 1

        return

def parse_var_info(dict):
    ret_dict = {}
    for name, info in dict.items():
        lineno = info["lineno"]
        val = info["value"]

        if ".copy()" in val and val.split(".")[0] in ret_dict:
            vartype = ret_dict[val.split(".")[0]]["type"]
        elif "QCircuit" in val or "['circ']" in val or "circuit" in val:
            vartype = VarType.Circuit
        elif "['layout']" in val or val == 'initial_layout.copy()':
            vartype = VarType.Layout
        elif "Perm" in val:
            vartype = VarType.Perm
        else:
            vartype = VarType.Other
        
        ret_dict[name] = {"lineno": lineno, "type": vartype}
    return ret_dict

def find_var(lineno, vartype, other=""):
    for name, info in reversed(list(var_info.items())):
        if info["lineno"] >= lineno:
            continue
        if info["type"] == vartype:
            if name == other:
                continue
            print(f"inferred {name}")
            return name
    return None

def raise_error_trans(node):

    """
    Function for modifying the AST of an astroid.If

    Input node
    ------------------
    if test:
        body
    else:
        orelse

    Output node
    ------------------
    assertion(Not(test))
    orelse
    """

    new_assertion = astroid.Call(
                    lineno = node.lineno,
                    col_offset = node.col_offset,
                    parent = node.parent,
                    )

    not_test = astroid.Call(
                    lineno = node.lineno,
                    col_offset = node.col_offset,
                    parent = new_assertion,
                    )

    func_name = astroid.Name(
                    name = "assertion",
                    lineno = node.lineno,
                    col_offset = node.col_offset,
                    parent = node.parent,
                    )

    func_not = astroid.Name(
                    name = "Not",
                    lineno = node.lineno,
                    col_offset = node.col_offset,
                    parent = new_assertion,
                    )

    not_test.postinit(args = [node.test],
                    func = func_not,
                    keywords = None
                    )

    new_assertion.postinit(args = [not_test],
                    func = func_name,
                    keywords = None
                    )

    new_node = astroid.nodes.Module(
                    name = None,
                    doc = "",
                    parent = node.parent,
                    )

    new_node.postinit(body = [new_assertion])

    return new_node

def unsupported_if_condition(node):
    if " in " in node.as_string():
        return True 
    return False

def if_trans_first(node):
    """
    Function for modifying the AST of an astroid.If

    Input node
    ------------------
    if test:
        body
    else:
        orelse

    Output node
    ------------------
    assertion(test)
    body
    """

    # if (next(node.test.func.expr.infer())._proxied) 
    # if (next(node.test.func.expr.infer())._proxied) 

    func_name = astroid.Name(
                    name = "assertion",
                    lineno = node.lineno,
                    col_offset = node.col_offset,
                    parent = node.parent,
                    )
    
    new_assertion = astroid.Call(
                    lineno = node.lineno,
                    col_offset = node.col_offset,
                    parent = node.parent,
                    )
     
    new_assertion.postinit(args = [node.test],
                    func = func_name,
                    keywords = None
                    )
    
    new_node = astroid.nodes.Module(
                    name = None,
                    doc = "",
                    parent = node.parent,
                    )

    if unsupported_if_condition(new_assertion):
        new_node.postinit(body = node.body)
    else:
        new_node.postinit(body = [new_assertion] + node.body)

    return new_node

def if_trans_second(node):
    """
    Function for modifying the AST of an astroid.If

    Input node
    ------------------
    if test:
        body
    else:
        orelse

    Output node
    ------------------
    assertion(Not(test))
    orelse
    """

    new_assertion = astroid.Call(
                    lineno = node.lineno,
                    col_offset = node.col_offset,
                    parent = node.parent,
                    )

    not_test = astroid.Call(
                    lineno = node.lineno,
                    col_offset = node.col_offset,
                    parent = new_assertion,
                    )

    func_name = astroid.Name(
                    name = "assertion",
                    lineno = node.lineno,
                    col_offset = node.col_offset,
                    parent = node.parent,
                    )

    func_not = astroid.Name(
                    name = "Not",
                    lineno = node.lineno,
                    col_offset = node.col_offset,
                    parent = new_assertion,
                    )

    not_test.postinit(args = [node.test],
                    func = func_not,
                    keywords = None
                    )

    new_assertion.postinit(args = [not_test],
                    func = func_name,
                    keywords = None
                    )

    new_node = astroid.nodes.Module(
                    name = None,
                    doc = "",
                    parent = node.parent,
                    )

    if unsupported_if_condition(new_assertion):
        new_node.postinit(body = node.orelse)
    else:
        new_node.postinit(body = [new_assertion] + node.orelse)

    return new_node

def twoq_trans(node):

    new_node = astroid.extract_node("gate_argn[GateType.gid({}.data)]==2".format(node.func.expr.name))
    return new_node
        

def test_twoq_node(node):

    try:
        if (node.func.attrname == 'isTwoQGate' and 
           next(node.func.expr.infer())._proxied.name != 'QGate'):
            return True
    except:
        pass

    return False 

def if_giallar_import(node):

    return 'impl' in node.modname

def import_trans(node):
    new_node = node
    new_node.modname = new_node.modname.replace('impl', 'spec')
    return new_node

def function_trans(node):
    new_node = node
    function_name = node.name
    specified_return = False
    if node.lineno:
        for comment_lineno in range(node.lineno, node.lineno + 10):
            if comment_lineno in comment_lineno_dict:
                comment = comment_lineno_dict[comment_lineno]
                if comment.startswith("#@ return"):
                    specified_return = True
                    # print(function_name, comment_lineno, comment[9:]) 
                    x = parse(comment[9:])
                    # print(x.body[0])
    if len(function_name) >= 2 and node.name[0] == '_' and node.name[1] != '_':
        new_node.body.clear()
        fresh_int_name = astroid.nodes.Name(name="fresh_int")
        fresh_int_call = astroid.nodes.Call()
        fresh_int_call.postinit(func=fresh_int_name, args=[])
        new_ret = astroid.nodes.Return()
        if specified_return:
            new_ret.postinit(value=x.body[0])
        else:
            new_ret.postinit(value=fresh_int_call)
        new_node.body.append(new_ret)
    return new_node

def for_trans(node):
    
    if base_name == "Routing":
        return for_trans_routing(node)

    if base_name in ["Transformation", "Analysis"]:
        return for_trans_transformation(node)

def for_trans_routing(node):
    if not hasattr(node, '__loop_para__'):
        node.__loop_para__ = {}
    for comment_lineno in range(node.lineno, node.lineno + 10):
        if comment_lineno in comment_lineno_dict:
            parse_para_loops(node, comment_lineno)
    if 'permutation' not in node.__loop_para__:
        node.__loop_para__['permutation'] = find_var(node.lineno, VarType.Perm)
    if 'circuit' not in node.__loop_para__:
        node.__loop_para__['circuit'] = find_var(node.lineno, VarType.Circuit)
    if 'layout' not in node.__loop_para__:
        node.__loop_para__['layout'] = find_var(node.lineno, VarType.Layout)

    # print(node.__loop_para__)

    new_node = astroid.nodes.Module(
                    name = None,
                    doc = "",
                    parent = node.parent,
                    )

    func_name = 'loop_body' + str(node.__for_num__)
    new_func = astroid.nodes.FunctionDef(name = func_name)

    gate_name = node.target
    circuit_name = node.iter.expr

    try:
        perm_name = astroid.nodes.Name(name=node.__loop_para__['permutation'])
        layout_name = astroid.nodes.Name(name=node.__loop_para__['layout'])
        ret_circuit_name = astroid.nodes.Name(name=node.__loop_para__['circuit'])
        ret_circuit_assign_name = astroid.nodes.AssignName(name=node.__loop_para__['circuit'])
        perm_assign_name = astroid.nodes.AssignName(name=node.__loop_para__['permutation'])

    except:
        raise_error("Please provide necessary loop annotation in for loops for the routing pass.")

    coup_name = astroid.extract_node("self.coupling")
    # coup_name = astroid.nodes.Attribute(attrname='coupling_map', expr=astroid.nodes.Name(name='self'))

    new_arg = astroid.nodes.Arguments()
    new_arg.postinit(args = [gate_name, ret_circuit_name, perm_name, layout_name],
                     defaults = [],
                     kwonlyargs = [],
                     kw_defaults = [],
                     annotations = [])

    new_tuple = astroid.nodes.Tuple()
    new_tuple.postinit(elts=[ret_circuit_name, perm_name])
    assign_tuple = astroid.nodes.Tuple()
    assign_tuple.postinit(elts=[ret_circuit_assign_name, perm_assign_name])
    new_ret = astroid.nodes.Return()
    new_ret.postinit(value = new_tuple)
    new_func.postinit(args = new_arg, body = node.body + [new_ret])

    new_call = astroid.nodes.Call()
    arg_list = [circuit_name, layout_name, coup_name, astroid.nodes.Name(name=func_name)]

    new_assign = astroid.nodes.Assign()
    new_assign.postinit(targets=[assign_tuple], value=new_call)
    new_name = astroid.nodes.Name(name="iterate_all_gates")

    new_call.postinit(func = new_name, args = arg_list)
    new_node.postinit(body = [new_func, new_assign])

    # print("new_node", new_node.as_string())
    return new_node


def for_trans_transformation(node):
    if type(node.iter) == astroid.nodes.Call:
        return for_trans_transformation_blocks(node)
    if not hasattr(node, '__loop_para__'):
        node.__loop_para__ = {}
    for comment_lineno in range(node.lineno, node.lineno + 10):
        if comment_lineno in comment_lineno_dict:
            parse_para_loops(node, comment_lineno)
    if 'circuit' not in node.__loop_para__:
        node.__loop_para__['circuit'] = find_var(node.lineno, VarType.Circuit)

    new_node = astroid.nodes.Module(
                    name = None,
                    doc = "",
                    parent = node.parent,
                    )

    func_name = 'loop_body' + str(node.__for_num__)
    new_func = astroid.nodes.FunctionDef(name = func_name)

    gate_name = node.target
    circuit_name = node.iter.expr
    ret_circuit_name = astroid.nodes.Name(name=node.__loop_para__['circuit'])
    ret_circuit_assign_name = astroid.nodes.AssignName(name=node.__loop_para__['circuit'])

    new_arg = astroid.nodes.Arguments()
    new_arg.postinit(args = [gate_name, ret_circuit_name],
                     defaults = [],
                     kwonlyargs = [],
                     kw_defaults = [],
                     annotations = [])

    # new_tuple = astroid.nodes.Tuple()
    # new_tuple.postinit(elts=[ret_circuit_name])
    # assign_tuple = astroid.nodes.Tuple()
    # assign_tuple.postinit(elts=[ret_circuit_assign_name])
    new_ret = astroid.nodes.Return()
    new_ret.postinit(value = ret_circuit_name)
    new_func.postinit(args = new_arg, body = node.body + [new_ret])

    new_call = astroid.nodes.Call()
    arg_list = [circuit_name, astroid.nodes.Name(name=func_name)]

    new_assign = astroid.nodes.Assign()
    new_assign.postinit(targets=[ret_circuit_assign_name], value=new_call)
    new_name = astroid.nodes.Name(name="iterate_all_gates_transform")

    new_call.postinit(func = new_name, args = arg_list)
    new_node.postinit(body = [new_func, new_assign])

    # print("new_node", new_node.as_string())
    return new_node

def for_trans_transformation_blocks(node):
    if not hasattr(node, '__loop_para__'):
        node.__loop_para__ = {}
    for comment_lineno in range(node.lineno, node.lineno + 10):
        if comment_lineno in comment_lineno_dict:
            parse_para_loops(node, comment_lineno)
    if 'circuit' not in node.__loop_para__:
        node.__loop_para__['circuit'] = find_var(node.lineno, VarType.Circuit)

    #print(node.__loop_para__['circuit'])
    new_node = astroid.nodes.Module(
                    name = None,
                    doc = "",
                    parent = node.parent,
                    )

    func_name = 'loop_body' + str(node.__for_num__)
    new_func = astroid.nodes.FunctionDef(name = func_name)

    gate_name = node.target
    circuit_name = node.iter.func.expr
    ret_circuit_name = astroid.nodes.Name(name=node.__loop_para__['circuit'])
    ret_circuit_assign_name = astroid.nodes.AssignName(name=node.__loop_para__['circuit'])

    new_arg = astroid.nodes.Arguments()
    new_arg.postinit(args = [gate_name],
                     defaults = [],
                     kwonlyargs = [],
                     kw_defaults = [],
                     annotations = [])

    # new_tuple = astroid.nodes.Tuple()
    # new_tuple.postinit(elts=[ret_circuit_name])
    # assign_tuple = astroid.nodes.Tuple()
    # assign_tuple.postinit(elts=[ret_circuit_assign_name])

    ret_block_name = node.body[-1].value.args[0]
    new_ret = astroid.nodes.Return()
    new_ret.postinit(value = ret_block_name)
    new_func.postinit(args = new_arg, body = node.body[:-1] + [new_ret])

    new_call = astroid.nodes.Call()
    arg_list = [circuit_name, astroid.nodes.Name(name=func_name)]

    new_assign = astroid.nodes.Assign()
    new_assign.postinit(targets=[ret_circuit_assign_name], value=new_call)
    new_name = astroid.nodes.Name(name="iterate_all_blocks_transform")

    new_call.postinit(func = new_name, args = arg_list)
    new_node.postinit(body = [new_func, new_assign])

    # print("new_node", new_node.as_string())
    return new_node

def parse_para_loops(node, comment_lineno):
    
    comment_content = comment_lineno_dict[comment_lineno].lstrip(' ')

    match = re.compile("#@ (\S+): (\S+)").search(comment_content)
    if match:
        # print("match:", match.group(1), match.group(2))
        node.__loop_para__[match.group(1)] = match.group(2)


def if_for_gate(node):
    if type(node.iter) == astroid.nodes.Attribute:
        if node.iter.attrname == 'gate_list':
            return True
    if type(node.iter) == astroid.nodes.Call:
        try:
            if node.iter.func.attrname == 'blocks':
                return True
        except:
            return False
    return False

def if_qcircuit(node):

    try:
        if node.func.name == "QCircuit":
            return True
    except:
        pass

    return False

def if_circuit_while(node):
    
    try:

        if (type(node.test) == astroid.node_classes.Compare and
            type(node.test.left) == astroid.node_classes.Call and 
            node.test.left.func.attrname == "size" and
            node.test.ops[0][0] == ">" and
            node.test.ops[0][1].value == 0):
            return True

    except:

        raise_error("giallar does not support general while statement. Please read the doc.")


    return False


def while_trans(node):

    circ = node.test.left.func.expr.name

    if base_name == "Routing":
        return while_trans_routing(node)

    if base_name in ["Transformation", "Analysis"]:
        return while_trans_transformation(node)

def while_trans_routing(node):
    if not hasattr(node, '__loop_para__'):
        node.__loop_para__ = {}

    circuit_string = node.test.left.func.expr.name # It is tested in if_circuit_trans, so this must be valid
    circuit_name = node.test.left.func.expr
    # print(circuit_name)
    
    for comment_lineno in range(node.lineno, node.lineno + 10):
        if comment_lineno in comment_lineno_dict:
            parse_para_loops(node, comment_lineno)

    if 'circuit' not in node.__loop_para__:
        node.__loop_para__['circuit'] = find_var(node.lineno, VarType.Circuit, other=circuit_string)
    if 'permutation' not in node.__loop_para__:
        node.__loop_para__['permutation'] = find_var(node.lineno, VarType.Perm)
    if 'layout' not in node.__loop_para__:
        node.__loop_para__['layout'] = find_var(node.lineno, VarType.Layout)

    print(node.__loop_para__)

    new_node = astroid.nodes.Module(
                    name = None,
                    doc = "",
                    parent = node.parent,
                    )

    try:
        perm_name = astroid.nodes.Name(name=node.__loop_para__['permutation'])
        layout_name = astroid.nodes.Name(name=node.__loop_para__['layout'])
        ret_circuit_name = astroid.nodes.Name(name=node.__loop_para__['circuit'])
        ret_circuit_assign_name = astroid.nodes.AssignName(name=node.__loop_para__['circuit'])
        perm_assign_name = astroid.nodes.AssignName(name=node.__loop_para__['permutation'])

    except:
        raise_error("Please provide necessary loop annotation in for loops for the routing pass.")
    coup_name = astroid.extract_node("self.coupling")
    new_node = astroid.nodes.Module(
                    name = None,
                    doc = "",
                    parent = node.parent,
                    )

    func_name = 'while_body' + str(node.__while_num__)
    new_func = astroid.nodes.FunctionDef(name = func_name)

    new_arg = astroid.nodes.Arguments()
    new_arg.postinit(args = [circuit_name, ret_circuit_name, perm_name, layout_name],
                     defaults = [],
                     kwonlyargs = [],
                     kw_defaults = [],
                     annotations = [])

    new_tuple = astroid.nodes.Tuple()
    new_tuple.postinit(elts=[ret_circuit_name, circuit_name, perm_name, layout_name])
    assign_tuple = astroid.nodes.Tuple()
    assign_tuple.postinit(elts=[circuit_name, ret_circuit_name, perm_name])
    new_ret = astroid.nodes.Return()
    new_ret.postinit(value = new_tuple)
    new_func.postinit(args = new_arg, body = node.body + [new_ret])

    new_call = astroid.nodes.Call()
    arg_list = [circuit_name, ret_circuit_name, layout_name, coup_name, astroid.nodes.Name(name=func_name)]

    new_assign = astroid.nodes.Assign()
    new_assign.postinit(targets=[assign_tuple], value=new_call)
    new_name = astroid.nodes.Name(name="while_iterate_routing")

    new_call.postinit(func = new_name, args = arg_list)
    new_node.postinit(body = [new_func, new_assign])

    # print("new_node", new_node.as_string())
    return new_node

def while_trans_transformation(node):

    if not hasattr(node, '__loop_para__'):
        node.__loop_para__ = {}
    for comment_lineno in range(node.lineno, node.lineno + 10):
        if comment_lineno in comment_lineno_dict:
            parse_para_loops(node, comment_lineno)

    circuit_string = node.test.left.func.expr.name # It is tested in if_circuit_trans, so this must be valid
    circuit_name = node.test.left.func.expr
    # print(circuit_name)
    if 'circuit' not in node.__loop_para__:
        node.__loop_para__['circuit'] = find_var(node.lineno, VarType.Circuit, other=circuit_string)
    try:
        ret_circuit_name = astroid.nodes.Name(name=node.__loop_para__['circuit'])
        ret_circuit_assign_name = astroid.nodes.AssignName(name=node.__loop_para__['circuit'])

    except:
        raise_error("Please provide necessary loop annotation in while loops for the transformation pass.")
    
    new_node = astroid.nodes.Module(
                    name = None,
                    doc = "",
                    parent = node.parent,
                    )

    func_name = 'while_body' + str(node.__while_num__)
    new_func = astroid.nodes.FunctionDef(name = func_name)

    new_arg = astroid.nodes.Arguments()
    new_arg.postinit(args = [circuit_name, ret_circuit_name],
                     defaults = [],
                     kwonlyargs = [],
                     kw_defaults = [],
                     annotations = [])

    new_tuple = astroid.nodes.Tuple()
    new_tuple.postinit(elts=[circuit_name, ret_circuit_name])
    assign_tuple = astroid.nodes.Tuple()
    assign_tuple.postinit(elts=[circuit_name, ret_circuit_name])
    new_ret = astroid.nodes.Return()
    new_ret.postinit(value = new_tuple)
    new_func.postinit(args = new_arg, body = node.body + [new_ret])

    new_call = astroid.nodes.Call()
    arg_list = [circuit_name, ret_circuit_name, astroid.nodes.Name(name=func_name)]

    new_assign = astroid.nodes.Assign()
    new_assign.postinit(targets=[assign_tuple], value=new_call)
    new_name = astroid.nodes.Name(name="while_iterate_transformation")

    new_call.postinit(func = new_name, args = arg_list)
    new_node.postinit(body = [new_func, new_assign])

    # print("new_node", new_node.as_string())
    return new_node

def if_binop_trans(node):

    node.test = binop_trans(node.test)

    return node

def binop_trans(node):

    if type(node) == astroid.node_classes.UnaryOp and node.op == "not":
        call = astroid.nodes.Call()
        call.postinit(func=astroid.nodes.Name(name=node.op.capitalize()), args=[binop_trans(node.operand)])
        return call
    elif type(node) == astroid.node_classes.BoolOp:
        call = astroid.nodes.Call()
        call.postinit(func=astroid.nodes.Name(name=node.op.capitalize()), args=[binop_trans(x) for x in node.values])
        return call
    else:
        return node

def get_ast(filepath, modname):

    """return an ast(roid) representation for a module"""
    return MANAGER.ast_from_file(filepath, modname, source=True)

def expand_file(file_name):
	
    """
    Take a file and expand its modules
    """

    if exists(file_name):
        try:
            modname = ".".join(modutils.modpath_from_file(file_name))
        except ImportError:
            modname = None

        filepath = normpath(file_name)
        result = {
                    "path": filepath,
                    "name": modname,
                 }
    else:            
        raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), file_name)

    return result

def extract_comments(file_name):
    
    comment_lineno_dict = {}

    with open(file_name, 'rb') as content_file:
        token_list = list(tokenize.tokenize(content_file.readline))
    
    with open(file_name, 'r') as content_file:
        content = content_file.read()

    content_line = content.split('\n')

    for tktype, tkval, _, _, line in token_list:
        if tktype == tokenize.COMMENT:

            line_clean = line.replace('\r', '') .replace('\n', '')
            lineno = content_line.index(line_clean)
            comment_lineno_dict[lineno+1] = tkval
            if tkval == "#@external":
                # print(lineno)
                global external_count
                external_count += 1
                
    
    return comment_lineno_dict


def load_proof_utils(ast_module):

    new_module = ast_module
    z3_node = astroid.extract_node("from z3 import *")
    prove_util_node = astroid.extract_node("from giallar.z3_wrapper import *")
    invariant_node = astroid.extract_node("from giallar.core.spec.invariant import *")
    loop_template_node = astroid.extract_node("from giallar.core.spec.loop_template import *")
    library_node = astroid.extract_node("from giallar.utility_library.spec import *")
    proof_util_list = [z3_node, prove_util_node, invariant_node, loop_template_node, library_node]
    new_module.postinit(body = proof_util_list + ast_module.body)

    return new_module

def add_test(ast_module, module_name):
    test_node = astroid.extract_node("if __name__ == '__main__': {}.test()".format(module_name))
    new_module = astroid.nodes.Module(name='', doc='')
    # new_module = copy.deepcopy(ast_module)
    new_module.postinit(body = ast_module.body + [test_node])

    return new_module

# Test

if __name__ == "__main__":
    # Extract comments
    # comment_lineno_dict = extract_comments('basic_swap_test.py')
    # module_data = expand_file('basic_swap_test.py')
    external_count = 0
    argParser = argparse.ArgumentParser(description='Parse the input file.')
    argParser.add_argument('--file', dest='filename', default='')
    args = argParser.parse_args()
    filename = args.filename
    filename_final = filename.split('/')[-1].split('\\')[-1]
    comment_lineno_dict = extract_comments(filename)
    module_data = expand_file(filename)

    # Extract AST
    file_path, modname = module_data['path'], module_data['name']
    module_node = get_ast(file_path, modname)
    # print(type(module_node))

    module_node = load_proof_utils(module_node)

    # Module name


    # Annotate if statements
    if_annotation_cls = annotate_if(comment_lineno_dict)
    walker = ASTWalker(if_annotation_cls)
    walker.walk(module_node)
    module_name = if_annotation_cls.module_name
    if if_annotation_cls.base_name:
        base_name = if_annotation_cls.base_name
        print(f"Find {base_name} pass")
    else:
        raise_error("Please provide a giallar compiler pass (routing, transformation or analysis).")
    
    var_info = parse_var_info(if_annotation_cls.var_dict)
    # print(var_info)
    # print(module_node.repr_tree())
    # print(module_node.as_string())

    # Transform if statements
    # module_cp = copy.deepcopy(module_node)

    transform_walker = TransformVisitor()
    bin_str = list(map(lambda x: False if x=='0' else True, list('01')))

    if_count = if_annotation_cls.if_counter + 1

    transform_walker.register_transform(astroid.FunctionDef,
                                        lambda node: function_trans(node),
                                        predicate=lambda node: True)

    transform_walker.register_transform(astroid.node_classes.If,
                                        lambda node:if_binop_trans(node),
                                        predicate=lambda node:True)

    transform_walker.register_transform(astroid.node_classes.If,
                                        lambda node:raise_error_trans(node),
                                        predicate=lambda node:
                                                      node.__raise_error_if__)

    transform_walker.register_transform(astroid.nodes.While,
                                        lambda node:while_trans(node),
                                            predicate=lambda node:if_circuit_while(node)
                                        )

    transform_walker.register_transform(astroid.nodes.ImportFrom,
                                        lambda node:import_trans(node),
                                        predicate=lambda node:if_giallar_import(node)
                                        )

    transform_walker.register_transform(astroid.nodes.Call,
                                        lambda node:astroid.extract_node("QCircuit()"),
                                        predicate=lambda node:if_qcircuit(node)
                                        )

    transform_walker.register_transform(astroid.nodes.For,
                                        lambda node:for_trans(node),
                                        predicate=lambda node:if_for_gate(node)
                                        )

    transform_walker.register_transform(astroid.nodes.Call,
                                        lambda node:twoq_trans(node),
                                        predicate=lambda node:test_twoq_node(node))

    transform_walker.visit(module_node)

    unique_module = set()
    if base_name == 'Analysis':
        module_node = add_test(module_node, module_name)
        unique_module.add(module_node.as_string())
    else:
        for i in range(2**if_count):
            bin_str = list(str(bin(i))[2:].zfill(if_count))
            # print(bin_str)
            # print(type(module_node))
            module_cp = copy.deepcopy(module_node)
            transform_walker.register_transform(astroid.node_classes.If,
                                                lambda node:if_trans_first(node)
                                                            if bin_str[node.__if_num__] == '1'
                                                            else if_trans_second(node),
                                                predicate=lambda node:
                                                          not node.__invariant_if__)
            transform_walker.visit(module_cp)
            module_cp = add_test(module_cp, module_name)
            unique_module.add(module_cp.as_string())

    for i, module in enumerate(unique_module):
        print(f"Generating {i}th subgoal")
        filename = filename.replace("\\", "")
        with open("output_files/{}_{}".format(i, filename_final), "w") as f:
            f.write(module)
    with open("output_files/{}_count.txt".format(filename_final[:-3]), "w") as f:
        f.write(str(len(unique_module)) + '\n')
    
    subgoal_count = len(unique_module) + external_count + if_annotation_cls.for_counter + if_annotation_cls.while_counter

    print(f"Total number of subgoals: {subgoal_count}, {if_annotation_cls.for_counter}")
