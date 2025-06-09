%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                 1.5150964840        0.0000000000        0.0000000000
O                 2.1016263504       -1.0381441725        0.0944576251
C                 0.0000000000        0.0000000000        0.0000000000
F                -0.3697314281       -0.1222548406       -1.2345322660
O                 2.0503682021        1.2163887624        0.0000000000
H                 1.8297636081        1.6516211642       -0.8368254961


