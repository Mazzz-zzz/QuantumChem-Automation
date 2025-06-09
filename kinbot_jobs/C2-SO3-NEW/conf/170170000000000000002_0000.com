%mem=28GB
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 2
O                 2.0317690000        1.6262560000       -0.0387760000
H                 2.0670660000        1.9580240000        0.8728960000


