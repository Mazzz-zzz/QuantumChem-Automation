%mem=28GB
%chk=200200000000000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
F                -2.1257780000       -0.4603670000        0.0598670000
H                -1.8845720000        0.3907130000        0.4078530000


