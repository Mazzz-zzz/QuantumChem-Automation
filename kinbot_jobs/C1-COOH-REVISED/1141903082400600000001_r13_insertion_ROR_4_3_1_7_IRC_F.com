%mem=28GB
%chk=1141903082400600000001_r13_insertion_ROR_4_3_1_7_IRC_F
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
geom(AllCheck,NoKeepConstants)
guess(Read)
irc(RCFC,forward,MaxPoints=100,StepSize=2)

Gaussian input prepared by ASE

0 1
C                 3.9781830000        1.2508860000       -0.3869890000
O                 4.9007320000        1.8641330000       -0.5464290000
C                 0.9704560000        0.5509530000        0.1778660000
F                -0.7308960000        0.4456220000        0.5084330000
F                 1.0796260000       -0.0862800000       -0.9423250000
F                 1.4875430000       -0.1448840000        1.1377110000
O                 0.9017180000        1.8011000000        0.2265290000
H                -0.2658530000        1.5450290000        0.4480080000


