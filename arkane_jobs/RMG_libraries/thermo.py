#!/usr/bin/env python
# encoding: utf-8

name = "thermo"
shortDesc = ""
longDesc = """
Calculated using Arkane v3.1.0 using LevelOfTheory(method='b97d3',basis='def2msvp',software='gaussian').
"""
entry(
    index = 0,
    label = "C3-SO3-HIR",
    molecule = 
"""
1  S u0 p0 c0 {9,S} {10,D} {11,D} {12,S}
2  F u0 p3 c0 {12,S}
3  F u0 p3 c0 {12,S}
4  F u0 p3 c0 {13,S}
5  F u0 p3 c0 {13,S}
6  F u0 p3 c0 {14,S}
7  F u0 p3 c0 {14,S}
8  F u0 p3 c0 {14,S}
9  O u0 p2 c0 {1,S} {15,S}
10 O u0 p2 c0 {1,D}
11 O u0 p2 c0 {1,D}
12 C u0 p0 c0 {1,S} {2,S} {3,S} {13,S}
13 C u0 p0 c0 {4,S} {5,S} {12,S} {14,S}
14 C u0 p0 c0 {6,S} {7,S} {8,S} {13,S}
15 H u0 p0 c0 {9,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.00757,0.0852641,8.71931e-06,-2.51283e-07,2.36799e-10,-8.96545e+07,16.3543], Tmin=(10,'K'), Tmax=(483.686,'K')),
            NASAPolynomial(coeffs=[12.1775,0.0553786,-4.10934e-05,1.37737e-08,-1.71107e-12,-8.96559e+07,-26.781], Tmin=(483.686,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-745430,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (357.522,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 2

Geometry:
C      -0.92434500   -0.70151100   -0.53149800
C      -1.67754000    0.60513100   -0.91884200
F      -2.64402500    0.30192500   -1.77661400
F      -0.84363400    1.45948800   -1.49901700
F      -2.21413100    1.17345700    0.15309600
C       0.12904800   -0.60141500    0.61770800
F       0.73311600   -1.79790700    0.70152200
F      -0.48578500   -0.34496700    1.76898200
S       1.49564300    0.66533600    0.40043500
O       2.14271300    0.38999300   -0.85065100
O       0.97160300    1.94010100    0.77032300
O       2.43995200    0.18966800    1.60393600
F      -1.84033400   -1.59449500   -0.12090400
F      -0.32025000   -1.17541000   -1.62648800
H       3.03796900   -0.50939300    1.30801300
""",
)

