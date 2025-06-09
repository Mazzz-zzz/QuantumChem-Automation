%mem=28GB
%chk=1002122340540000000001_well
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
S                 1.8614700000       -0.1542500000        0.3941010000
O                 3.2817680000       -0.0751480000        0.4659200000
O                 1.1148360000       -1.3595700000        0.3599910000
O                 1.3141540000        0.7613660000       -0.7802390000
F                 1.3103860000        0.6966250000        1.6256860000
H                 1.8817700000        1.5316620000       -0.9158980000


