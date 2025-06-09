%mem=28GB
%chk=500620380000000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                -0.7909930000       -0.6831270000       -1.7464860000
F                -1.8106500000       -0.4260290000       -2.4955700000
F                -0.6829260000       -1.9667370000       -1.7571210000


