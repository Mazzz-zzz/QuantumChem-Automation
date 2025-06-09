%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.7672238692        0.0000000000        0.0000000000
O                 2.2495379533       -0.8903255273       -0.6070033651
C                 0.0000000000        0.0000000000        0.0000000000
F                 1.3523371732       -0.2685624040        1.4770411261
F                -0.7595081928        0.9018362678        0.4823071865
F                -0.6265167295       -1.0927963835       -0.0917814143
O                 2.1742583202        1.2808846263        0.0000000000
H                 1.9419136042        1.6974714415        0.8364925079


