%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 2
O                 2.0087670000        1.2448890000       -0.0011090000
H                 2.9790910000        1.2079970000        0.0132310000


