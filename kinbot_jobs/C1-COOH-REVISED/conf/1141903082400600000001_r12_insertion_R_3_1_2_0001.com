%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.8037291816        0.0000000000        0.0000000000
O                 1.2675189084       -0.2794799638       -1.1175983701
C                 0.0000000000        0.0000000000        0.0000000000
F                -0.2149479270        0.9495816962        0.9155102860
F                -0.8798418169        0.3102964343       -0.9563956927
F                -0.2930945658       -1.1820177801        0.4729169859
O                 3.0688139030        0.2993897085        0.0000000000
H                 3.5473029525       -0.3411663586        0.5660348747


