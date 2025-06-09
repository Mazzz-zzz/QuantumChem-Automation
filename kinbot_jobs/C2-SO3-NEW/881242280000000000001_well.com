%mem=28GB
%chk=881242280000000000001_well
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
C                -1.8560440000       -1.1829800000        0.4150000000
F                -1.6099970000        0.0681310000        0.0348630000
F                -1.1626760000       -2.0113230000       -0.3359370000
F                -1.5256500000       -1.3294700000        1.6788560000
F                -3.1474850000       -1.4246020000        0.2634940000


