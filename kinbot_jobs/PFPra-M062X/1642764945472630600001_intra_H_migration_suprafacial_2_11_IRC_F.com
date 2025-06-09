%mem=28GB
%chk=1642764945472630600001_intra_H_migration_suprafacial_2_11_IRC_F
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
C                 1.3576490000        0.2140680000       -1.1384670000
O                 0.3994020000        0.1386410000       -1.9434190000
C                 1.5224370000       -0.6962530000        0.0752600000
C                 2.5192690000       -1.8439150000       -0.2083640000
F                 2.5795710000       -2.6468680000        0.8396160000
F                 2.1106140000       -2.5342710000       -1.2652720000
F                 3.7238640000       -1.3535970000       -0.4521750000
F                 1.9821790000        0.0148310000        1.1094180000
F                 0.3462370000       -1.2367580000        0.3987520000
O                 2.1826670000        1.1076290000       -1.4476990000
H                 1.2138840000        1.0849440000       -2.3214570000


