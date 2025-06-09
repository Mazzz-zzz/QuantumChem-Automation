%mem=28GB
%chk=1502984803620600000001_intra_H_migration_suprafacial_6_9
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.6808200000       -0.3627040000       -1.6975170000
F                 2.0687180000        0.6016840000       -2.4773130000
F                 0.3711870000       -0.4323320000       -1.6684390000
F                 2.1210590000       -1.4416750000       -2.1259990000
S                 1.5135890000        0.3895250000        0.3175310000
O                 2.1762710000       -0.2349790000       -0.4119570000
O                 1.4635510000       -0.3533940000        1.7517770000
O                 0.8883760000        1.4061450000        0.1156420000
H                 1.7764920000        0.8922730000       -0.5058340000



