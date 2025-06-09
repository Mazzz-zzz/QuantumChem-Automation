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
            NASAPolynomial(coeffs=[2.5,-2.81405e-15,9.04759e-18,-8.59194e-21,2.41827e-24,24359.5,-0.461279], Tmin=(10,'K'), Tmax=(1853.57,'K')),
            NASAPolynomial(coeffs=[2.5,-1.31298e-12,9.14088e-16,-2.78281e-19,3.12633e-23,24359.5,-0.461279], Tmin=(1853.57,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (202.536,'kJ/mol'),
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
H       2.96715300    1.22110000   -0.00174600
""",
)

entry(
    index = 1,
    label = "1131732952100000000002",
    molecule = 
"""
multiplicity 2
1 F u0 p3 c0 {6,S}
2 F u0 p3 c0 {6,S}
3 F u0 p3 c0 {6,S}
4 O u1 p2 c0 {7,S}
5 O u0 p2 c0 {7,D}
6 C u0 p0 c0 {1,S} {2,S} {3,S} {7,S}
7 C u0 p0 c0 {4,S} {5,D} {6,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.7506,0.0226849,2.9747e-05,-9.68184e-08,6.27146e-11,3.03411e+06,13.1677], Tmin=(10,'K'), Tmax=(606.615,'K')),
            NASAPolynomial(coeffs=[6.69809,0.0222498,-1.61604e-05,5.26811e-09,-6.37372e-13,3.03341e+06,-2.46043], Tmin=(606.615,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (25227,'kJ/mol'),
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
C       1.50629400    0.06962600    0.01299200
O       2.21739000   -0.88433000   -0.33760400
C      -0.03584900    0.01111200    0.00397000
F      -0.52864100    0.81275300    0.93960000
F      -0.48670200    0.40882500   -1.18570500
F      -0.44683000   -1.23097600    0.22550300
O       2.13859700    1.08476100    0.34178600
""",
)

entry(
    index = 2,
    label = "1141903082400600000001",
    molecule = 
"""
1 F u0 p3 c0 {6,S}
2 F u0 p3 c0 {6,S}
3 F u0 p3 c0 {6,S}
4 O u0 p2 c0 {7,S} {8,S}
5 O u0 p2 c0 {7,D}
6 C u0 p0 c0 {1,S} {2,S} {3,S} {7,S}
7 C u0 p0 c0 {4,S} {5,D} {6,S}
8 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.83005,0.0116774,0.000124,-3.29146e-07,2.48668e-10,3.00314e+06,12.2708], Tmin=(10,'K'), Tmax=(465.658,'K')),
            NASAPolynomial(coeffs=[5.09371,0.0287313,-2.08353e-05,6.91743e-09,-8.55663e-13,3.00272e+06,3.89115], Tmin=(465.658,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (24969.5,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (182.918,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C       0.58252600    0.30755700    0.02868200
O       1.02960800    1.39654700    0.21040100
C      -0.93414900   -0.00597400    0.04461700
F      -1.31732200   -0.51094800   -1.13129600
F      -1.21402800   -0.90007800    0.99702100
F      -1.63065000    1.09451600    0.27962300
O       1.27219900   -0.80143700   -0.21234700
H       2.21181500   -0.58018200   -0.21670000
""",
)

entry(
    index = 3,
    label = "1141942801461180600001",
    molecule = 
"""
multiplicity 3
1 F u0 p3 c0 {6,S}
2 F u0 p3 c0 {6,S}
3 F u0 p3 c0 {6,S}
4 O u0 p2 c0 {5,S} {7,S}
5 O u0 p2 c0 {4,S} {8,S}
6 C u0 p0 c0 {1,S} {2,S} {3,S} {7,S}
7 C u2 p0 c0 {4,S} {6,S}
8 H u0 p0 c0 {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.69148,0.0250943,7.15468e-05,-2.47941e-07,2.02995e-10,3.06675e+06,12.0498], Tmin=(10,'K'), Tmax=(463.34,'K')),
            NASAPolynomial(coeffs=[6.55197,0.0268475,-1.97498e-05,6.61302e-09,-8.22609e-13,3.0662e+06,-2.61345], Tmin=(463.34,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (25498.4,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (182.918,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.53102200    0.36507500    0.78528700
O      -2.69217600   -0.15208100    1.12957300
C       0.66382400    0.12225200   -0.15663200
F       1.65143200   -0.40569500    0.56800200
F       0.45582200   -0.68613800   -1.20610500
F       1.05359900    1.30589800   -0.63206100
O      -1.47865400   -0.29719200    0.31865500
H      -3.28640300   -0.72028000    0.61913400
""",
)

entry(
    index = 4,
    label = "160000000000000000003",
    molecule = 
"""
multiplicity 3
1 C u2 p1 c0
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[2.5,-2.81405e-15,9.04759e-18,-8.59194e-21,2.41827e-24,1.58801e+06,4.09089], Tmin=(10,'K'), Tmax=(1853.57,'K')),
            NASAPolynomial(coeffs=[2.5,-1.31298e-12,9.14088e-16,-2.78281e-19,3.12633e-23,1.58801e+06,4.09089], Tmin=(1853.57,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (13203.4,'kJ/mol'),
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
O       2.20524500   -0.99388800    0.00289400
""",
)

entry(
    index = 5,
    label = "170170000000000000002",
    molecule = 
"""
multiplicity 2
1 O u1 p2 c0 {2,S}
2 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.49692,0.000176978,-9.43965e-07,1.45966e-09,-5.56114e-13,1.56196e+06,1.47189], Tmin=(10,'K'), Tmax=(1001.24,'K')),
            NASAPolynomial(coeffs=[3.47107,-0.000338786,7.56163e-07,-2.89887e-10,3.4923e-14,1.56199e+06,1.75162], Tmin=(1001.24,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (12986.9,'kJ/mol'),
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
O       1.99952200    1.24837900   -0.00212800
H       2.96983900    1.22102400   -0.00174500
""",
)

entry(
    index = 6,
    label = "190000000000000000002",
    molecule = 
"""
multiplicity 2
1 F u1 p3 c0
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[2.5,-2.81405e-15,9.04759e-18,-8.59194e-21,2.41827e-24,8800.05,3.94355], Tmin=(10,'K'), Tmax=(1853.57,'K')),
            NASAPolynomial(coeffs=[2.5,-1.31298e-12,9.14088e-16,-2.78281e-19,3.12633e-23,8800.05,3.94355], Tmin=(1853.57,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (73.1678,'kJ/mol'),
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
F      -0.46549200    0.63128200    1.08138300
""",
)

entry(
    index = 7,
    label = "280280000000000000001",
    molecule = 
"""
multiplicity 3
1 O u0 p2 c0 {2,D}
2 C u2 p0 c0 {1,D}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.50428,-0.000214876,2.66217e-07,1.45016e-09,-1.08966e-12,1.55009e+06,3.8237], Tmin=(10,'K'), Tmax=(777.474,'K')),
            NASAPolynomial(coeffs=[3.00208,0.00120143,-2.13944e-07,-6.94466e-11,2.00027e-14,1.5502e+06,6.34701], Tmin=(777.474,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (12888.2,'kJ/mol'),
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
C       2.51671700   -2.16629300    0.57960000
O       2.11015000   -1.24973900    0.06821100
""",
)

entry(
    index = 8,
    label = "440560320000000000001",
    molecule = 
"""
1 O u0 p2 c0 {3,D}
2 O u0 p2 c0 {3,D}
3 C u0 p0 c0 {1,D} {2,D}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.01316,-0.00103598,1.23293e-05,-1.31085e-08,2.09921e-12,3.07333e+06,-5.86627], Tmin=(10,'K'), Tmax=(422.285,'K')),
            NASAPolynomial(coeffs=[3.17133,0.00510962,-3.00556e-06,8.47167e-10,-9.24246e-14,3.07342e+06,-2.33759], Tmin=(422.285,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (25553.1,'kJ/mol'),
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
C       2.33901500   -0.10350300   -0.67803300
O       2.67987000   -0.58573000   -1.67248200
O       1.99833200    0.37877000    0.31647100
""",
)

entry(
    index = 9,
    label = "450730450170000000002",
    molecule = 
"""
multiplicity 2
1 O u0 p2 c0 {3,S} {4,S}
2 O u0 p2 c0 {3,D}
3 C u1 p0 c0 {1,S} {2,D}
4 H u0 p0 c0 {1,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.04641,-0.00430434,4.95632e-05,-8.76702e-08,5.07185e-11,3.09864e+06,6.93631], Tmin=(10,'K'), Tmax=(545.757,'K')),
            NASAPolynomial(coeffs=[3.05998,0.00939603,-5.87617e-06,1.7756e-09,-2.06168e-13,3.09865e+06,10.2151], Tmin=(545.757,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (25763.6,'kJ/mol'),
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
C       1.57406500   -0.00505600    0.00049900
O       2.17734700   -1.01922000    0.00294000
O       2.00031100    1.24377200   -0.00211800
H       2.97169200    1.25606500   -0.00182100
""",
)

entry(
    index = 10,
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
            NASAPolynomial(coeffs=[4.04263,-0.00322312,2.87034e-05,-4.23717e-08,1.98619e-11,-18407.7,5.92597], Tmin=(10,'K'), Tmax=(696.642,'K')),
            NASAPolynomial(coeffs=[3.38088,0.00640004,-4.55615e-06,1.4563e-09,-1.72572e-13,-18456.8,7.86511], Tmin=(696.642,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-153.046,'kJ/mol'),
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
C      -1.25206000    0.34473900   -1.03536500
F      -2.16555500    1.24149300   -0.80607500
F      -1.90386800   -0.66764500   -1.52673800
""",
)

entry(
    index = 11,
    label = "641041150370000000001",
    molecule = 
"""
1 F u0 p3 c0 {4,S}
2 O u0 p2 c0 {4,S} {5,S}
3 O u0 p2 c0 {4,D}
4 C u0 p0 c0 {1,S} {2,S} {3,D}
5 H u0 p0 c0 {2,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.08348,-0.00834387,0.000101559,-1.9374e-07,1.18569e-10,3.04858e+06,8.35492], Tmin=(10,'K'), Tmax=(535.713,'K')),
            NASAPolynomial(coeffs=[3.18651,0.0149695,-1.02432e-05,3.29061e-09,-3.98297e-13,3.04844e+06,9.89707], Tmin=(535.713,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (25347.3,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (108.088,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C       1.74542700    0.03753000    0.95269600
O       2.75191900   -0.04144400    1.55182300
F       0.55015300   -0.30857200    1.48140700
O       1.58663900    0.45705000   -0.28952100
H       0.65824400    0.42280200   -0.54041100
""",
)

entry(
    index = 12,
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
            NASAPolynomial(coeffs=[4.05907,-0.00571747,7.37039e-05,-1.35105e-07,7.80652e-11,-51574.4,8.13565], Tmin=(10,'K'), Tmax=(575.04,'K')),
            NASAPolynomial(coeffs=[3.53931,0.011906,-8.80756e-06,2.91681e-09,-3.57124e-13,-51746.2,8.34175], Tmin=(575.04,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-428.823,'kJ/mol'),
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
C      -0.04973300    0.00461500   -0.00007400
F      -0.44840200    0.63414900    1.08534000
F      -0.44765500    0.62915600   -1.08864200
F      -0.44621300   -1.25061100    0.00267200
""",
)

entry(
    index = 13,
    label = "701061740000000000001",
    molecule = 
"""
1 F u0 p3 c0 {4,S}
2 F u0 p3 c0 {4,S}
3 F u0 p3 c0 {4,S}
4 C u0 p0 c0 {1,S} {2,S} {3,S} {5,S}
5 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[4.07015,-0.00601483,7.34018e-05,-1.20396e-07,6.31007e-11,-79091.9,7.48804], Tmin=(10,'K'), Tmax=(614.548,'K')),
            NASAPolynomial(coeffs=[2.50728,0.0163529,-1.09604e-05,3.41195e-09,-4.00662e-13,-79130.1,12.3934], Tmin=(614.548,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (-657.61,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (108.088,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -1.15045000    0.15389200    0.52353700
F      -2.42465300    0.26577200    0.90755500
F      -1.01990600    0.72171300   -0.67817000
F      -0.85516400   -1.14378200    0.41200800
H      -0.49059100    0.63452700    1.24627500
""",
)

entry(
    index = 14,
    label = "861382320600000000001",
    molecule = 
"""
1 F u0 p3 c0 {5,S}
2 F u0 p3 c0 {5,S}
3 F u0 p3 c0 {5,S}
4 O u0 p2 c0 {5,S} {6,S}
5 C u0 p0 c0 {1,S} {2,S} {3,S} {4,S}
6 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.92772,0.00413201,6.93696e-05,-1.37947e-07,7.96768e-11,1.45521e+06,9.1663], Tmin=(10,'K'), Tmax=(596.673,'K')),
            NASAPolynomial(coeffs=[4.06347,0.0205156,-1.52928e-05,5.22224e-09,-6.61926e-13,1.45489e+06,6.00182], Tmin=(596.673,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (12099.3,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (133.032,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 1
External symmetry: -1.0
Optical isomers: 1

Geometry:
C      -0.76438800    0.78306600    0.10160400
F      -0.38094800    0.79178000    1.39030300
F      -1.72527100    1.67727000   -0.05709800
F      -1.27408000   -0.43860500   -0.13406300
O       0.24246500    1.08280400   -0.73028100
H       0.94863400    0.43869600   -0.62502900
""",
)

entry(
    index = 15,
    label = "951592011700400000002",
    molecule = 
"""
multiplicity 2
1 F u0 p3 c0 {6,S}
2 F u0 p3 c0 {6,S}
3 O u0 p2 c0 {5,S} {7,S}
4 O u0 p2 c0 {5,D}
5 C u0 p0 c0 {3,S} {4,D} {6,S}
6 C u1 p0 c0 {1,S} {2,S} {5,S}
7 H u0 p0 c0 {3,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.70287,0.0259351,-3.81162e-06,-3.43108e-08,2.74669e-11,3.05007e+06,11.5478], Tmin=(10,'K'), Tmax=(591.081,'K')),
            NASAPolynomial(coeffs=[5.98312,0.0201376,-1.35464e-05,4.24252e-09,-5.01756e-13,3.04963e+06,0.322255], Tmin=(591.081,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (25359.7,'kJ/mol'),
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
C       1.55327200   -0.03112300   -0.01667400
O       2.22953100   -0.95683000    0.36744000
C       0.15110700   -0.14750600   -0.30129900
F      -0.60037000    0.83177600   -0.71984300
F      -0.48216000   -1.27398600   -0.16452900
O       2.00256800    1.21930100   -0.22933300
H       2.94295600    1.21995500   -0.01835000
""",
)

entry(
    index = 16,
    label = "971452351050000000002",
    molecule = 
"""
multiplicity 2
1 F u0 p3 c0 {5,S}
2 F u0 p3 c0 {5,S}
3 F u0 p3 c0 {5,S}
4 O u0 p2 c0 {6,D}
5 C u0 p0 c0 {1,S} {2,S} {3,S} {6,S}
6 C u1 p0 c0 {4,D} {5,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.82264,0.014547,4.97541e-05,-1.42701e-07,1.01848e-10,1.49461e+06,11.5327], Tmin=(10,'K'), Tmax=(520.094,'K')),
            NASAPolynomial(coeffs=[5.57977,0.0188198,-1.3868e-05,4.60675e-09,-5.67476e-13,1.49419e+06,1.89162], Tmin=(520.094,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (12426.9,'kJ/mol'),
        Cp0 = (33.2579,'J/(mol*K)'),
        CpInf = (133.032,'J/(mol*K)'),
    ),
    shortDesc = """""",
    longDesc = 
"""
Spin multiplicity: 2
External symmetry: -1.0
Optical isomers: 1

Geometry:
C       1.55167200   -0.00742200    0.00045300
O       2.22879600   -0.95626600    0.00287100
C      -0.01460700   -0.01544300   -0.00002600
F      -0.44226200    0.62614100    1.08236500
F      -0.44156900    0.62118300   -1.08561300
F      -0.51997800   -1.24472600    0.00262000
""",
)

entry(
    index = 17,
    label = "981622481180600000001",
    molecule = 
"""
multiplicity 3
1 F u0 p3 c0 {5,S}
2 F u0 p3 c0 {5,S}
3 F u0 p3 c0 {5,S}
4 O u0 p2 c0 {6,S} {7,S}
5 C u0 p0 c0 {1,S} {2,S} {3,S} {6,S}
6 C u2 p0 c0 {4,S} {5,S}
7 H u0 p0 c0 {4,S}
""",
    thermo = NASA(
        polynomials = [
            NASAPolynomial(coeffs=[3.88009,0.00784047,0.000100279,-2.43795e-07,1.71189e-10,1.49889e+06,11.1961], Tmin=(10,'K'), Tmax=(494.453,'K')),
            NASAPolynomial(coeffs=[4.51373,0.0247798,-1.80478e-05,5.99687e-09,-7.40439e-13,1.49856e+06,5.85782], Tmin=(494.453,'K'), Tmax=(3000,'K')),
        ],
        Tmin = (10,'K'),
        Tmax = (3000,'K'),
        E0 = (12462.5,'kJ/mol'),
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
C       1.49621000    0.20667300   -0.46908500
C       0.00660300    0.07863700   -0.07904300
F      -0.40501900    0.80094400    0.97024900
F      -0.72767500    0.44349800   -1.13607900
F      -0.23767300   -1.20821300    0.19276700
O       2.02935800    1.03102600    0.36674300
H       2.96436200    1.13419400    0.15035000
""",
)

