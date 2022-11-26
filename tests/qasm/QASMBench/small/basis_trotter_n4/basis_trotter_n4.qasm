// Generated from Cirq v0.8.0
OPENQASM 2.0;
include "qelib1.inc";

// Qubits: [0, 1, 2, 3]
qreg q[4];
creg c[4];

z q[0];
z q[1];
z q[2];
z q[3];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

// Gate: PhasedISWAP**0.08130614625631793
rz(pi*0.25) q[0];
rz(pi*-0.25) q[1];
cx q[0],q[1];
h q[0];
cx q[1],q[0];
rz(pi*0.0406530731) q[0];
cx q[1],q[0];
rz(pi*-0.0406530731) q[0];
h q[0];
cx q[0],q[1];
rz(pi*-0.25) q[0];
rz(pi*0.25) q[1];

// Gate: PhasedISWAP**-0.08130614625631793
rz(pi*0.25) q[2];
rz(pi*-0.25) q[3];
cx q[2],q[3];
h q[2];
cx q[3],q[2];
rz(pi*-0.0406530731) q[2];
cx q[3],q[2];
rz(pi*0.0406530731) q[2];
h q[2];
cx q[2],q[3];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[3];

rz(pi*0.1123177385) q[0];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

rz(pi*0.1123177385) q[1];
rz(pi*0.0564909955) q[3];
rz(pi*0.0564909955) q[2];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

// Gate: PhasedISWAP**-0.05102950815299322
rz(pi*0.25) q[0];
rz(pi*-0.25) q[1];
cx q[0],q[1];
h q[0];
cx q[1],q[0];
rz(pi*-0.0255147541) q[0];
cx q[1],q[0];
rz(pi*0.0255147541) q[0];
h q[0];
cx q[0],q[1];
rz(pi*-0.25) q[0];
rz(pi*0.25) q[1];

// Gate: PhasedISWAP**0.05102950815299322
rz(pi*0.25) q[2];
rz(pi*-0.25) q[3];
cx q[2],q[3];
h q[2];
cx q[3],q[2];
rz(pi*0.0255147541) q[2];
cx q[3],q[2];
rz(pi*-0.0255147541) q[2];
h q[2];
cx q[2],q[3];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[3];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

// Gate: CZ**-0.048279591094340914
u3(pi*0.5,0,pi*0.5) q[0];
u3(pi*0.5,pi*1.0,pi*1.0) q[1];
rx(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*0.4758602045) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[0],q[1];
u3(pi*0.5,pi*0.4758602045,pi*1.0) q[0];
u3(pi*0.5,pi*1.9758602045,0) q[1];

swap q[0],q[1];

// Gate: CZ**-0.022156912718971442
u3(pi*0.5,0,pi*1.75) q[2];
u3(pi*0.5,pi*1.0,pi*1.25) q[3];
rx(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*0.4889215436) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*-0.5) q[3];
rz(pi*0.5) q[3];
cx q[2],q[3];
u3(pi*0.5,pi*1.2389215436,pi*1.0) q[2];
u3(pi*0.5,pi*1.7389215436,0) q[3];

swap q[2],q[3];

// Gate: CZ**-0.03270667647415345
u3(pi*0.5,0,0) q[1];
u3(pi*0.5,pi*1.0,pi*1.5) q[2];
rx(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*0.4836466618) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[1],q[2];
u3(pi*0.5,pi*0.9836466618,pi*1.0) q[1];
u3(pi*0.5,pi*1.4836466618,0) q[2];

swap q[1],q[2];

// Gate: CZ**-0.03270667647415345
u3(pi*0.5,0,0) q[0];
u3(pi*0.5,pi*1.0,pi*1.5) q[1];
rx(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*0.4836466618) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[0],q[1];
u3(pi*0.5,pi*0.9836466618,pi*1.0) q[0];
u3(pi*0.5,pi*1.4836466618,0) q[1];

// Gate: CZ**-0.03270667647415345
u3(pi*0.5,0,0) q[2];
u3(pi*0.5,pi*1.0,pi*1.5) q[3];
rx(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*0.4836466618) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*-0.5) q[3];
rz(pi*0.5) q[3];
cx q[2],q[3];
u3(pi*0.5,pi*0.9836466618,pi*1.0) q[2];
u3(pi*0.5,pi*1.4836466618,0) q[3];

swap q[0],q[1];
swap q[2],q[3];

// Gate: CZ**-0.03270667647415345
u3(pi*0.5,0,0) q[1];
u3(pi*0.5,pi*1.0,pi*1.5) q[2];
rx(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*0.4836466618) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[1],q[2];
u3(pi*0.5,pi*0.9836466618,pi*1.0) q[1];
u3(pi*0.5,pi*1.4836466618,0) q[2];

rz(pi*-0.0241397955) q[3];
rz(pi*-0.0110784564) q[0];
swap q[1],q[2];
rz(pi*-0.0241397955) q[2];
rz(pi*-0.0110784564) q[1];
z q[2];
z q[1];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[2];
rz(pi*-0.25) q[1];
cx q[2],q[1];
h q[2];
cx q[1],q[2];
rz(pi*-0.5) q[2];
cx q[1],q[2];
rz(pi*0.5) q[2];
h q[2];
cx q[2],q[1];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[1];

// Gate: PhasedISWAP**-0.9500630905158097
rz(pi*0.25) q[3];
rz(pi*-0.25) q[2];
cx q[3],q[2];
h q[3];
cx q[2],q[3];
rz(pi*-0.4750315453) q[3];
cx q[2],q[3];
rz(pi*0.4750315453) q[3];
h q[3];
cx q[3],q[2];
rz(pi*-0.25) q[3];
rz(pi*0.25) q[2];

// Gate: PhasedISWAP**0.9500630905158097
rz(pi*0.25) q[1];
rz(pi*-0.25) q[0];
cx q[1],q[0];
h q[1];
cx q[0],q[1];
rz(pi*0.4750315453) q[1];
cx q[0],q[1];
rz(pi*-0.4750315453) q[1];
h q[1];
cx q[1],q[0];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[0];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[2];
rz(pi*-0.25) q[1];
cx q[2],q[1];
h q[2];
cx q[1],q[2];
rz(pi*-0.5) q[2];
cx q[1],q[2];
rz(pi*0.5) q[2];
h q[2];
cx q[2],q[1];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[1];

// Gate: CZ**-0.013654184706660842
u3(pi*0.5,0,pi*1.5) q[3];
u3(pi*0.5,pi*1.0,pi*1.0) q[2];
rx(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*0.4931729076) q[3];
ry(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[3],q[2];
u3(pi*0.5,pi*1.4931729076,pi*1.0) q[3];
u3(pi*0.5,pi*1.9931729076,0) q[2];

swap q[3],q[2];

// Gate: CZ**-0.006328040119021747
u3(pi*0.5,0,pi*1.4961253835) q[1];
u3(pi*0.5,pi*1.0,pi*1.9961253835) q[0];
rx(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*0.4968359799) q[1];
ry(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*-0.5) q[0];
rz(pi*0.5) q[0];
cx q[1],q[0];
u3(pi*0.5,pi*1.5007105964,pi*1.0) q[1];
u3(pi*0.5,pi*1.0007105964,0) q[0];

swap q[1],q[0];

// Gate: CZ**0.009295387491454189
u3(pi*0.5,pi*1.0,pi*1.0820521548) q[2];
u3(pi*0.5,pi*1.0,pi*1.5820521548) q[1];
rx(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*0.4953523063) q[2];
ry(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[2],q[1];
u3(pi*0.5,pi*1.9225955389,0) q[2];
u3(pi*0.5,pi*1.4225955389,0) q[1];

swap q[2],q[1];

// Gate: CZ**0.009295387491454189
u3(pi*0.5,pi*1.0,pi*1.0820521548) q[3];
u3(pi*0.5,pi*1.0,pi*1.5820521548) q[2];
rx(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*0.4953523063) q[3];
ry(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[3],q[2];
u3(pi*0.5,pi*1.9225955389,0) q[3];
u3(pi*0.5,pi*1.4225955389,0) q[2];

// Gate: CZ**0.009295387491454189
u3(pi*0.5,pi*1.0,pi*1.0820521548) q[1];
u3(pi*0.5,pi*1.0,pi*1.5820521548) q[0];
rx(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*0.4953523063) q[1];
ry(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*-0.5) q[0];
rz(pi*0.5) q[0];
cx q[1],q[0];
u3(pi*0.5,pi*1.9225955389,0) q[1];
u3(pi*0.5,pi*1.4225955389,0) q[0];

swap q[3],q[2];
swap q[1],q[0];

// Gate: CZ**0.009295387491454189
u3(pi*0.5,pi*1.0,pi*1.0820521548) q[2];
u3(pi*0.5,pi*1.0,pi*1.5820521548) q[1];
rx(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*0.4953523063) q[2];
ry(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[2],q[1];
u3(pi*0.5,pi*1.9225955389,0) q[2];
u3(pi*0.5,pi*1.4225955389,0) q[1];

rz(pi*-0.0068270924) q[0];
rz(pi*-0.0031640201) q[3];
swap q[2],q[1];
z q[0];
z q[3];
rz(pi*-0.0068270924) q[1];
rz(pi*-0.0031640201) q[2];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

// Gate: PhasedISWAP**-0.5017530508495694
rz(pi*0.25) q[0];
rz(pi*-0.25) q[1];
cx q[0],q[1];
h q[0];
cx q[1],q[0];
rz(pi*-0.2508765254) q[0];
cx q[1],q[0];
rz(pi*0.2508765254) q[0];
h q[0];
cx q[0],q[1];
rz(pi*-0.25) q[0];
rz(pi*0.25) q[1];

// Gate: PhasedISWAP**0.5017530508495694
rz(pi*0.25) q[2];
rz(pi*-0.25) q[3];
cx q[2],q[3];
h q[2];
cx q[3],q[2];
rz(pi*0.2508765254) q[2];
cx q[3],q[2];
rz(pi*-0.2508765254) q[2];
h q[2];
cx q[2],q[3];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[3];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

// Gate: CZ**-0.00046375097365492423
u3(pi*0.5,0,pi*1.5001274262) q[0];
u3(pi*0.5,pi*1.0,pi*1.0001274262) q[1];
rx(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*0.4997681245) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[0],q[1];
u3(pi*0.5,pi*1.4996406983,pi*1.0) q[0];
u3(pi*0.5,pi*1.9996406983,0) q[1];

swap q[0],q[1];

// Gate: CZ**-0.0004129506013584246
u3(pi*0.5,pi*1.0,pi*1.4998373235) q[2];
u3(pi*0.5,0,pi*1.9998373235) q[3];
rx(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*0.4997935247) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*-0.5) q[3];
rz(pi*0.5) q[3];
cx q[2],q[3];
u3(pi*0.5,pi*1.4999562012,0) q[2];
u3(pi*0.5,pi*0.9999562012,pi*1.0) q[3];

swap q[2],q[3];

// Gate: CZ**0.00043761426330885954
u3(pi*0.5,0,pi*1.9993457511) q[1];
u3(pi*0.5,0,pi*1.4993457511) q[2];
rx(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*0.4997811929) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[1],q[2];
u3(pi*0.5,pi*1.0008730561,pi*1.0) q[1];
u3(pi*0.5,pi*1.5008730561,pi*1.0) q[2];

swap q[1],q[2];

// Gate: CZ**0.00043761426330885954
u3(pi*0.5,0,pi*1.9993457511) q[0];
u3(pi*0.5,0,pi*1.4993457511) q[1];
rx(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*0.4997811929) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[0],q[1];
u3(pi*0.5,pi*1.0008730561,pi*1.0) q[0];
u3(pi*0.5,pi*1.5008730561,pi*1.0) q[1];

// Gate: CZ**0.00043761426330885954
u3(pi*0.5,0,pi*1.9993457511) q[2];
u3(pi*0.5,0,pi*1.4993457511) q[3];
rx(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*0.4997811929) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*-0.5) q[3];
rz(pi*0.5) q[3];
cx q[2],q[3];
u3(pi*0.5,pi*1.0008730561,pi*1.0) q[2];
u3(pi*0.5,pi*1.5008730561,pi*1.0) q[3];

swap q[0],q[1];
swap q[2],q[3];

// Gate: CZ**0.00043761426330885954
u3(pi*0.5,0,pi*1.9993457511) q[1];
u3(pi*0.5,0,pi*1.4993457511) q[2];
rx(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*0.4997811929) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[1],q[2];
u3(pi*0.5,pi*1.0008730561,pi*1.0) q[1];
u3(pi*0.5,pi*1.5008730561,pi*1.0) q[2];

rz(pi*-0.0002318755) q[3];
rz(pi*-0.0002064753) q[0];
swap q[1],q[2];
z q[3];
z q[0];
rz(pi*-0.0002318755) q[2];
rz(pi*-0.0002064753) q[1];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[2];
rz(pi*-0.25) q[1];
cx q[2],q[1];
h q[2];
cx q[1],q[2];
rz(pi*-0.5) q[2];
cx q[1],q[2];
rz(pi*0.5) q[2];
h q[2];
cx q[2],q[1];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[1];

// Gate: PhasedISWAP**-0.4158482042253096
rz(pi*0.25) q[3];
rz(pi*-0.25) q[2];
cx q[3],q[2];
h q[3];
cx q[2],q[3];
rz(pi*-0.2079241021) q[3];
cx q[2],q[3];
rz(pi*0.2079241021) q[3];
h q[3];
cx q[3],q[2];
rz(pi*-0.25) q[3];
rz(pi*0.25) q[2];

// Gate: PhasedISWAP**0.4158482042253096
rz(pi*0.25) q[1];
rz(pi*-0.25) q[0];
cx q[1],q[0];
h q[1];
cx q[0],q[1];
rz(pi*0.2079241021) q[1];
cx q[0],q[1];
rz(pi*-0.2079241021) q[1];
h q[1];
cx q[1],q[0];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[0];

z q[3];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[2];
rz(pi*-0.25) q[1];
cx q[2],q[1];
h q[2];
cx q[1],q[2];
rz(pi*-0.5) q[2];
cx q[1],q[2];
rz(pi*0.5) q[2];
h q[2];
cx q[2],q[1];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[1];

z q[2];
z q[0];
z q[1];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[2];
rz(pi*-0.25) q[1];
cx q[2],q[1];
h q[2];
cx q[1],q[2];
rz(pi*-0.5) q[2];
cx q[1],q[2];
rz(pi*0.5) q[2];
h q[2];
cx q[2],q[1];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[1];

// Gate: PhasedISWAP**0.08130614625631793
rz(pi*0.25) q[3];
rz(pi*-0.25) q[2];
cx q[3],q[2];
h q[3];
cx q[2],q[3];
rz(pi*0.0406530731) q[3];
cx q[2],q[3];
rz(pi*-0.0406530731) q[3];
h q[3];
cx q[3],q[2];
rz(pi*-0.25) q[3];
rz(pi*0.25) q[2];

// Gate: PhasedISWAP**-0.08130614625631793
rz(pi*0.25) q[1];
rz(pi*-0.25) q[0];
cx q[1],q[0];
h q[1];
cx q[0],q[1];
rz(pi*-0.0406530731) q[1];
cx q[0],q[1];
rz(pi*0.0406530731) q[1];
h q[1];
cx q[1],q[0];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[0];

rz(pi*0.1123177385) q[3];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[2];
rz(pi*-0.25) q[1];
cx q[2],q[1];
h q[2];
cx q[1],q[2];
rz(pi*-0.5) q[2];
cx q[1],q[2];
rz(pi*0.5) q[2];
h q[2];
cx q[2],q[1];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[1];

rz(pi*0.1123177385) q[2];
rz(pi*0.0564909955) q[0];
rz(pi*0.0564909955) q[1];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[2];
rz(pi*-0.25) q[1];
cx q[2],q[1];
h q[2];
cx q[1],q[2];
rz(pi*-0.5) q[2];
cx q[1],q[2];
rz(pi*0.5) q[2];
h q[2];
cx q[2],q[1];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[1];

// Gate: PhasedISWAP**-0.05102950815299322
rz(pi*0.25) q[3];
rz(pi*-0.25) q[2];
cx q[3],q[2];
h q[3];
cx q[2],q[3];
rz(pi*-0.0255147541) q[3];
cx q[2],q[3];
rz(pi*0.0255147541) q[3];
h q[3];
cx q[3],q[2];
rz(pi*-0.25) q[3];
rz(pi*0.25) q[2];

// Gate: PhasedISWAP**0.05102950815299322
rz(pi*0.25) q[1];
rz(pi*-0.25) q[0];
cx q[1],q[0];
h q[1];
cx q[0],q[1];
rz(pi*0.0255147541) q[1];
cx q[0],q[1];
rz(pi*-0.0255147541) q[1];
h q[1];
cx q[1],q[0];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[0];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[2];
rz(pi*-0.25) q[1];
cx q[2],q[1];
h q[2];
cx q[1],q[2];
rz(pi*-0.5) q[2];
cx q[1],q[2];
rz(pi*0.5) q[2];
h q[2];
cx q[2],q[1];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[1];

// Gate: CZ**-0.048279591094340914
u3(pi*0.5,0,pi*0.5) q[3];
u3(pi*0.5,pi*1.0,pi*1.0) q[2];
rx(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*0.4758602045) q[3];
ry(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[3],q[2];
u3(pi*0.5,pi*0.4758602045,pi*1.0) q[3];
u3(pi*0.5,pi*1.9758602045,0) q[2];

swap q[3],q[2];

// Gate: CZ**-0.022156912718971442
u3(pi*0.5,0,pi*1.75) q[1];
u3(pi*0.5,pi*1.0,pi*1.25) q[0];
rx(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*0.4889215436) q[1];
ry(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*-0.5) q[0];
rz(pi*0.5) q[0];
cx q[1],q[0];
u3(pi*0.5,pi*1.2389215436,pi*1.0) q[1];
u3(pi*0.5,pi*1.7389215436,0) q[0];

swap q[1],q[0];

// Gate: CZ**-0.03270667647415345
u3(pi*0.5,0,0) q[2];
u3(pi*0.5,pi*1.0,pi*1.5) q[1];
rx(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*0.4836466618) q[2];
ry(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[2],q[1];
u3(pi*0.5,pi*0.9836466618,pi*1.0) q[2];
u3(pi*0.5,pi*1.4836466618,0) q[1];

swap q[2],q[1];

// Gate: CZ**-0.03270667647415345
u3(pi*0.5,0,0) q[3];
u3(pi*0.5,pi*1.0,pi*1.5) q[2];
rx(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*0.4836466618) q[3];
ry(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[3],q[2];
u3(pi*0.5,pi*0.9836466618,pi*1.0) q[3];
u3(pi*0.5,pi*1.4836466618,0) q[2];

// Gate: CZ**-0.03270667647415345
u3(pi*0.5,0,0) q[1];
u3(pi*0.5,pi*1.0,pi*1.5) q[0];
rx(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*0.4836466618) q[1];
ry(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*-0.5) q[0];
rz(pi*0.5) q[0];
cx q[1],q[0];
u3(pi*0.5,pi*0.9836466618,pi*1.0) q[1];
u3(pi*0.5,pi*1.4836466618,0) q[0];

swap q[3],q[2];
swap q[1],q[0];

// Gate: CZ**-0.03270667647415345
u3(pi*0.5,0,0) q[2];
u3(pi*0.5,pi*1.0,pi*1.5) q[1];
rx(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*0.4836466618) q[2];
ry(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[2],q[1];
u3(pi*0.5,pi*0.9836466618,pi*1.0) q[2];
u3(pi*0.5,pi*1.4836466618,0) q[1];

rz(pi*-0.0241397955) q[0];
rz(pi*-0.0110784564) q[3];
swap q[2],q[1];
rz(pi*-0.0241397955) q[1];
rz(pi*-0.0110784564) q[2];
z q[1];
z q[2];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

// Gate: PhasedISWAP**-0.9500630905158097
rz(pi*0.25) q[0];
rz(pi*-0.25) q[1];
cx q[0],q[1];
h q[0];
cx q[1],q[0];
rz(pi*-0.4750315453) q[0];
cx q[1],q[0];
rz(pi*0.4750315453) q[0];
h q[0];
cx q[0],q[1];
rz(pi*-0.25) q[0];
rz(pi*0.25) q[1];

// Gate: PhasedISWAP**0.9500630905158097
rz(pi*0.25) q[2];
rz(pi*-0.25) q[3];
cx q[2],q[3];
h q[2];
cx q[3],q[2];
rz(pi*0.4750315453) q[2];
cx q[3],q[2];
rz(pi*-0.4750315453) q[2];
h q[2];
cx q[2],q[3];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[3];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

// Gate: CZ**-0.013654184706660842
u3(pi*0.5,0,pi*1.5) q[0];
u3(pi*0.5,pi*1.0,pi*1.0) q[1];
rx(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*0.4931729076) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[0],q[1];
u3(pi*0.5,pi*1.4931729076,pi*1.0) q[0];
u3(pi*0.5,pi*1.9931729076,0) q[1];

swap q[0],q[1];

// Gate: CZ**-0.006328040119021747
u3(pi*0.5,0,pi*1.4961253835) q[2];
u3(pi*0.5,pi*1.0,pi*1.9961253835) q[3];
rx(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*0.4968359799) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*-0.5) q[3];
rz(pi*0.5) q[3];
cx q[2],q[3];
u3(pi*0.5,pi*1.5007105964,pi*1.0) q[2];
u3(pi*0.5,pi*1.0007105964,0) q[3];

swap q[2],q[3];

// Gate: CZ**0.009295387491454189
u3(pi*0.5,pi*1.0,pi*1.0820521548) q[1];
u3(pi*0.5,pi*1.0,pi*1.5820521548) q[2];
rx(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*0.4953523063) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[1],q[2];
u3(pi*0.5,pi*1.9225955389,0) q[1];
u3(pi*0.5,pi*1.4225955389,0) q[2];

swap q[1],q[2];

// Gate: CZ**0.009295387491454189
u3(pi*0.5,pi*1.0,pi*1.0820521548) q[0];
u3(pi*0.5,pi*1.0,pi*1.5820521548) q[1];
rx(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*0.4953523063) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[0],q[1];
u3(pi*0.5,pi*1.9225955389,0) q[0];
u3(pi*0.5,pi*1.4225955389,0) q[1];

// Gate: CZ**0.009295387491454189
u3(pi*0.5,pi*1.0,pi*1.0820521548) q[2];
u3(pi*0.5,pi*1.0,pi*1.5820521548) q[3];
rx(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*0.4953523063) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*-0.5) q[3];
rz(pi*0.5) q[3];
cx q[2],q[3];
u3(pi*0.5,pi*1.9225955389,0) q[2];
u3(pi*0.5,pi*1.4225955389,0) q[3];

swap q[0],q[1];
swap q[2],q[3];

// Gate: CZ**0.009295387491454189
u3(pi*0.5,pi*1.0,pi*1.0820521548) q[1];
u3(pi*0.5,pi*1.0,pi*1.5820521548) q[2];
rx(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*0.4953523063) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[1],q[2];
u3(pi*0.5,pi*1.9225955389,0) q[1];
u3(pi*0.5,pi*1.4225955389,0) q[2];

rz(pi*-0.0068270924) q[3];
rz(pi*-0.0031640201) q[0];
swap q[1],q[2];
z q[3];
z q[0];
rz(pi*-0.0068270924) q[2];
rz(pi*-0.0031640201) q[1];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[2];
rz(pi*-0.25) q[1];
cx q[2],q[1];
h q[2];
cx q[1],q[2];
rz(pi*-0.5) q[2];
cx q[1],q[2];
rz(pi*0.5) q[2];
h q[2];
cx q[2],q[1];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[1];

// Gate: PhasedISWAP**-0.5017530508495694
rz(pi*0.25) q[3];
rz(pi*-0.25) q[2];
cx q[3],q[2];
h q[3];
cx q[2],q[3];
rz(pi*-0.2508765254) q[3];
cx q[2],q[3];
rz(pi*0.2508765254) q[3];
h q[3];
cx q[3],q[2];
rz(pi*-0.25) q[3];
rz(pi*0.25) q[2];

// Gate: PhasedISWAP**0.5017530508495694
rz(pi*0.25) q[1];
rz(pi*-0.25) q[0];
cx q[1],q[0];
h q[1];
cx q[0],q[1];
rz(pi*0.2508765254) q[1];
cx q[0],q[1];
rz(pi*-0.2508765254) q[1];
h q[1];
cx q[1],q[0];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[0];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[2];
rz(pi*-0.25) q[1];
cx q[2],q[1];
h q[2];
cx q[1],q[2];
rz(pi*-0.5) q[2];
cx q[1],q[2];
rz(pi*0.5) q[2];
h q[2];
cx q[2],q[1];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[1];

// Gate: CZ**-0.00046375097365492423
u3(pi*0.5,0,pi*1.5001274262) q[3];
u3(pi*0.5,pi*1.0,pi*1.0001274262) q[2];
rx(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*0.4997681245) q[3];
ry(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[3],q[2];
u3(pi*0.5,pi*1.4996406983,pi*1.0) q[3];
u3(pi*0.5,pi*1.9996406983,0) q[2];

swap q[3],q[2];

// Gate: CZ**-0.0004129506013584246
u3(pi*0.5,pi*1.0,pi*1.4998373235) q[1];
u3(pi*0.5,0,pi*1.9998373235) q[0];
rx(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*0.4997935247) q[1];
ry(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*-0.5) q[0];
rz(pi*0.5) q[0];
cx q[1],q[0];
u3(pi*0.5,pi*1.4999562012,0) q[1];
u3(pi*0.5,pi*0.9999562012,pi*1.0) q[0];

swap q[1],q[0];

// Gate: CZ**0.00043761426330885954
u3(pi*0.5,0,pi*1.9993457511) q[2];
u3(pi*0.5,0,pi*1.4993457511) q[1];
rx(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*0.4997811929) q[2];
ry(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[2],q[1];
u3(pi*0.5,pi*1.0008730561,pi*1.0) q[2];
u3(pi*0.5,pi*1.5008730561,pi*1.0) q[1];

swap q[2],q[1];

// Gate: CZ**0.00043761426330885954
u3(pi*0.5,0,pi*1.9993457511) q[3];
u3(pi*0.5,0,pi*1.4993457511) q[2];
rx(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*0.4997811929) q[3];
ry(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[3],q[2];
u3(pi*0.5,pi*1.0008730561,pi*1.0) q[3];
u3(pi*0.5,pi*1.5008730561,pi*1.0) q[2];

// Gate: CZ**0.00043761426330885954
u3(pi*0.5,0,pi*1.9993457511) q[1];
u3(pi*0.5,0,pi*1.4993457511) q[0];
rx(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*0.4997811929) q[1];
ry(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*-0.5) q[0];
rz(pi*0.5) q[0];
cx q[1],q[0];
u3(pi*0.5,pi*1.0008730561,pi*1.0) q[1];
u3(pi*0.5,pi*1.5008730561,pi*1.0) q[0];

swap q[3],q[2];
swap q[1],q[0];

// Gate: CZ**0.00043761426330885954
u3(pi*0.5,0,pi*1.9993457511) q[2];
u3(pi*0.5,0,pi*1.4993457511) q[1];
rx(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*0.4997811929) q[2];
ry(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[2],q[1];
u3(pi*0.5,pi*1.0008730561,pi*1.0) q[2];
u3(pi*0.5,pi*1.5008730561,pi*1.0) q[1];

rz(pi*-0.0002318755) q[0];
rz(pi*-0.0002064753) q[3];
swap q[2],q[1];
z q[0];
z q[3];
rz(pi*-0.0002318755) q[1];
rz(pi*-0.0002064753) q[2];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

// Gate: PhasedISWAP**-0.4158482042253096
rz(pi*0.25) q[0];
rz(pi*-0.25) q[1];
cx q[0],q[1];
h q[0];
cx q[1],q[0];
rz(pi*-0.2079241021) q[0];
cx q[1],q[0];
rz(pi*0.2079241021) q[0];
h q[0];
cx q[0],q[1];
rz(pi*-0.25) q[0];
rz(pi*0.25) q[1];

// Gate: PhasedISWAP**0.4158482042253096
rz(pi*0.25) q[2];
rz(pi*-0.25) q[3];
cx q[2],q[3];
h q[2];
cx q[3],q[2];
rz(pi*0.2079241021) q[2];
cx q[3],q[2];
rz(pi*-0.2079241021) q[2];
h q[2];
cx q[2],q[3];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[3];

z q[0];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

z q[1];
z q[3];
z q[2];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

// Gate: PhasedISWAP**0.08130614625631793
rz(pi*0.25) q[0];
rz(pi*-0.25) q[1];
cx q[0],q[1];
h q[0];
cx q[1],q[0];
rz(pi*0.0406530731) q[0];
cx q[1],q[0];
rz(pi*-0.0406530731) q[0];
h q[0];
cx q[0],q[1];
rz(pi*-0.25) q[0];
rz(pi*0.25) q[1];

// Gate: PhasedISWAP**-0.08130614625631793
rz(pi*0.25) q[2];
rz(pi*-0.25) q[3];
cx q[2],q[3];
h q[2];
cx q[3],q[2];
rz(pi*-0.0406530731) q[2];
cx q[3],q[2];
rz(pi*0.0406530731) q[2];
h q[2];
cx q[2],q[3];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[3];

rz(pi*0.1123177385) q[0];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

rz(pi*0.1123177385) q[1];
rz(pi*0.0564909955) q[3];
rz(pi*0.0564909955) q[2];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

// Gate: PhasedISWAP**-0.05102950815299322
rz(pi*0.25) q[0];
rz(pi*-0.25) q[1];
cx q[0],q[1];
h q[0];
cx q[1],q[0];
rz(pi*-0.0255147541) q[0];
cx q[1],q[0];
rz(pi*0.0255147541) q[0];
h q[0];
cx q[0],q[1];
rz(pi*-0.25) q[0];
rz(pi*0.25) q[1];

// Gate: PhasedISWAP**0.05102950815299322
rz(pi*0.25) q[2];
rz(pi*-0.25) q[3];
cx q[2],q[3];
h q[2];
cx q[3],q[2];
rz(pi*0.0255147541) q[2];
cx q[3],q[2];
rz(pi*-0.0255147541) q[2];
h q[2];
cx q[2],q[3];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[3];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

// Gate: CZ**-0.048279591094340914
u3(pi*0.5,0,pi*0.5) q[0];
u3(pi*0.5,pi*1.0,pi*1.0) q[1];
rx(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*0.4758602045) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[0],q[1];
u3(pi*0.5,pi*0.4758602045,pi*1.0) q[0];
u3(pi*0.5,pi*1.9758602045,0) q[1];

swap q[0],q[1];

// Gate: CZ**-0.022156912718971442
u3(pi*0.5,0,pi*1.75) q[2];
u3(pi*0.5,pi*1.0,pi*1.25) q[3];
rx(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*0.4889215436) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*-0.5) q[3];
rz(pi*0.5) q[3];
cx q[2],q[3];
u3(pi*0.5,pi*1.2389215436,pi*1.0) q[2];
u3(pi*0.5,pi*1.7389215436,0) q[3];

swap q[2],q[3];

// Gate: CZ**-0.03270667647415345
u3(pi*0.5,0,0) q[1];
u3(pi*0.5,pi*1.0,pi*1.5) q[2];
rx(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*0.4836466618) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[1],q[2];
u3(pi*0.5,pi*0.9836466618,pi*1.0) q[1];
u3(pi*0.5,pi*1.4836466618,0) q[2];

swap q[1],q[2];

// Gate: CZ**-0.03270667647415345
u3(pi*0.5,0,0) q[0];
u3(pi*0.5,pi*1.0,pi*1.5) q[1];
rx(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*0.4836466618) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[0],q[1];
u3(pi*0.5,pi*0.9836466618,pi*1.0) q[0];
u3(pi*0.5,pi*1.4836466618,0) q[1];

// Gate: CZ**-0.03270667647415345
u3(pi*0.5,0,0) q[2];
u3(pi*0.5,pi*1.0,pi*1.5) q[3];
rx(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*0.4836466618) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*-0.5) q[3];
rz(pi*0.5) q[3];
cx q[2],q[3];
u3(pi*0.5,pi*0.9836466618,pi*1.0) q[2];
u3(pi*0.5,pi*1.4836466618,0) q[3];

swap q[0],q[1];
swap q[2],q[3];

// Gate: CZ**-0.03270667647415345
u3(pi*0.5,0,0) q[1];
u3(pi*0.5,pi*1.0,pi*1.5) q[2];
rx(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*0.4836466618) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[1],q[2];
u3(pi*0.5,pi*0.9836466618,pi*1.0) q[1];
u3(pi*0.5,pi*1.4836466618,0) q[2];

rz(pi*-0.0241397955) q[3];
rz(pi*-0.0110784564) q[0];
swap q[1],q[2];
rz(pi*-0.0241397955) q[2];
rz(pi*-0.0110784564) q[1];
z q[2];
z q[1];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[2];
rz(pi*-0.25) q[1];
cx q[2],q[1];
h q[2];
cx q[1],q[2];
rz(pi*-0.5) q[2];
cx q[1],q[2];
rz(pi*0.5) q[2];
h q[2];
cx q[2],q[1];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[1];

// Gate: PhasedISWAP**-0.9500630905158097
rz(pi*0.25) q[3];
rz(pi*-0.25) q[2];
cx q[3],q[2];
h q[3];
cx q[2],q[3];
rz(pi*-0.4750315453) q[3];
cx q[2],q[3];
rz(pi*0.4750315453) q[3];
h q[3];
cx q[3],q[2];
rz(pi*-0.25) q[3];
rz(pi*0.25) q[2];

// Gate: PhasedISWAP**0.9500630905158097
rz(pi*0.25) q[1];
rz(pi*-0.25) q[0];
cx q[1],q[0];
h q[1];
cx q[0],q[1];
rz(pi*0.4750315453) q[1];
cx q[0],q[1];
rz(pi*-0.4750315453) q[1];
h q[1];
cx q[1],q[0];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[0];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[2];
rz(pi*-0.25) q[1];
cx q[2],q[1];
h q[2];
cx q[1],q[2];
rz(pi*-0.5) q[2];
cx q[1],q[2];
rz(pi*0.5) q[2];
h q[2];
cx q[2],q[1];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[1];

// Gate: CZ**-0.013654184706660842
u3(pi*0.5,0,pi*1.5) q[3];
u3(pi*0.5,pi*1.0,pi*1.0) q[2];
rx(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*0.4931729076) q[3];
ry(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[3],q[2];
u3(pi*0.5,pi*1.4931729076,pi*1.0) q[3];
u3(pi*0.5,pi*1.9931729076,0) q[2];

swap q[3],q[2];

// Gate: CZ**-0.006328040119021747
u3(pi*0.5,0,pi*1.4961253835) q[1];
u3(pi*0.5,pi*1.0,pi*1.9961253835) q[0];
rx(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*0.4968359799) q[1];
ry(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*-0.5) q[0];
rz(pi*0.5) q[0];
cx q[1],q[0];
u3(pi*0.5,pi*1.5007105964,pi*1.0) q[1];
u3(pi*0.5,pi*1.0007105964,0) q[0];

swap q[1],q[0];

// Gate: CZ**0.009295387491454189
u3(pi*0.5,pi*1.0,pi*1.0820521548) q[2];
u3(pi*0.5,pi*1.0,pi*1.5820521548) q[1];
rx(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*0.4953523063) q[2];
ry(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[2],q[1];
u3(pi*0.5,pi*1.9225955389,0) q[2];
u3(pi*0.5,pi*1.4225955389,0) q[1];

swap q[2],q[1];

// Gate: CZ**0.009295387491454189
u3(pi*0.5,pi*1.0,pi*1.0820521548) q[3];
u3(pi*0.5,pi*1.0,pi*1.5820521548) q[2];
rx(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*0.4953523063) q[3];
ry(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[3],q[2];
u3(pi*0.5,pi*1.9225955389,0) q[3];
u3(pi*0.5,pi*1.4225955389,0) q[2];

// Gate: CZ**0.009295387491454189
u3(pi*0.5,pi*1.0,pi*1.0820521548) q[1];
u3(pi*0.5,pi*1.0,pi*1.5820521548) q[0];
rx(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*0.4953523063) q[1];
ry(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*-0.5) q[0];
rz(pi*0.5) q[0];
cx q[1],q[0];
u3(pi*0.5,pi*1.9225955389,0) q[1];
u3(pi*0.5,pi*1.4225955389,0) q[0];

swap q[3],q[2];
swap q[1],q[0];

// Gate: CZ**0.009295387491454189
u3(pi*0.5,pi*1.0,pi*1.0820521548) q[2];
u3(pi*0.5,pi*1.0,pi*1.5820521548) q[1];
rx(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*0.4953523063) q[2];
ry(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[2],q[1];
u3(pi*0.5,pi*1.9225955389,0) q[2];
u3(pi*0.5,pi*1.4225955389,0) q[1];

rz(pi*-0.0068270924) q[0];
rz(pi*-0.0031640201) q[3];
swap q[2],q[1];
z q[0];
z q[3];
rz(pi*-0.0068270924) q[1];
rz(pi*-0.0031640201) q[2];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

// Gate: PhasedISWAP**-0.5017530508495694
rz(pi*0.25) q[0];
rz(pi*-0.25) q[1];
cx q[0],q[1];
h q[0];
cx q[1],q[0];
rz(pi*-0.2508765254) q[0];
cx q[1],q[0];
rz(pi*0.2508765254) q[0];
h q[0];
cx q[0],q[1];
rz(pi*-0.25) q[0];
rz(pi*0.25) q[1];

// Gate: PhasedISWAP**0.5017530508495694
rz(pi*0.25) q[2];
rz(pi*-0.25) q[3];
cx q[2],q[3];
h q[2];
cx q[3],q[2];
rz(pi*0.2508765254) q[2];
cx q[3],q[2];
rz(pi*-0.2508765254) q[2];
h q[2];
cx q[2],q[3];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[3];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[1];
rz(pi*-0.25) q[2];
cx q[1],q[2];
h q[1];
cx q[2],q[1];
rz(pi*-0.5) q[1];
cx q[2],q[1];
rz(pi*0.5) q[1];
h q[1];
cx q[1],q[2];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[2];

// Gate: CZ**-0.00046375097365492423
u3(pi*0.5,0,pi*1.5001274262) q[0];
u3(pi*0.5,pi*1.0,pi*1.0001274262) q[1];
rx(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*0.4997681245) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[0],q[1];
u3(pi*0.5,pi*1.4996406983,pi*1.0) q[0];
u3(pi*0.5,pi*1.9996406983,0) q[1];

swap q[0],q[1];

// Gate: CZ**-0.0004129506013584246
u3(pi*0.5,pi*1.0,pi*1.4998373235) q[2];
u3(pi*0.5,0,pi*1.9998373235) q[3];
rx(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*0.4997935247) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*-0.5) q[3];
rz(pi*0.5) q[3];
cx q[2],q[3];
u3(pi*0.5,pi*1.4999562012,0) q[2];
u3(pi*0.5,pi*0.9999562012,pi*1.0) q[3];

swap q[2],q[3];

// Gate: CZ**0.00043761426330885954
u3(pi*0.5,0,pi*1.9993457511) q[1];
u3(pi*0.5,0,pi*1.4993457511) q[2];
rx(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*0.4997811929) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[1],q[2];
u3(pi*0.5,pi*1.0008730561,pi*1.0) q[1];
u3(pi*0.5,pi*1.5008730561,pi*1.0) q[2];

swap q[1],q[2];

// Gate: CZ**0.00043761426330885954
u3(pi*0.5,0,pi*1.9993457511) q[0];
u3(pi*0.5,0,pi*1.4993457511) q[1];
rx(pi*0.5) q[0];
cx q[0],q[1];
rx(pi*0.4997811929) q[0];
ry(pi*0.5) q[1];
cx q[1],q[0];
rx(pi*-0.5) q[1];
rz(pi*0.5) q[1];
cx q[0],q[1];
u3(pi*0.5,pi*1.0008730561,pi*1.0) q[0];
u3(pi*0.5,pi*1.5008730561,pi*1.0) q[1];

// Gate: CZ**0.00043761426330885954
u3(pi*0.5,0,pi*1.9993457511) q[2];
u3(pi*0.5,0,pi*1.4993457511) q[3];
rx(pi*0.5) q[2];
cx q[2],q[3];
rx(pi*0.4997811929) q[2];
ry(pi*0.5) q[3];
cx q[3],q[2];
rx(pi*-0.5) q[3];
rz(pi*0.5) q[3];
cx q[2],q[3];
u3(pi*0.5,pi*1.0008730561,pi*1.0) q[2];
u3(pi*0.5,pi*1.5008730561,pi*1.0) q[3];

swap q[0],q[1];
swap q[2],q[3];

// Gate: CZ**0.00043761426330885954
u3(pi*0.5,0,pi*1.9993457511) q[1];
u3(pi*0.5,0,pi*1.4993457511) q[2];
rx(pi*0.5) q[1];
cx q[1],q[2];
rx(pi*0.4997811929) q[1];
ry(pi*0.5) q[2];
cx q[2],q[1];
rx(pi*-0.5) q[2];
rz(pi*0.5) q[2];
cx q[1],q[2];
u3(pi*0.5,pi*1.0008730561,pi*1.0) q[1];
u3(pi*0.5,pi*1.5008730561,pi*1.0) q[2];

rz(pi*-0.0002318755) q[3];
rz(pi*-0.0002064753) q[0];
swap q[1],q[2];
z q[3];
z q[0];
rz(pi*-0.0002318755) q[2];
rz(pi*-0.0002064753) q[1];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[2];
rz(pi*-0.25) q[1];
cx q[2],q[1];
h q[2];
cx q[1],q[2];
rz(pi*-0.5) q[2];
cx q[1],q[2];
rz(pi*0.5) q[2];
h q[2];
cx q[2],q[1];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[1];

// Gate: PhasedISWAP**-0.4158482042253096
rz(pi*0.25) q[3];
rz(pi*-0.25) q[2];
cx q[3],q[2];
h q[3];
cx q[2],q[3];
rz(pi*-0.2079241021) q[3];
cx q[2],q[3];
rz(pi*0.2079241021) q[3];
h q[3];
cx q[3],q[2];
rz(pi*-0.25) q[3];
rz(pi*0.25) q[2];

// Gate: PhasedISWAP**0.4158482042253096
rz(pi*0.25) q[1];
rz(pi*-0.25) q[0];
cx q[1],q[0];
h q[1];
cx q[0],q[1];
rz(pi*0.2079241021) q[1];
cx q[0],q[1];
rz(pi*-0.2079241021) q[1];
h q[1];
cx q[1],q[0];
rz(pi*-0.25) q[1];
rz(pi*0.25) q[0];

// Gate: PhasedISWAP**-1.0
rz(pi*0.25) q[2];
rz(pi*-0.25) q[1];
cx q[2],q[1];
h q[2];
cx q[1],q[2];
rz(pi*-0.5) q[2];
cx q[1],q[2];
rz(pi*0.5) q[2];
h q[2];
cx q[2],q[1];
rz(pi*-0.25) q[2];
rz(pi*0.25) q[1];

swap q[3],q[2];
swap q[1],q[0];
swap q[2],q[1];
swap q[3],q[2];
swap q[1],q[0];
swap q[2],q[1];

measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];

