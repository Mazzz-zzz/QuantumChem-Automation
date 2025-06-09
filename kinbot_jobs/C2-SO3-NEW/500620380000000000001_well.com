%mem=28GB
%chk=500620380000000000001_well
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
C                -3.2185270000       -0.3145230000        0.4688780000
F                -3.6864400000        0.7831710000        0.9826710000
F                -4.1727440000       -1.1831030000        0.6190670000


