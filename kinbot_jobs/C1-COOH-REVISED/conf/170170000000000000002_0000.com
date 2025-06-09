%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 2
O                 1.9928050000        1.2500280000       -0.0019260000
H                 2.9636360000        1.2261960000       -0.0015970000


