%mem=28GB
%chk=1502984803620600000001_R_Addition_MultipleBond_5_1_2_IRC_R
%nprocshared=8
#P mp2/6-31G ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
guess(Read,Mix)
geom(AllCheck,NoKeepConstants)
irc(RCFC,reverse,MaxPoints=100,StepSize=2)

Gaussian input prepared by ASE

0 1
C                -1.0489250000       -0.1259960000        0.0680490000
F                -1.6472330000        1.0314210000       -0.3565120000
F                -1.3606330000       -0.3834010000        1.3853020000
F                -1.4026710000       -1.1845540000       -0.7400330000
S                 0.9639840000       -0.0130970000       -0.0145470000
O                 1.5520170000       -0.0438980000        1.4666320000
O                 1.4995430000       -1.0139570000       -1.1334730000
O                 0.9296930000        1.6898850000       -0.6489160000
H                 1.8651000000        1.9985010000       -0.7811070000


