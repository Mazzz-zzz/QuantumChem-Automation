%mem=28GB
%chk=280280000000000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                 2.4977400000       -2.0691300000       -2.3156720000
O                 2.5826650000       -1.2739840000       -1.5281770000


