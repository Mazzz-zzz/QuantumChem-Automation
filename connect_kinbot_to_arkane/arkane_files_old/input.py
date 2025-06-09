#!/usr/bin/env python
# encoding: utf-8


#modelChemistry = "M06-2X/def2TZVP"
#modelChemistry = "wb97x-d3/def2-tzvp"
 
useAtomCorrections = True
#Empirical compilations (e.g. Kesharwani & Martin, J. Phys. Chem. A 2015, 119, 1701) put B97-D/def2-SVP at 0.994 ± 0.005.
#frequencyScaleFactor = 0.987


modelChemistry = LevelOfTheory(
    method='b97d3',
    basis='def2msvp',
    software='gaussian'  # Specify the software used for calculations
)
#modelChemistry = "b97d-3/def2-msvp"

atomEnergies = {
    "H": -0.499278,   # doublet 2S
    "C": -37.848505,  # triplet 3P
    "F": -99.731526,  # doublet 2P
    "S": -100.000000,  # doublet 2P
    "O": -79.999999,  # doublet 2P
}

#atomEnergies = {
#    "H": -0.499278,   # doublet 2S
#    "C": -37.848505,  # triplet 3P
#    "F": -99.731526,  # doublet 2P
#}


useHinderedRotors = False
useBondCorrections = False


# ------------------------ species (external *.py) ----------------------------
species('10000000000000000002', '10000000000000000002.py', structure=SMILES('[H]'))
species('140260020000000000003', '140260020000000000003.py', structure=SMILES('[H][C][H]'))
species('190000000000000000002', '190000000000000000002.py', structure=SMILES('[F]'))
species('200200000000000000001', '200200000000000000001.py', structure=SMILES('[H][F]'))
species('20020000000000000001', '20020000000000000001.py', structure=SMILES('[H][H]'))
species('320440200000000000001', '320440200000000000001.py', structure=SMILES('[H][C][F]'))
species('330570420000000000002', '330570420000000000002.py', structure=SMILES('[H][C]([H])[F]'))
species('340700660000000000001', '340700660000000000001.py', structure=SMILES('[H][C]([H])([H])[F]'))
species('460940920440000000001', '460940920440000000001.py', structure=SMILES('[H][C]([H])=[C]([H])[F]'))
species('471071270480000000002', '471071270480000000002.py', structure=SMILES('[H][C]([H])[C]([H])([H])[F]'))
species('520881200000000000001', '520881200000000000001.py', structure=SMILES('[H][C]([H])([F])[F]'))
species('641121280800000000001', '641121280800000000001.py', structure=SMILES('[H][C]([F])=[C]([H])[F]'))
species('641121300780000000001', '641121300780000000001.py', structure=SMILES('[H][C]([H])([F])[C][F]'))
species('651251631020000000002', '651251631020000000002.py', structure=SMILES('[H][C]([F])[C]([H])([H])[F]'))
species('661381981260000000001', '661381981260000000001.py', structure=SMILES('[H][C]([H])([F])[C]([H])([H])[F]'))

# ------------------------ transition state (uncomment if needed) -------------
transitionState('661381981260000000001_r12_insertion_R_1_2_3', '661381981260000000001_r12_insertion_R_1_2_3.py')
transitionState('661381981260000000001_r12_insertion_R_1_2_5', '661381981260000000001_r12_insertion_R_1_2_5.py')
transitionState('661381981260000000001_r12_insertion_R_3_2_5', '661381981260000000001_r12_insertion_R_3_2_5.py')
transitionState('661381981260000000001_r12_insertion_R_5_2_3', '661381981260000000001_r12_insertion_R_5_2_3.py')
transitionState('661381981260000000001_r12_insertion_R_5_2_6', '661381981260000000001_r12_insertion_R_5_2_6.py')


# ------------------------ kinetics block  -----------------------------------
# Reaction definitions:
reaction(
    label          = '661381981260000000001 <=> 140260020000000000003 + 520881200000000000001',
    reactants      = ['661381981260000000001'],
    products       = ['140260020000000000003', '520881200000000000001'],
    transitionState= '661381981260000000001_r12_insertion_R_1_2_3',
)

reaction(
    label          = '661381981260000000001 <=> 200200000000000000001 + 460940920440000000001',
    reactants      = ['661381981260000000001'],
    products       = ['200200000000000000001', '460940920440000000001'],
    transitionState= '661381981260000000001_r12_insertion_R_1_2_5',
)

reaction(
    label          = '661381981260000000001 <=> 320440200000000000001 + 340700660000000000001',
    reactants      = ['661381981260000000001'],
    products       = ['320440200000000000001', '340700660000000000001'],
    transitionState= '661381981260000000001_r12_insertion_R_3_2_5',
)

reaction(
    label          = '661381981260000000001 <=> 20020000000000000001 + 641121280800000000001',
    reactants      = ['661381981260000000001'],
    products       = ['20020000000000000001', '641121280800000000001'],
    transitionState= '661381981260000000001_r12_insertion_R_5_2_3',
)

reaction(
    label          = '661381981260000000001 <=> 20020000000000000001 + 641121300780000000001',
    reactants      = ['661381981260000000001'],
    products       = ['20020000000000000001', '641121300780000000001'],
    transitionState= '661381981260000000001_r12_insertion_R_5_2_6',
)


# ------------------------- high-P-limit kinetics fits ------------------------
kinetics(
    label = '661381981260000000001 <=> 140260020000000000003 + 520881200000000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

kinetics(
    label = '661381981260000000001 <=> 200200000000000000001 + 460940920440000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

kinetics(
    label = '661381981260000000001 <=> 320440200000000000001 + 340700660000000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

kinetics(
    label = '661381981260000000001 <=> 20020000000000000001 + 641121280800000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

kinetics(
    label = '661381981260000000001 <=> 20020000000000000001 + 641121300780000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

# ------------------------- high-P-limit kinetics fits ------------------------
# Example of kinetics calculation:
# kinetics(
#     label = '{species} <=> Product1 + Product2',
#     Tmin  = (300,  'K'),
#     Tmax  = (2000, 'K'),
#     Tcount= 20,
# )

# Example of bath gas definition for pressure dependence:
# species(
#     label = 'nitrogen',
#     structure = SMILES('N#N'),
#     molecularWeight = (28.04,"g/mol"),
#     collisionModel = TransportData(sigma=(3.70,'angstrom'), epsilon=(94.9,'K')),
#     reactive = False
# )

# Example of network definition:
# network(
#     label = '{species}_pdep',
#     isomers = ['{species}'],
#     reactants = [
#         ('Product1', 'Product2'),
#     ],
#     bathGas = {
#         'nitrogen': 1.0,
#     }
# )

# ------------------------ pressure dependence (uncomment if needed) ----------
# pressureDependence(
#     '{species}_pdep',
#     Tmin=(300.0,'K'), Tmax=(2000.0,'K'), Tcount=8,
#     Pmin=(0.01,'bar'), Pmax=(100.0,'bar'), Pcount=5,
#     maximumGrainSize = (10,'kcal/mol'),
#     minimumGrainCount = 250,
#     method = 'chemically-significant eigenvalues',
#     interpolationModel = ('chebyshev', 6, 4),
#     activeJRotor = True,
# )


# ------------------------ thermo calculation ---------------------------------
statmech('10000000000000000002')
thermo('10000000000000000002', 'NASA')

statmech('140260020000000000003')
thermo('140260020000000000003', 'NASA')

statmech('190000000000000000002')
thermo('190000000000000000002', 'NASA')

statmech('200200000000000000001')
thermo('200200000000000000001', 'NASA')

statmech('20020000000000000001')
thermo('20020000000000000001', 'NASA')

statmech('320440200000000000001')
thermo('320440200000000000001', 'NASA')

statmech('330570420000000000002')
thermo('330570420000000000002', 'NASA')

statmech('340700660000000000001')
thermo('340700660000000000001', 'NASA')

statmech('460940920440000000001')
thermo('460940920440000000001', 'NASA')

statmech('471071270480000000002')
thermo('471071270480000000002', 'NASA')

statmech('520881200000000000001')
thermo('520881200000000000001', 'NASA')

statmech('641121280800000000001')
thermo('641121280800000000001', 'NASA')

statmech('641121300780000000001')
thermo('641121300780000000001', 'NASA')

statmech('651251631020000000002')
thermo('651251631020000000002', 'NASA')

statmech('661381981260000000001')
thermo('661381981260000000001', 'NASA')

statmech('661381981260000000001_r12_insertion_R_1_2_3')
statmech('661381981260000000001_r12_insertion_R_1_2_5')
statmech('661381981260000000001_r12_insertion_R_3_2_5')
statmech('661381981260000000001_r12_insertion_R_5_2_3')
statmech('661381981260000000001_r12_insertion_R_5_2_6')
