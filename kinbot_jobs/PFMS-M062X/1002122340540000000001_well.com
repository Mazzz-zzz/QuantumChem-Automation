%mem=28GB
%chk=1002122340540000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
F                -0.0792850000        1.1568740000       -1.4650530000
S                 0.8553250000        0.6702880000       -0.3362960000
O                 0.1148350000        0.7166530000        0.8588140000
O                 1.5031630000       -0.4873210000       -0.8146770000
O                 1.8525620000        1.8699010000       -0.3168680000
H                 2.5730610000        1.7150670000       -0.9439820000


