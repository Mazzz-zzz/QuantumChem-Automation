%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
F                 0.0000000000        0.0000000000        0.0000000000
S                 1.5483622595        0.0000000000        0.0000000000
O                 1.9555551081       -0.4994987249        1.2466496867
O                 1.9443620187       -0.5462283483       -1.2392889176
O                 1.7871292289        1.5419734814        0.0000000000
H                 1.0751403108        1.9897022432        0.4782937640


