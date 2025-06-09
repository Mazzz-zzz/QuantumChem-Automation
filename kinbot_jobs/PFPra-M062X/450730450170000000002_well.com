%mem=28GB
%chk=450730450170000000002_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 2
C                 1.5441690000        0.0003320000        0.0002590000
O                 2.1887910000       -0.9973350000        0.0102840000
O                 2.0106220000        1.2448180000       -0.0010820000
H                 2.9772360000        1.2080680000        0.0132040000


