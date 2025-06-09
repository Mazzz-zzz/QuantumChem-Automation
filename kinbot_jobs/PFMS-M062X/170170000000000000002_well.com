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
O                 1.9126350000        1.6311480000        0.1017490000
H                 1.9599280000        2.0008750000       -0.7917130000


