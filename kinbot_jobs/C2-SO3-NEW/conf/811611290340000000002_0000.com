%mem=28GB
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 2
S                 1.7869750000        0.0278700000       -0.0454760000
O                 2.2999240000       -0.5180230000        1.2056960000
O                 2.2335820000       -0.4288780000       -1.3466260000
O                 2.0654420000        1.6440340000       -0.0368910000
H                 2.0447470000        1.9642040000        0.8745920000


