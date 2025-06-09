%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 2.0126220000        0.2226000000       -0.3074040000
O                 2.1700770000       -0.2944400000       -1.3154540000
C                -0.0758350000        0.2160160000        0.1429070000
F                -0.8067990000        0.6878600000        1.1831160000
F                -0.5649110000        0.7975080000       -0.9594840000
F                -0.3415950000       -1.0933830000        0.0549660000
O                 2.3822910000        0.8130180000        0.7224230000
H                 1.2194400000        0.7437000000        0.8485280000


