%mem=28GB
%chk=690931140000000000002_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 2
C                -0.6177770000       -1.3316220000        0.1958830000
F                -0.3014490000       -2.0794050000       -0.8461600000
F                -0.2532640000       -1.9488880000        1.3079480000
F                -1.9303380000       -1.1481140000        0.2116720000


