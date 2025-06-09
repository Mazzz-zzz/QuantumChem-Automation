%mem=28GB
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 2
H                 2.0669860000        1.9572730000        0.8708320000


