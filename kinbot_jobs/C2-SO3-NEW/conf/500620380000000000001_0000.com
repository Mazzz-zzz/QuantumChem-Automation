%mem=28GB
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
C                -3.2169630000       -0.3147270000        0.4681610000
F                -3.6872680000        0.7830170000        0.9829750000
F                -4.1734800000       -1.1827450000        0.6194800000


