%mem=28GB
%chk=1001482381140000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
C                -1.6594860000       -1.2149950000        0.1985290000
C                -0.7200860000       -0.6321450000        1.2968290000
F                -1.3790900000        0.3499830000        1.8006730000
F                -0.9493650000       -1.8141760000       -0.7412910000
F                -2.4121550000       -2.1258570000        0.8234140000
F                -2.4613020000       -0.3237000000       -0.3759610000


