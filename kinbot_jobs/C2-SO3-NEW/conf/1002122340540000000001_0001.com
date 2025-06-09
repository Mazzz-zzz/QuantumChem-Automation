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
S                 1.5968325767        0.0000000000        0.0000000000
O                 1.9862088193       -0.5531393692        1.2547887396
O                 2.0091035727       -0.4882422494       -1.2646639005
O                 1.8272828265        1.5690528348        0.0000000000
F                 0.0000000000        0.0000000000        0.0000000000
H                 1.1825983727        2.0080182129       -0.5702427745


