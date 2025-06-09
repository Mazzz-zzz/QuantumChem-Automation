%mem=28GB
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 2
C                -0.7265900000        0.2976010000        1.3741250000
F                -0.4819040000       -0.6966050000        2.2016720000
F                -0.1896620000        1.4203760000        1.8032290000
F                -2.0183800000        0.4358490000        1.1612080000


