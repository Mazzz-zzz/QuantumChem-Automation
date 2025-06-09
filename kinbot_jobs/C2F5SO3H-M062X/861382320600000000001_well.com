%mem=28GB
%chk=861382320600000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
C                -1.9914880000        0.1682680000       -0.3038480000
O                -0.9765280000        0.9598130000        0.0947950000
F                -2.1265500000       -0.9029960000        0.4787340000
F                -3.1603410000        0.8080120000       -0.2919880000
F                -1.7440040000       -0.2288190000       -1.5381550000
H                -1.0261240000        1.1127120000        1.0454940000


