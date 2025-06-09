%mem=28GB
%chk=1502984803620600000001_R_Addition_MultipleBond_5_1_2_IRC_F
%nprocshared=8
#P mp2/6-31G ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
guess(Read,Mix)
geom(AllCheck,NoKeepConstants)
irc(RCFC,forward,MaxPoints=100,StepSize=2)

Gaussian input prepared by ASE

0 1
C                -1.0489260000       -0.1259440000        0.0682080000
F                -1.6470980000        1.0336240000       -0.3506640000
F                -1.3602730000       -0.3892730000        1.3844240000
F                -1.4031860000       -1.1807050000       -0.7445440000
S                 0.9639820000       -0.0129740000       -0.0140940000
O                 1.5512510000       -0.0388120000        1.4674400000
O                 1.5003740000       -1.0173600000       -1.1295180000
O                 0.9296080000        1.6876430000       -0.6547580000
H                 1.8649220000        1.9941150000       -0.7925540000


