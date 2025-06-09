%mem=28GB
%chk=690931140000000000002_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 2
C                -0.0693110000       -0.0602780000        0.0630210000
F                -0.5709420000        0.6185880000       -0.9599630000
F                -0.5441840000        0.4363460000        1.1885950000
F                -0.4109960000       -1.3296670000       -0.0425550000


