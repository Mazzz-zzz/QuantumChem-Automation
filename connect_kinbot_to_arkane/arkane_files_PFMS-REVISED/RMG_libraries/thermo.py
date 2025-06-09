#!/usr/bin/env python
# encoding: utf-8

name = "thermo"
shortDesc = ""
longDesc = """
Calculated using Arkane v3.1.0 using LevelOfTheory(method='b97d3',basis='def2msvp',software='gaussian').
"""
entry(
    index = 0,
    label = "10000000000000000002",
    molecule = 
"""
multiplicity 2
1 H u1 p0 c0
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[2.5,-2.81405e-15,9.04759e-18,-8.59194e-21,2.41827e-24,25832.4,-0.461279], Tmin=(10,'K'), Tmax=(1853.57,'K')),
            NASAPolynomial(coeffs=[2.5,-1.31298e-12,9.14088e-16,-2.78281e-19,3.12633e-23,25832.4,-0.461279], Tmin=(1853.57,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (214.783,'kJ/mol'),
        Cp0 = (20.7862,'J/(mol*K)'),
        CpInf = (20.7862,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
H       1.95992800    2.00087500   -0.79171300
""",
)

entry(
    index = 1,
    label = "1002122340540000000001",
    molecule = 
"""
1 S u0 p0 c0 {2,S} {3,S} {4,D} {5,D}
2 F u0 p3 c0 {1,S}
3 O u0 p2 c0 {1,S} {6,S}
4 O u0 p2 c0 {1,D}
5 O u0 p2 c0 {1,D}
6 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.9121,0.00516782,7.4805e-05,-1.59381e-07,9.72793e-11,-8.95463e+07,10.1817], Tmin=(10,'K'), Tmax=(575.534,'K')),
            NASAPolynomial(coeffs=[4.822,0.0190888,-1.42406e-05,4.8832e-09,-6.22161e-13,-8.95467e+07,3.38173], Tmin=(575.534,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-744530,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (133.032,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
F      -0.07962900    1.15502800   -1.46550000
S       0.85640300    0.67124300   -0.33094200
O       0.11201600    0.71580200    0.85789900
O       1.50317900   -0.48478300   -0.81705200
O       1.85443300    1.87059100   -0.31707200
H       2.57326000    1.71358100   -0.94539500
""",
)

entry(
    index = 2,
    label = "1302784824321400000001",
    molecule = 
"""
multiplicity 3
1 S u0 p0 c0 {4,S} {5,S} {6,D} {7,D}
2 F u0 p3 c0 {7,S}
3 F u0 p3 c0 {7,S}
4 O u1 p2 c0 {1,S}
5 O u1 p2 c0 {1,S}
6 O u0 p2 c0 {1,D}
7 C u0 p0 c0 {1,D} {2,S} {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.84189,0.0103442,0.000115209,-2.94703e-07,2.11917e-10,-8.9541e+07,11.281], Tmin=(10,'K'), Tmax=(495.743,'K')),
            NASAPolynomial(coeffs=[5.6958,0.0250426,-1.90003e-05,6.45306e-09,-8.0884e-13,-8.95415e+07,-0.0378016], Tmin=(495.743,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-744486,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (157.975,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C       0.32897800   -0.83153500    0.00987700
F      -0.17111000   -1.53740000    0.99072900
F       0.52510000   -1.58143700   -1.04351900
S       0.16579300    0.89259600   -0.08320100
O       1.43164300   -0.01646300    0.36967600
O       0.36034100    1.50475000   -1.34383800
O      -0.44421800    1.55633600    1.00725800
""",
)

entry(
    index = 3,
    label = "1312673532570400000002",
    molecule = 
"""
multiplicity 2
1 S u0 p0 c0 {4,S} {5,S} {6,D} {7,D}
2 F u0 p3 c0 {7,S}
3 F u0 p3 c0 {7,S}
4 O u0 p2 c0 {1,S} {8,S}
5 O u1 p2 c0 {1,S}
6 O u0 p2 c0 {1,D}
7 C u0 p0 c0 {1,D} {2,S} {3,S}
8 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.70827,0.0229394,9.62456e-05,-3.22682e-07,2.72249e-10,-8.95409e+07,13.4816], Tmin=(10,'K'), Tmax=(442.97,'K')),
            NASAPolynomial(coeffs=[6.61752,0.0269743,-2.00387e-05,6.76877e-09,-8.48038e-13,-8.95415e+07,-1.54107], Tmin=(442.97,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-744486,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (182.918,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
C      -0.01643200   -0.07198200    0.11857500
F      -0.56448100    0.41760100    1.20173800
F      -0.46486000   -1.26837700   -0.16140100
S       1.77534600    0.05965500    0.05978200
O       2.32126400   -0.42314100    1.27300900
O       2.16665000   -0.42220100   -1.21667600
O       1.91497700    1.62623700    0.09188700
H       1.90899200    1.97645500   -0.81007400
""",
)

entry(
    index = 4,
    label = "1332333552100000000002",
    molecule = 
"""
multiplicity 2
1 S u1 p0 c0 {5,D} {6,D} {7,S}
2 F u0 p3 c0 {7,S}
3 F u0 p3 c0 {7,S}
4 F u0 p3 c0 {7,S}
5 O u0 p2 c0 {1,D}
6 O u0 p2 c0 {1,D}
7 C u0 p0 c0 {1,S} {2,S} {3,S} {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.64857,0.0298419,1.52253e-05,-1.0316e-07,8.35956e-11,-9.11121e+07,12.8366], Tmin=(10,'K'), Tmax=(525.411,'K')),
            NASAPolynomial(coeffs=[7.15466,0.0220465,-1.6468e-05,5.50648e-09,-6.80727e-13,-9.11127e+07,-4.30399], Tmin=(525.411,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-757549,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (157.975,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.09481800   -0.05912200    0.05993400
F      -0.58332900    0.58958800   -0.97420700
F      -0.54869400    0.46102800    1.17915100
F      -0.41475900   -1.33251500   -0.01083100
S       1.80501300    0.10822300    0.03922000
O       2.23779000   -0.52495300    1.25793400
O       2.19674800   -0.36143700   -1.26436100
""",
)

entry(
    index = 5,
    label = "1342503882400600000001",
    molecule = 
"""
1 S u0 p1 c0 {5,S} {6,D} {7,S}
2 F u0 p3 c0 {7,S}
3 F u0 p3 c0 {7,S}
4 F u0 p3 c0 {7,S}
5 O u0 p2 c0 {1,S} {8,S}
6 O u0 p2 c0 {1,D}
7 C u0 p0 c0 {1,S} {2,S} {3,S} {4,S}
8 H u0 p0 c0 {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.74176,0.0187964,0.000133007,-4.15473e-07,3.47362e-10,-9.11293e+07,12.7211], Tmin=(10,'K'), Tmax=(439.324,'K')),
            NASAPolynomial(coeffs=[6.83525,0.0272008,-2.0552e-05,7.02751e-09,-8.88096e-13,-9.11299e+07,-3.67535], Tmin=(439.324,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-757692,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (182.918,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
C      -0.01107200   -0.01969700    0.04926000
F      -0.45741300    0.72125500   -0.96053700
F      -0.50146300    0.46058700    1.18348600
F      -0.42617000   -1.26404500   -0.11208800
S       1.86098900    0.00929500    0.08731700
O       2.21980300   -0.50934100   -1.21881400
O       1.94879200    1.61411100    0.07583700
H       1.59535200    1.96482600   -0.75789800
""",
)

entry(
    index = 6,
    label = "1492814473150000000002",
    molecule = 
"""
multiplicity 2
1 S u0 p0 c0 {5,S} {6,D} {7,D} {8,S}
2 F u0 p3 c0 {8,S}
3 F u0 p3 c0 {8,S}
4 F u0 p3 c0 {8,S}
5 O u1 p2 c0 {1,S}
6 O u0 p2 c0 {1,D}
7 O u0 p2 c0 {1,D}
8 C u0 p0 c0 {1,S} {2,S} {3,S} {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.45518,0.0482104,-5.12575e-05,1.91348e-08,1.28431e-12,-8.95638e+07,13.7249], Tmin=(10,'K'), Tmax=(714.806,'K')),
            NASAPolynomial(coeffs=[10.2007,0.0205668,-1.44505e-05,4.58105e-09,-5.41638e-13,-8.9565e+07,-18.3591], Tmin=(714.806,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-744676,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (182.918,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.08369300   -0.06016100    0.05784200
F      -0.59401000    0.58008000   -0.97640000
F      -0.55506200    0.45686400    1.17610700
F      -0.39889000   -1.33957900   -0.00963300
S       1.74957300    0.09655800    0.03316400
O       2.23158300   -0.48052800    1.23975500
O       2.18491100   -0.33419300   -1.24982500
O       1.97617300    1.59291800    0.11757900
""",
)

entry(
    index = 7,
    label = "1502984803620600000001",
    molecule = 
"""
1 S u0 p0 c0 {2,S} {3,S} {4,D} {5,D}
2 C u0 p0 c0 {1,S} {6,S} {7,S} {8,S}
3 O u0 p2 c0 {1,S} {9,S}
4 O u0 p2 c0 {1,D}
5 O u0 p2 c0 {1,D}
6 F u0 p3 c0 {2,S}
7 F u0 p3 c0 {2,S}
8 F u0 p3 c0 {2,S}
9 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.69197,0.0231437,0.000138023,-4.34095e-07,3.60551e-10,-8.95945e+07,13.2617], Tmin=(10,'K'), Tmax=(442.874,'K')),
            NASAPolynomial(coeffs=[7.00451,0.0321129,-2.40665e-05,8.17008e-09,-1.02677e-12,-8.95952e+07,-4.32703], Tmin=(442.874,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-744931,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (207.862,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
C      -1.06803200   -0.07509000   -0.04723800
F      -1.44866500    0.33825000   -1.24035100
F      -1.33102600    0.86882400    0.84632800
F      -1.72068200   -1.17585300    0.27173100
S       0.73723700   -0.43076300   -0.04052200
O       1.08324900   -0.76390500    1.29450000
O       1.00270200   -1.25991100   -1.15146600
O       1.28027700    1.00680600   -0.37514800
H       1.46494100    1.49164000    0.44216400
""",
)

entry(
    index = 8,
    label = "1503305764823040000001",
    molecule = 
"""
1 S u0 p1 c0 {2,S} {3,S} {4,S} {5,S}
2 C u0 p0 c0 {1,S} {6,S} {7,S} {8,S}
3 O u0 p2 c0 {1,S} {4,S}
4 O u0 p2 c0 {1,S} {3,S}
5 O u0 p2 c0 {1,S} {9,S}
6 F u0 p3 c0 {2,S}
7 F u0 p3 c0 {2,S}
8 F u0 p3 c0 {2,S}
9 H u0 p0 c0 {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.66163,0.0248914,0.000159002,-5.19288e-07,4.4432e-10,-8.95442e+07,13.3098], Tmin=(10,'K'), Tmax=(434.738,'K')),
            NASAPolynomial(coeffs=[8.03803,0.0312854,-2.40568e-05,8.31769e-09,-1.05891e-12,-8.9545e+07,-9.22959], Tmin=(434.738,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-744512,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (207.862,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
C      -1.03974900   -0.09368600    0.16148100
F      -1.89108300    0.50234500   -0.66892200
F      -1.12917300    0.47278800    1.35210000
F      -1.38572600   -1.37601900    0.26978700
S       0.69456600   -0.05488500   -0.59564800
O       1.38447600   -0.79353500    0.59033300
O       2.44654100   -0.18974100   -0.27221400
O       0.69457900    1.52242900   -0.35011400
H       1.58739400    1.85395200   -0.51582900
""",
)

entry(
    index = 9,
    label = "160000000000000000003",
    molecule = 
"""
multiplicity 3
1 C u2 p1 c0
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[2.5,-2.81405e-15,9.04759e-18,-8.59194e-21,2.41827e-24,1.58714e+06,4.09089], Tmin=(10,'K'), Tmax=(1853.57,'K')),
            NASAPolynomial(coeffs=[2.5,-1.31298e-12,9.14088e-16,-2.78281e-19,3.12633e-23,1.58714e+06,4.09089], Tmin=(1853.57,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (13196.2,'kJ/mol'),
        Cp0 = (20.7862,'J/(mol*K)'),
        CpInf = (20.7862,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 3
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       2.24169700   -0.46415800    1.25031300
""",
)

entry(
    index = 10,
    label = "170170000000000000002",
    molecule = 
"""
multiplicity 2
1 O u1 p2 c0 {2,S}
2 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.49691,0.000178073,-9.52281e-07,1.47652e-09,-5.64343e-13,1.56223e+06,1.47277], Tmin=(10,'K'), Tmax=(998.496,'K')),
            NASAPolynomial(coeffs=[3.46813,-0.000332067,7.53692e-07,-2.89856e-10,3.49902e-14,1.56226e+06,1.76775], Tmin=(998.496,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (12989.1,'kJ/mol'),
        Cp0 = (29.1007,'J/(mol*K)'),
        CpInf = (37.4151,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
O       1.91256000    1.63056500    0.10315700
H       1.96000300    2.00145800   -0.79312100
""",
)

entry(
    index = 11,
    label = "190000000000000000002",
    molecule = 
"""
multiplicity 2
1 F u1 p3 c0
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[2.5,-2.81405e-15,9.04759e-18,-8.59194e-21,2.41827e-24,8067.55,3.94355], Tmin=(10,'K'), Tmax=(1853.57,'K')),
            NASAPolynomial(coeffs=[2.5,-1.31298e-12,9.14088e-16,-2.78281e-19,3.12633e-23,8067.55,3.94355], Tmin=(1853.57,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (67.0775,'kJ/mol'),
        Cp0 = (20.7862,'J/(mol*K)'),
        CpInf = (20.7862,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
F      -0.57094200    0.61858800   -0.95996300
""",
)

entry(
    index = 12,
    label = "200200000000000000001",
    molecule = 
"""
1 F u0 p3 c0 {2,S}
2 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.49724,0.000144772,-7.12082e-07,1.01113e-09,-3.47434e-13,-33024.5,0.922616], Tmin=(10,'K'), Tmax=(1095.29,'K')),
            NASAPolynomial(coeffs=[3.55836,-0.000520855,8.05397e-07,-2.81308e-10,3.17421e-14,-33011.3,0.743337], Tmin=(1095.29,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-274.582,'kJ/mol'),
        Cp0 = (29.1007,'J/(mol*K)'),
        CpInf = (37.4151,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
F      -2.12170500   -0.44599700    0.06574200
H      -1.88864500    0.37634300    0.40197800
""",
)

entry(
    index = 13,
    label = "500620380000000000001",
    molecule = 
"""
multiplicity 3
1 F u0 p3 c0 {3,S}
2 F u0 p3 c0 {3,S}
3 C u2 p0 c0 {1,S} {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.04101,-0.00301654,2.63982e-05,-3.77358e-08,1.7137e-11,-24825.7,5.90856], Tmin=(10,'K'), Tmax=(715.723,'K')),
            NASAPolynomial(coeffs=[3.30803,0.00639976,-4.48558e-06,1.41633e-09,-1.66208e-13,-24857,8.24771], Tmin=(715.723,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-206.407,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (58.2013,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -1.71957600   -1.36598100    0.12234800
F      -1.14493100   -2.23664900    0.88734800
F      -2.69609200   -0.90400400    0.83404800
""",
)

entry(
    index = 14,
    label = "690931140000000000002",
    molecule = 
"""
multiplicity 2
1 F u0 p3 c0 {4,S}
2 F u0 p3 c0 {4,S}
3 F u0 p3 c0 {4,S}
4 C u1 p0 c0 {1,S} {2,S} {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.05618,-0.00537534,6.96779e-05,-1.26128e-07,7.20829e-11,-60217.5,8.12052], Tmin=(10,'K'), Tmax=(578.86,'K')),
            NASAPolynomial(coeffs=[3.43544,0.0118905,-8.68919e-06,2.85302e-09,-3.47214e-13,-60363,8.89798], Tmin=(578.86,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-500.685,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (83.1447,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.10220400   -0.06032000    0.06073600
F      -0.55937000    0.62015800   -0.96313900
F      -0.53360300    0.43848300    1.19441400
F      -0.40025600   -1.33333200   -0.04291300
""",
)

entry(
    index = 15,
    label = "811611290340000000002",
    molecule = 
"""
multiplicity 2
1 S u1 p0 c0 {2,S} {3,D} {4,D}
2 O u0 p2 c0 {1,S} {5,S}
3 O u0 p2 c0 {1,D}
4 O u0 p2 c0 {1,D}
5 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.93777,0.00366122,5.40037e-05,-1.1452e-07,6.98395e-11,-8.95003e+07,10.1075], Tmin=(10,'K'), Tmax=(574.294,'K')),
            NASAPolynomial(coeffs=[4.52165,0.0139234,-1.02257e-05,3.48599e-09,-4.43148e-13,-8.95007e+07,5.55721], Tmin=(574.294,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-744148,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (108.088,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 2

Geometry:
S       1.73505600    0.05603500    0.03025900
O       2.24408300   -0.46556700    1.26254300
O       2.20296700   -0.38862400   -1.25652600
O       1.94580600    1.64391600    0.10531900
H       1.93803600    2.00208500   -0.79381800
""",
)

