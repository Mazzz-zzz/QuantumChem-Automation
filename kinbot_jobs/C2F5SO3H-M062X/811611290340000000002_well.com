%mem=28GB
%chk=811611290340000000002_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 2
S                 1.9090330000       -0.0307800000        0.2538730000
O                 2.2230140000       -0.2300260000        1.6149520000
O                 2.3744440000       -0.8667950000       -0.7941720000
O                 2.2355870000        1.4678850000       -0.0891010000
H                 2.3458860000        1.5775250000       -1.0447960000


