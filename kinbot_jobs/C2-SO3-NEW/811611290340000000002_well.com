%mem=28GB
%chk=811611290340000000002_well
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 2
S                 1.8172620000        0.0408390000       -0.0466080000
O                 2.2825620000       -0.5130680000        1.1946610000
O                 2.2320110000       -0.4228430000       -1.3308770000
O                 2.0318490000        1.6270070000       -0.0367120000
H                 2.0669860000        1.9572730000        0.8708320000


