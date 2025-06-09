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
S                 1.7350560000        0.0560350000        0.0302590000
O                 2.2440830000       -0.4655670000        1.2625430000
O                 2.2029670000       -0.3886240000       -1.2565260000
O                 1.9458060000        1.6439160000        0.1053190000
H                 1.9380360000        2.0020850000       -0.7938180000


