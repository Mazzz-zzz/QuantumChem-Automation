%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 2
S                 1.8755440000       -0.0391110000        0.2547750000
O                 2.2328480000       -0.2296460000        1.6279050000
O                 2.3878590000       -0.8665160000       -0.8060610000
O                 2.2477330000        1.4823760000       -0.0884290000
H                 2.3439810000        1.5707060000       -1.0474340000


