%mem=28GB
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
C                -1.9302630000       -0.4674180000       -0.0095250000
C                -1.6952360000        0.6523130000       -0.6661430000
F                -1.6032900000        0.7173050000       -1.9742700000
F                -1.5296920000        1.8141400000       -0.0774270000
F                -2.0222090000       -0.5324100000        1.2986030000
F                -2.0958070000       -1.6292450000       -0.5982400000


