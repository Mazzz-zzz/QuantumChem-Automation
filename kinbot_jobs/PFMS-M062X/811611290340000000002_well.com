%mem=28GB
%chk=811611290340000000002_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 2
S                 1.7660830000        0.0669680000        0.0323260000
O                 2.2416970000       -0.4641580000        1.2503130000
O                 2.1856040000       -0.3869880000       -1.2448970000
O                 1.9126350000        1.6311480000        0.1017490000
H                 1.9599280000        2.0008750000       -0.7917130000


