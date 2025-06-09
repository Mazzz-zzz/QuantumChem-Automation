%mem=28GB
%chk=160000000000000000003_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 3
O                 2.2416970000       -0.4641580000        1.2503130000


