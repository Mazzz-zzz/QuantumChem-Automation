%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
F                -2.1217050000       -0.4459970000        0.0657420000
H                -1.8886450000        0.3763430000        0.4019780000


