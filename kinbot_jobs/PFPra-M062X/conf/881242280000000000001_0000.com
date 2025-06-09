%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                -1.4570260000        0.7057980000        0.9161270000
F                -2.3442020000        1.6518240000        1.1415510000
F                -1.8603840000       -0.4161140000        1.4740070000
F                -0.2981280000        1.0595540000        1.4304760000
F                -1.3252910000        0.5279400000       -0.3814130000


