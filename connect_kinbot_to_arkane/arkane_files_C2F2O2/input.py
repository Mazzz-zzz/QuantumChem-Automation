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
species('160000000000000000003', '160000000000000000003.py', structure=SMILES('[C]'))
species('190000000000000000002', '190000000000000000002.py', structure=SMILES('[F]'))
species('280280000000000000001', '280280000000000000001.py', structure=SMILES('[C]=[O]'))
species('470590350000000000002', '470590350000000000002.py', structure=SMILES('[O]=[C][F]'))
species('660901080000000000001', '660901080000000000001.py', structure=SMILES('[O]=[C]([F])[F]'))
species('751111220670000000002', '751111220670000000002.py', structure=SMILES('[O][C]([F])=[C]=[O]'))
species('781141250730000000001', '781141250730000000001.py', structure=SMILES('[O][C]([F])=[C][F]'))
species('941421881400000000001', '941421881400000000001.py', structure=SMILES('[O]=[C]([F])[C](=[O])[F]'))
species('941461610900730000001', '941461610900730000001.py', structure=SMILES('[O]=[C]([F])[O][C][F]'))
species('941742762340700000001', '941742762340700000001.py', structure=SMILES('[F][C][C]1([F])[O][O]1'))

# ------------------------ transition state (uncomment if needed) -------------
transitionState('941421881400000000001_r12_insertion_R_1_3_5', '941421881400000000001_r12_insertion_R_1_3_5.py')
transitionState('941421881400000000001_r12_insertion_R_4_3_1', '941421881400000000001_r12_insertion_R_4_3_1.py')
transitionState('941421881400000000001_r12_insertion_R_5_3_1', '941421881400000000001_r12_insertion_R_5_3_1.py')
transitionState('941421881400000000001_ketoenol_2_1_3_4', '941421881400000000001_ketoenol_2_1_3_4.py')


# ------------------------ kinetics block  -----------------------------------
# Reaction definitions:
reaction(
    label          = '941421881400000000001_R1 <=> 280280000000000000001 + 660901080000000000001',
    reactants      = ['941421881400000000001'],
    products       = ['280280000000000000001', '660901080000000000001'],
    transitionState= '941421881400000000001_r12_insertion_R_1_3_5',
)

reaction(
    label          = '941421881400000000001_R2 <=> 941461610900730000001',
    reactants      = ['941421881400000000001'],
    products       = ['941461610900730000001'],
    transitionState= '941421881400000000001_r12_insertion_R_4_3_1',
)

reaction(
    label          = '941421881400000000001_R3 <=> 280280000000000000001 + 660901080000000000001',
    reactants      = ['941421881400000000001'],
    products       = ['280280000000000000001', '660901080000000000001'],
    transitionState= '941421881400000000001_r12_insertion_R_5_3_1',
)

reaction(
    label          = '941421881400000000001_R4 <=> 941742762340700000001',
    reactants      = ['941421881400000000001'],
    products       = ['941742762340700000001'],
    transitionState= '941421881400000000001_ketoenol_2_1_3_4',
)


# ------------------------- high-P-limit kinetics fits ------------------------
kinetics(
    label = '941421881400000000001_R1 <=> 280280000000000000001 + 660901080000000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

kinetics(
    label = '941421881400000000001_R2 <=> 941461610900730000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

kinetics(
    label = '941421881400000000001_R3 <=> 280280000000000000001 + 660901080000000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

kinetics(
    label = '941421881400000000001_R4 <=> 941742762340700000001',
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
statmech('160000000000000000003')
thermo('160000000000000000003', 'NASA')

statmech('190000000000000000002')
thermo('190000000000000000002', 'NASA')

statmech('280280000000000000001')
thermo('280280000000000000001', 'NASA')

statmech('470590350000000000002')
thermo('470590350000000000002', 'NASA')

statmech('660901080000000000001')
thermo('660901080000000000001', 'NASA')

statmech('751111220670000000002')
thermo('751111220670000000002', 'NASA')

statmech('781141250730000000001')
thermo('781141250730000000001', 'NASA')

statmech('941421881400000000001')
thermo('941421881400000000001', 'NASA')

statmech('941461610900730000001')
thermo('941461610900730000001', 'NASA')

statmech('941742762340700000001')
thermo('941742762340700000001', 'NASA')

statmech('941421881400000000001_r12_insertion_R_1_3_5')
statmech('941421881400000000001_r12_insertion_R_4_3_1')
statmech('941421881400000000001_r12_insertion_R_5_3_1')
statmech('941421881400000000001_ketoenol_2_1_3_4')
