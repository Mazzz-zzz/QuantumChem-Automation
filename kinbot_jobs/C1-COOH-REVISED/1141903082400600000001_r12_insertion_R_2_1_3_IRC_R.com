%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_2_1_3_IRC_R
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
C                 1.5633380000        0.4201670000        0.4265050000
O                 1.5399180000       -0.2026380000       -0.6808040000
C                -0.0717700000       -0.1247680000       -0.1059780000
F                -0.8076190000        0.8620870000        0.4143280000
F                -0.5963700000       -0.2697740000       -1.3260630000
F                -0.2411720000       -1.2363250000        0.5592090000
O                 2.6436760000        1.0809930000        0.7202370000
H                 3.2896230000        0.9745300000       -0.0085170000


