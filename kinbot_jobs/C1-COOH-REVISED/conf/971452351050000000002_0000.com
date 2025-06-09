%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 2
C                 1.5523190000       -0.0050500000        0.0000230000
O                 2.2148290000       -0.9593020000        0.0032630000
C                -0.0138290000       -0.0122940000       -0.0001600000
F                -0.4414050000        0.6252700000        1.0782930000
F                -0.4412270000        0.6202160000       -1.0816440000
F                -0.5075050000       -1.2407880000        0.0026610000


