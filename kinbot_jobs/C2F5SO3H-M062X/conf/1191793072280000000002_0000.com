%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 2
C                -0.6428520000       -1.3252510000        0.1888710000
C                -0.0036420000        0.0436380000        0.0739560000
F                -0.2275910000        0.6372780000       -1.0743620000
F                -0.2517400000        0.8308200000        1.0936960000
F                -0.2565410000       -2.0879560000       -0.8239990000
F                -0.2830450000       -1.8948570000        1.3303510000
F                -1.9746120000       -1.2418880000        0.1649260000


