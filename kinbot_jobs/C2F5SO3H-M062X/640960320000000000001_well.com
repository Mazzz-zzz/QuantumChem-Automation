%mem=28GB
%chk=640960320000000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
S                 1.5931690000        1.0274420000       -1.2999490000
O                 2.1745670000        0.9470960000        0.0037060000
O                 1.4155560000        2.3196290000       -1.8707930000


