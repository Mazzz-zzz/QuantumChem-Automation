%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_3_1_7_IRC_R
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
C                 1.5511930000       -0.4638500000        0.0484730000
O                 2.6738710000       -0.8520470000        0.0993670000
C                -0.0241530000        0.0808780000       -0.0227170000
F                -0.2856310000        0.8124910000        1.0239700000
F                -0.2230990000        0.7118220000       -1.1457710000
F                -0.8747890000       -0.9555330000        0.0008460000
O                 1.7729110000        1.0318710000       -0.0172990000
H                 2.7293170000        1.1386440000        0.0120430000


