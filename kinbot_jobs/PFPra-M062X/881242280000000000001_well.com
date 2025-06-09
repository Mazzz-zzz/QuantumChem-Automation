%mem=28GB
%chk=881242280000000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                -1.4558910000        0.7031290000        0.9196230000
F                -2.3433340000        1.6513260000        1.1402920000
F                -1.8614460000       -0.4156910000        1.4738760000
F                -0.2980510000        1.0611010000        1.4305460000
F                -1.3263090000        0.5291360000       -0.3835890000


