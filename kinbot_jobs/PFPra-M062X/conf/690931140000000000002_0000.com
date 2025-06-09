%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 2
C                -0.6090880000        0.3982730000        1.4102830000
F                -1.9080670000        0.2320570000        1.3382940000
F                -0.0756400000       -0.4017670000        2.3023480000
F                -0.3024620000        1.6505710000        1.6509990000


