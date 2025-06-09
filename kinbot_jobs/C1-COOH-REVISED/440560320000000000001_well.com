%mem=28GB
%chk=440560320000000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                 2.0617060000       -0.1162730000       -0.6674840000
O                 2.1137650000       -0.6978330000       -1.6606780000
O                 2.0153420000        0.4683700000        0.3300570000


