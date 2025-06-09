%mem=28GB
%chk=500620380000000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                -1.7198390000       -1.3664230000        0.1236600000
F                -1.1441890000       -2.2369300000        0.8866680000
F                -2.6965710000       -0.9032810000        0.8334160000


