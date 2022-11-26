# -*- coding: utf-8 -*-
# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2018.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
#
# (C) Modified by the CertiQ team

"""
A two-ways dict to represent a layout.

Layout is the relation between virtual (qu)bits and physical (qu)bits.
Virtual (qu)bits are tuples, e.g. `(QuantumRegister(3, 'qr'), 2)` or simply `qr[2]`.
Physical (qu)bits are integers.
"""
import warnings

from giallar.core.impl.error_handler import raise_error

class Layout():
    """Two-ways dict to represent a Layout."""

    def __init__(self, input_dict=None):
        """construct a Layout from a bijective dictionary, mapping
        virtual qubits to physical qubits"""
        self._p2v = {}
        self._v2p = {}

        if input_dict is not None:
            if not isinstance(input_dict, dict):
                raise_error("Layout constructor takes a dict")
            self.from_dict(input_dict)

    def __repr__(self):
        """Representation of a Layout"""
        str_list = []
        for key, val in self._p2v.items():
            str_list.append("{k}: {v},".format(k=key, v=val))
        if str_list:
            str_list[-1] = str_list[-1][:-1]
        return "Layout({\n" + "\n".join(str_list) + "\n})"

    def from_dict(self, input_dict):
        """Populates a Layout from a dictionary.

        The dictionary must be a bijective mapping between
        virtual qubits (tuple) and physical qubits (int).

        """
        for key, value in input_dict.items():
            virtual, physical = key, value
            self._p2v[physical] = virtual
            if virtual is None:
                continue
            self._v2p[virtual] = physical

    def __getitem__(self, item):
        if item in self._p2v:
            return self._p2v[item]
        if item in self._v2p:
            return self._v2p[item]
        raise KeyError('The item %s does not exist in the Layout' % (item,))

    def __setitem__(self, key, value):
        virtual, physical = key, value
        self._set_type_checked_item(virtual, physical)

    def _set_type_checked_item(self, virtual, physical):
        old = self._v2p.pop(virtual, None)
        self._p2v.pop(old, None)
        old = self._p2v.pop(physical, None)
        self._v2p.pop(old, None)

        self._p2v[physical] = virtual
        if virtual is not None:
            self._v2p[virtual] = physical

    def __delitem__(self, key):
        if isinstance(key, int):
            del self._p2v[key]
            del self._v2p[self._p2v[key]]
        elif isinstance(key, str):
            del self._v2p[key]
            del self._p2v[self._v2p[key]]
        else:
            raise_error('The key to remove should be of the form'
                              ' Qubit or integer) and %s was provided' % (type(key),))

    def __len__(self):
        return len(self._p2v)

    def add(self, virtual_bit, physical_bit=None):
        """
        Adds a map element between `bit` and `physical_bit`. If `physical_bit` is not
        defined, `bit` will be mapped to a new physical bit (extending the length of the
        layout by one.)

        Args:
            virtual_bit (tuple): A (qu)bit. For example, (QuantumRegister(3, 'qr'), 2).
            physical_bit (int): A physical bit. For example, 3.
        """
        if physical_bit is None:
            physical_candidate = len(self)
            while physical_candidate in self._p2v:
                physical_candidate += 1
            physical_bit = physical_candidate
        self[virtual_bit] = physical_bit

    def get_virtual_bits(self):
        return self._v2p

    def get_physical_bits(self):
        return self._p2v

    def swap(self, left, right):
        if type(left) is not type(right):
            raise_error('The method swap only works with elements of the same type.')
        temp = self[left]
        self[left] = self[right]
        self[right] = temp


    def combine_into_edge_map(self, another_layout):
        """Combines self and another_layout into an "edge map".

        For example::

              self       another_layout  resulting edge map
           qr_1 -> 0        0 <- q_2         qr_1 -> q_2
           qr_2 -> 2        2 <- q_1         qr_2 -> q_1
           qr_3 -> 3        3 <- q_0         qr_3 -> q_0

        The edge map is used to compose dags via, for example, compose.

        Args:
            another_layout (Layout): The other layout to combine.
        Returns:
            dict: A "edge map".
        Raises:
            LayoutError: another_layout can be bigger than self, but not smaller.
                Otherwise, raises.
        """
        warnings.warn('combine_into_edge_map is deprecated as of 0.14.0 and '
                      'will be removed in a future release. Instead '
                      'reorder_bits() should be used', DeprecationWarning,
                      stacklevel=2)
        edge_map = dict()

        for virtual, physical in self.get_virtual_bits().items():
            if physical not in another_layout._p2v:
                raise LayoutError('The wire_map_from_layouts() method does not support when the'
                                  ' other layout (another_layout) is smaller.')
            edge_map[virtual] = another_layout[physical]

        return edge_map

    @staticmethod
    def generate_trivial_layout(qcirc):
        """Creates a trivial ("one-to-one") Layout with the registers in `regs`.

        Args:
            *regs (Registers): registers to include in the layout.
        Returns:
            Layout: A layout with all the `regs` in the given order.
        """
        layout_dict = {} 
        for i, qubit in enumerate(qcirc.qubits):
            layout_dict[qubit] = i
        layout = Layout(layout_dict)
        return layout
    
    
    @staticmethod
    def from_intlist(int_list, *qregs):
        """Converts a list of integers to a Layout
        mapping virtual qubits (index of the list) to
        physical qubits (the list values).

        Args:
            int_list (list): A list of integers.
            *qregs (QuantumRegisters): The quantum registers to apply
                the layout to.
        Returns:
            Layout: The corresponding Layout object.
        Raises:
            LayoutError: Invalid input layout.
        """
        if not all(isinstanceint(i) for i in int_list):
            raise LayoutError('Expected a list of ints')
        if len(int_list) != len(set(int_list)):
            raise LayoutError('Duplicate values not permitted; Layout is bijective.')
        num_qubits = sum(reg.size for reg in qregs)
        # Check if list is too short to cover all qubits
        if len(int_list) < num_qubits:
            err_msg = 'Integer list length must equal number of qubits in circuit.'
            raise LayoutError(err_msg)
        out = Layout()
        main_idx = 0
        for qreg in qregs:
            for idx in range(qreg.size):
                out[qreg[idx]] = int_list[main_idx]
                main_idx += 1
        if main_idx != len(int_list):
            for int_item in int_list[main_idx:]:
                out[int_item] = None
        return out

    @staticmethod
    def from_qubit_list(qubit_list):
        """
        Populates a Layout from a list containing virtual
        qubits, Qubit or None.

        Args:
            qubit_list (list):
                e.g.: [qr[0], None, qr[2], qr[3]]
        Returns:
            Layout: the corresponding Layout object
        Raises:
            LayoutError: If the elements are not Qubit or None
        """
        out = Layout()
        for physical, virtual in enumerate(qubit_list):
            if virtual is None:
                continue
            if isinstance(virtual, Qubit):
                if virtual in out._v2p:
                    raise LayoutError('Duplicate values not permitted; Layout is bijective.')
                out[virtual] = physical
            else:
                raise LayoutError("The list should contain elements of the Bits or NoneTypes")
        return out

    def copy(self):
        """Returns a copy of a Layout instance."""
        layout_copy = type(self)()

        layout_copy._p2v = self._p2v.copy()
        layout_copy._v2p = self._v2p.copy()

        return layout_copy


class Permutation:
    
    def __init__(self, qubits):
        self._n2i = {}
        self._i2n = {}
        for q in qubits:
            self._n2i[q] = q
            self._i2n[q] = q

    def swap(self, x, y):

        a = self._n2i[x]
        b = self._n2i[y]
        self._n2i[x] = b
        self._n2i[y] = a
        self._i2n[a] = y
        self._i2n[b] = x

        return self


def update_layout_with_perm(initial_layout, perm):

    layout = Layout()

    for keys in initial_layout._v2p:

        p_key = initial_layout._v2p[keys]
        layout._v2p[perm._n2i[keys]] = p_key
        layout._p2v[p_key] = perm._n2i[keys]
        
    return layout
