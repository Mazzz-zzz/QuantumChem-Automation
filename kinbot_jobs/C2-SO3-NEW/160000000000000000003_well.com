%mem=28GB
%chk=160000000000000000003_well
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 3
O                 2.2825620000       -0.5130680000        1.1946610000


