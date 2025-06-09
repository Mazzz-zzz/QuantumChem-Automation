%mem=28GB
%chk=1002122340540000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
F                 0.2914530000        0.8500320000       -0.6841470000
S                 1.8209720000        0.8914990000       -0.3599080000
O                 1.9298930000        1.5386580000        0.8881880000
O                 2.3262680000       -0.3838580000       -0.6463980000
O                 2.2664810000        1.8546790000       -1.5010070000
H                 2.1943180000        2.7753950000       -1.2113960000


