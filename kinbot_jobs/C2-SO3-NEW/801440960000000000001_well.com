%mem=28GB
%chk=801440960000000000001_well
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
S                 2.5065530000       -0.2298160000       -0.5322280000
O                 2.6909920000       -1.0699920000        0.6107520000
O                 2.8162510000       -0.7078380000       -1.8447540000
O                 2.0387860000        1.1169840000       -0.3579830000


