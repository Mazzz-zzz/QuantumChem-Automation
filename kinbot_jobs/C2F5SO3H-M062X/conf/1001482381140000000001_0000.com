%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
C                -1.6728970000       -1.2243940000        0.2119550000
C                -0.7502150000       -0.6681540000        1.3393600000
F                -1.3298790000        0.4035610000        1.7450830000
F                -0.9311020000       -1.7769220000       -0.7350990000
F                -2.4202030000       -2.1666320000        0.7899780000
F                -2.4771880000       -0.3283480000       -0.3490840000


