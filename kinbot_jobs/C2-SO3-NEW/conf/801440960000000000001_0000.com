%mem=28GB
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
S                 2.5131400000       -0.2226980000       -0.5310550000
O                 2.6893010000       -1.0732420000        0.6083630000
O                 2.8144460000       -0.7118090000       -1.8435870000
O                 2.0356960000        1.1170860000       -0.3579340000


