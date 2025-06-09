%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
F                -2.6173910000       -0.7953940000        0.5976840000
H                -2.7823230000        0.1049740000        0.6734650000


