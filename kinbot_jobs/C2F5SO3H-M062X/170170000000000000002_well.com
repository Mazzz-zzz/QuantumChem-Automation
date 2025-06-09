%mem=28GB
%chk=170170000000000000002_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 2
O                 2.2355870000        1.4678850000       -0.0891010000
H                 2.3458860000        1.5775250000       -1.0447960000


