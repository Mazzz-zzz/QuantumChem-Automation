%mem=28GB
%chk=690931140000000000002_well
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 2
C                -0.7090150000        0.2805810000        1.3362340000
F                -0.4922090000       -0.6857650000        2.2093390000
F                -0.1992970000        1.4231890000        1.8163880000
F                -2.0160150000        0.4392160000        1.1782730000


