%mem=28GB
%chk=690931140000000000002_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 2
C                -0.0000340000       -0.0000270000       -0.0000470000
F                -0.4608700000        0.6308350000        1.0770050000
F                -0.4600690000        0.6255170000       -1.0805470000
F                -0.4586140000       -1.2371300000        0.0028310000


