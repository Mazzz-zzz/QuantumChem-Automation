%mem=28GB
%chk=450730450170000000002_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 2
C                 1.5439120000       -0.0000040000        0.0004870000
O                 2.1988580000       -0.9911390000        0.0027060000
O                 1.9948200000        1.2499790000       -0.0019250000
H                 2.9616210000        1.2262450000       -0.0015980000


