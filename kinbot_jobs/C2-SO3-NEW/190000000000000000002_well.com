%mem=28GB
%chk=190000000000000000002_well
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 2
F                -0.4922090000       -0.6857650000        2.2093390000


