OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];

h q[4];
cx q[0], q[4];
cx q[0], q[4];

