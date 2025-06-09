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
C                 2.5416960000       -0.7899310000       -0.6418360000
O                 2.5593410000       -1.9434600000       -0.6878810000
O                 2.5240480000        0.3635990000       -0.5957910000


