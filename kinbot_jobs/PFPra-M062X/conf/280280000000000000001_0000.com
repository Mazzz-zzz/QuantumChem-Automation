%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                 2.4978230000       -2.0683570000       -2.3149070000
O                 2.5825820000       -1.2747570000       -1.5289420000


