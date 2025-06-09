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
C                -0.0471580000        0.0048310000       -0.0000790000
F                -0.4446250000        0.6324460000        1.0808970000
F                -0.4438200000        0.6271070000       -1.0844320000
F                -0.4439840000       -1.2451890000        0.0028560000


