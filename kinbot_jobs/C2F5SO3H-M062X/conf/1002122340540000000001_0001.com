%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
F                 0.0000000000        0.0000000000        0.0000000000
S                 1.5484959054        0.0000000000        0.0000000000
O                 1.9443350942       -0.5467091484        1.2391650149
O                 1.9556583821       -0.4990734479       -1.2468294213
O                 1.7874080178        1.5420162116        0.0000000000
H                 1.0778181542        1.9898326416       -0.4817409998


