%mem=28GB
%chk=1141903082400600000001_R_Addition_MultipleBond_1_3_4_IRC_F
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
C                 0.9954310000        0.0035150000        0.0683100000
O                 1.6482260000       -0.8483210000        0.6981100000
C                -0.5350790000       -0.0373830000       -0.0120040000
F                -1.0699230000        0.0223930000        1.2803120000
F                -1.0800520000        1.0020390000       -0.7558790000
F                -0.9378040000       -1.2470970000       -0.5902690000
O                 1.5164650000        1.0701850000       -0.6266110000
H                 2.5001100000        1.0795530000       -0.5641180000


