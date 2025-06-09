%mem=28GB
%chk=1001482381140000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                -0.0635960000       -0.7284020000        0.7803260000
C                -1.0797740000        0.4275110000        0.9726030000
F                -2.1327540000        0.3535230000        0.1758650000
F                -1.4841300000        0.3321290000        2.2421610000
F                -0.4795990000        1.5914310000        0.7989180000
F                -0.7554030000       -1.7727140000        0.5335290000


