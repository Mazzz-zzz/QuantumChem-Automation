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
C                -1.2690030000        0.1154760000       -0.8547470000
F                -2.3867220000       -0.1693740000       -0.2765080000
F                -1.1420390000       -0.7664780000       -1.7885030000


