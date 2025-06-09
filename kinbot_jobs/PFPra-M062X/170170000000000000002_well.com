%mem=28GB
%chk=170170000000000000002_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 2
O                 2.0106220000        1.2448180000       -0.0010820000
H                 2.9772360000        1.2080680000        0.0132040000


