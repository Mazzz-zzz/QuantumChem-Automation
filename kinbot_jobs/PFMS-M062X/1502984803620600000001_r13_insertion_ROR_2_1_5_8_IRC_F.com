%mem=28GB
%chk=1502984803620600000001_r13_insertion_ROR_2_1_5_8_IRC_F
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
C                 1.5896580000        0.0835650000       -0.0815930000
F                -0.4759850000        0.5604460000        0.0867740000
F                 1.6183280000       -0.6747390000        0.9210000000
F                 1.5197040000       -0.5510010000       -1.1615360000
S                 2.0869600000        1.9620060000        0.0252580000
O                 3.3154240000        1.7969930000        0.7220970000
O                 2.0978100000        2.2907360000       -1.3547940000
O                 0.9597810000        2.4291460000        0.8017380000
H                -0.2313340000        1.4305410000        0.4186340000


