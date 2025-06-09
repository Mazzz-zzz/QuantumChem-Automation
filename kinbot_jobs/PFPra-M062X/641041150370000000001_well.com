%mem=28GB
%chk=641041150370000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                 1.7954280000        0.3269510000       -1.5865540000
O                 2.2518700000        0.7679360000       -2.5711390000
F                 0.4457390000        0.0904400000       -1.4879220000
O                 2.3931600000       -0.0104060000       -0.4760190000
H                 1.7411230000       -0.3480470000        0.1833700000


