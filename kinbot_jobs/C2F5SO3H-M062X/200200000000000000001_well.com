%mem=28GB
%chk=200200000000000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
F                -2.6171180000       -0.7968860000        0.5975580000
H                -2.7825960000        0.1064660000        0.6735910000


