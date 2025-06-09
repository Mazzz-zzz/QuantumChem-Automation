%mem=28GB
%chk=1141903082400600000001_R_Addition_MultipleBond_1_7_8_IRC_R_prod
%nprocshared=8
#P mp2/6-31G ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
guess(Mix,Always)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                 0.9859400000        0.0679520000       -0.0031330000
O                 1.7507380000       -0.8307390000       -0.3955760000
C                -0.5522870000       -0.0770940000        0.0098320000
F                -1.1770300000        0.6760190000        1.0012730000
F                -1.0839710000        0.3084030000       -1.2299770000
F                -0.8812650000       -1.4196970000        0.2143870000
O                 1.4999100000        1.2776010000        0.3893960000
H                 2.4809500000        1.2221840000        0.2882130000


