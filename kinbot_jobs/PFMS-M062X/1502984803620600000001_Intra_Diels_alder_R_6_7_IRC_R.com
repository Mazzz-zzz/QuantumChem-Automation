%mem=28GB
%chk=1502984803620600000001_Intra_Diels_alder_R_6_7_IRC_R
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
geom(AllCheck,NoKeepConstants)
guess(Read)
irc(RCFC,reverse,MaxPoints=100,StepSize=2)

Gaussian input prepared by ASE

0 1
C                -0.9575680000       -0.1374480000        0.0299300000
F                -1.5203650000        1.0176730000       -0.2876780000
F                -1.3568760000       -0.5019510000        1.2297710000
F                -1.3219670000       -1.0488830000       -0.8514050000
S                 0.9111280000        0.0156500000        0.0192020000
O                 1.3862870000       -0.8367930000       -1.0114160000
O                 1.3342430000       -0.0668810000        1.3634840000
O                 1.0896900000        1.5104260000       -0.4327170000
H                 1.1848280000        1.5617620000       -1.3943520000


