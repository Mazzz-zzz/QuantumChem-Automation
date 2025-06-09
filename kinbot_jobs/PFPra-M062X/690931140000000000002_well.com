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
C                -0.5940310000        0.3880930000        1.3716140000
F                -1.9085450000        0.2379010000        1.3521390000
F                -0.0821090000       -0.3958250000        2.3142050000
F                -0.3105720000        1.6489650000        1.6639670000


