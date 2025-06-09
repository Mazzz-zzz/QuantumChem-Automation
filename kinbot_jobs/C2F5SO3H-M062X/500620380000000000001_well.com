%mem=28GB
%chk=500620380000000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
C                -2.9628710000       -0.8739710000        0.7388610000
F                -4.0746070000       -1.2342190000        1.2897840000
F                -2.9588800000       -1.4682810000       -0.4096650000


