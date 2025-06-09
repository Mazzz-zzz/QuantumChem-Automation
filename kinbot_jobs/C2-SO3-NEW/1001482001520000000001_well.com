%mem=28GB
%chk=1001482001520000000001_well
%nprocshared=8
#P wb97xd/6-311++G(d,p) ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
C                -1.9291680000       -0.4695680000       -0.0096040000
C                -1.6966760000        0.6501580000       -0.6664400000
F                -1.6023240000        0.7192050000       -1.9746930000
F                -1.5298940000        1.8143450000       -0.0766890000
F                -2.0218260000       -0.5304360000        1.2980010000
F                -2.0966090000       -1.6290190000       -0.5975770000


