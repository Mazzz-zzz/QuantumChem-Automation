%mem=28GB
%chk=440560320000000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                 2.5396780000       -0.7917380000       -0.6428540000
O                 2.5603500000       -1.9425950000       -0.6873740000
O                 2.5250570000        0.3645410000       -0.5952800000


