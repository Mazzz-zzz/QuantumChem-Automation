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
C                -1.8603790000       -1.1760590000        0.4112540000
F                -1.6078680000        0.0649820000        0.0366100000
F                -1.1611090000       -2.0120090000       -0.3347180000
F                -1.5238180000       -1.3303030000        1.6790070000
F                -3.1486780000       -1.4268560000        0.2641240000


