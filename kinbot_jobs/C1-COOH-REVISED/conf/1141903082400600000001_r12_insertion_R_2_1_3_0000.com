%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.8039042300        0.0000000000        0.0000000000
O                 1.2676752695       -0.2807566003       -1.1172296179
C                 0.0000000000        0.0000000000        0.0000000000
F                -0.2152922816        0.9500150235        0.9149839147
F                -0.8794652155        0.3097030374       -0.9567989708
F                -0.2929845726       -1.1817443321        0.4736772326
O                 3.0694835116        0.2973361172        0.0000000000
H                 3.1829027252        1.2050233413        0.3505770597


