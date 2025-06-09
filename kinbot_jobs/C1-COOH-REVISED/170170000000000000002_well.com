%mem=28GB
%chk=170170000000000000002_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 2
O                 1.9948200000        1.2499790000       -0.0019250000
H                 2.9616210000        1.2262450000       -0.0015980000


