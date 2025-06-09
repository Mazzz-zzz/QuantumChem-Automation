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
species('1001482001520000000001', '1001482001520000000001.py', structure=SMILES('[F][C]([F])=[C]([F])[F]'))
species('1001482381140000000001', '1001482381140000000001.py', structure=SMILES('[F][C][C]([F])([F])[F]'))
species('1002122340540000000001', '1002122340540000000001.py', structure=SMILES('[H][O][S](=[O])(=[O])[F]'))
species('1191793072280000000002', '1191793072280000000002.py', structure=SMILES('[F][C]([F])[C]([F])([F])[F]'))
species('1312673532570400000002', '1312673532570400000002.py', structure=SMILES('[H][O][S]([O])(=[O])=[C]([F])[F]'))
species('1502823922432230600001', '1502823922432230600001.py', structure=SMILES('[H][O][S](=[O])[O][C]([F])([F])[F]'))
species('1502984803620600000001', '1502984803620600000001.py', structure=SMILES('[H][O][S](=[O])(=[O])[C]([F])([F])[F]'))
species('160000000000000000003', '160000000000000000003.py', structure=SMILES('[C]'))
species('170170000000000000002', '170170000000000000002.py', structure=SMILES('[H][O]'))
species('1803646687765942100001', '1803646687765942100001.py', structure=SMILES('[O]=[S]1(=[O])[O][C]1([F])[C]([F])([F])[F]'))
species('1813535465033480600002', '1813535465033480600002.py', structure=SMILES('[H][O][S]([O])(=[O])=[C]([F])[C]([F])([F])[F]'))
species('1813535595952630400002', '1813535595952630400002.py', structure=SMILES('[H][O][S](=[O])(=[O])[C]([F])([F])[C]([F])[F]'))
species('1833195415772100000002', '1833195415772100000002.py', structure=SMILES('[O]=[S](=[O])[C]([F])([F])[C]([F])([F])[F]'))
species('1843365746072630600001', '1843365746072630600001.py', structure=SMILES('[H][O][S](=[O])[C]([F])([F])[C]([F])([F])[F]'))
species('190000000000000000002', '190000000000000000002.py', structure=SMILES('[F]'))
species('1993676336753150000002', '1993676336753150000002.py', structure=SMILES('[O][S](=[O])(=[O])[C]([F])([F])[C]([F])([F])[F]'))
species('200200000000000000001', '200200000000000000001.py', structure=SMILES('[H][F]'))
species('2003846667223680600001', '2003846667223680600001.py', structure=SMILES('[H][O][S](=[O])(=[O])[C]([F])([F])[C]([F])([F])[F]'))
species('2003847066703800600001', '2003847066703800600001.py', structure=SMILES('[H][O][C]([F])([F])[S](=[O])(=[O])[C]([F])([F])[F]'))
species('2003885976044371740001', '2003885976044371740001.py', structure=SMILES('[H][O][S](=[O])([O][F])=[C]([F])[C]([F])([F])[F]'))
species('2004167628425982700001', '2004167628425982700001.py', structure=SMILES('[H][O][S]1([C]([F])([F])[C]([F])([F])[F])[O][O]1'))
species('2004328380979804780401', '2004328380979804780401.py', structure=SMILES('[H][O][S]1(=[O])([F])[O][C]([F])([F])[C]1([F])[F]'))
species('500620380000000000001', '500620380000000000001.py', structure=SMILES('[F][C][F]'))
species('690931140000000000002', '690931140000000000002.py', structure=SMILES('[F][C]([F])[F]'))
species('811611290340000000002', '811611290340000000002.py', structure=SMILES('[H][O][S](=[O])=[O]'))


# ------------------------ transition state (uncomment if needed) -------------
transitionState('2003846667223680600001_r12_insertion_R_3_2_5', '2003846667223680600001_r12_insertion_R_3_2_5.py')
transitionState('2003846667223680600001_r12_insertion_R_5_2_1', '2003846667223680600001_r12_insertion_R_5_2_1.py')
transitionState('2003846667223680600001_r12_insertion_R_5_2_3', '2003846667223680600001_r12_insertion_R_5_2_3.py')
transitionState('2003846667223680600001_r12_insertion_R_6_5_7', '2003846667223680600001_r12_insertion_R_6_5_7.py')
transitionState('2003846667223680600001_r12_insertion_R_9_1_2', '2003846667223680600001_r12_insertion_R_9_1_2.py')
transitionState('2003846667223680600001_r12_insertion_R_9_1_10', '2003846667223680600001_r12_insertion_R_9_1_10.py')
transitionState('2003846667223680600001_r13_insertion_ROR_1_2_5_6', '2003846667223680600001_r13_insertion_ROR_1_2_5_6.py')
transitionState('2003846667223680600001_r13_insertion_ROR_1_2_5_8', '2003846667223680600001_r13_insertion_ROR_1_2_5_8.py')
transitionState('2003846667223680600001_r13_insertion_ROR_3_2_5_6', '2003846667223680600001_r13_insertion_ROR_3_2_5_6.py')
transitionState('2003846667223680600001_r13_insertion_ROR_3_2_5_8', '2003846667223680600001_r13_insertion_ROR_3_2_5_8.py')
transitionState('2003846667223680600001_r13_insertion_RSR_9_1_2_5', '2003846667223680600001_r13_insertion_RSR_9_1_2_5.py')


# ------------------------ kinetics block  -----------------------------------
# Reaction definitions:
reaction(
    label          = '2003846667223680600001 <=> 1001482381140000000001 + 1002122340540000000001',
    reactants      = ['2003846667223680600001'],
    products       = ['1001482381140000000001', '1002122340540000000001'],
    transitionState= '2003846667223680600001_r12_insertion_R_3_2_5',
)

reaction(
    label          = '2003846667223680600001 <=> 2003847066703800600001',
    reactants      = ['2003846667223680600001'],
    products       = ['2003847066703800600001'],
    transitionState= '2003846667223680600001_r12_insertion_R_5_2_1',
)

reaction(
    label          = '2003846667223680600001 <=> 1001482381140000000001 + 1002122340540000000001',
    reactants      = ['2003846667223680600001'],
    products       = ['1001482381140000000001', '1002122340540000000001'],
    transitionState= '2003846667223680600001_r12_insertion_R_5_2_3',
)

reaction(
    label          = '2003846667223680600001 <=> 2004167628425982700001',
    reactants      = ['2003846667223680600001'],
    products       = ['2004167628425982700001'],
    transitionState= '2003846667223680600001_r12_insertion_R_6_5_7',
)

reaction(
    label          = '2003846667223680600001 <=> 1502984803620600000001 + 500620380000000000001',
    reactants      = ['2003846667223680600001'],
    products       = ['1502984803620600000001', '500620380000000000001'],
    transitionState= '2003846667223680600001_r12_insertion_R_9_1_2',
)

reaction(
    label          = '2003846667223680600001 <=> 2004328380979804780401',
    reactants      = ['2003846667223680600001'],
    products       = ['2004328380979804780401'],
    transitionState= '2003846667223680600001_r12_insertion_R_9_1_10',
)

reaction(
    label          = '2003846667223680600001 <=> 1502823922432230600001 + 500620380000000000001',
    reactants      = ['2003846667223680600001'],
    products       = ['1502823922432230600001', '500620380000000000001'],
    transitionState= '2003846667223680600001_r13_insertion_ROR_1_2_5_6',
)


reaction(
    label          = '2003846667223680600001 <=> 2003885976044371740001',
    reactants      = ['2003846667223680600001'],
    products       = ['2003885976044371740001'],
    transitionState= '2003846667223680600001_r13_insertion_ROR_3_2_5_6',
)

reaction(
    label          = '2003846667223680600001 <=> 1803646687765942100001 + 200200000000000000001',
    reactants      = ['2003846667223680600001'],
    products       = ['1803646687765942100001', '200200000000000000001'],
    transitionState= '2003846667223680600001_r13_insertion_ROR_3_2_5_8',
)

reaction(
    label          = '2003846667223680600001 <=> 1001482001520000000001 + 1002122340540000000001',
    reactants      = ['2003846667223680600001'],
    products       = ['1001482001520000000001', '1002122340540000000001'],
    transitionState= '2003846667223680600001_r13_insertion_RSR_9_1_2_5',
)



# ------------------------- high-P-limit kinetics fits ------------------------
kinetics(
    label = '2003846667223680600001 <=> 1001482381140000000001 + 1002122340540000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
    three_params = False,

)

kinetics(
    label = '2003846667223680600001 <=> 1001482381140000000001 + 1002122340540000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
    three_params = False,

)

kinetics(
    label = '2003846667223680600001 <=> 1502984803620600000001 + 500620380000000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
    three_params = False,

)

kinetics(
    label = '2003846667223680600001 <=> 1502823922432230600001 + 500620380000000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
    three_params = False,

)

kinetics(
    label = '2003846667223680600001 <=> 1803646687765942100001 + 200200000000000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
    three_params = False,

)

kinetics(
    label = '2003846667223680600001 <=> 1001482001520000000001 + 1002122340540000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
    three_params = False,

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

statmech('1001482001520000000001')
thermo('1001482001520000000001', 'NASA')

statmech('1001482381140000000001')
thermo('1001482381140000000001', 'NASA')

statmech('1002122340540000000001')
thermo('1002122340540000000001', 'NASA')

statmech('1191793072280000000002')
thermo('1191793072280000000002', 'NASA')

statmech('1312673532570400000002')
thermo('1312673532570400000002', 'NASA')

statmech('1502823922432230600001')
thermo('1502823922432230600001', 'NASA')

statmech('1502984803620600000001')
thermo('1502984803620600000001', 'NASA')

statmech('160000000000000000003')
thermo('160000000000000000003', 'NASA')

statmech('170170000000000000002')
thermo('170170000000000000002', 'NASA')

statmech('1803646687765942100001')
thermo('1803646687765942100001', 'NASA')

statmech('1813535465033480600002')
thermo('1813535465033480600002', 'NASA')

statmech('1813535595952630400002')
thermo('1813535595952630400002', 'NASA')

statmech('1833195415772100000002')
thermo('1833195415772100000002', 'NASA')

statmech('1843365746072630600001')
thermo('1843365746072630600001', 'NASA')

statmech('190000000000000000002')
thermo('190000000000000000002', 'NASA')

statmech('1993676336753150000002')
thermo('1993676336753150000002', 'NASA')

statmech('200200000000000000001')
thermo('200200000000000000001', 'NASA')

statmech('2003846667223680600001')
thermo('2003846667223680600001', 'NASA')

statmech('2003847066703800600001')
thermo('2003847066703800600001', 'NASA')

statmech('2003885976044371740001')
thermo('2003885976044371740001', 'NASA')

statmech('2004167628425982700001')
thermo('2004167628425982700001', 'NASA')

statmech('2004328380979804780401')
thermo('2004328380979804780401', 'NASA')

statmech('500620380000000000001')
thermo('500620380000000000001', 'NASA')

statmech('690931140000000000002')
thermo('690931140000000000002', 'NASA')

statmech('811611290340000000002')
thermo('811611290340000000002', 'NASA')

statmech('2003846667223680600001_r12_insertion_R_3_2_5')
statmech('2003846667223680600001_r12_insertion_R_5_2_1')
statmech('2003846667223680600001_r12_insertion_R_5_2_3')
statmech('2003846667223680600001_r12_insertion_R_6_5_7')
statmech('2003846667223680600001_r12_insertion_R_9_1_2')
statmech('2003846667223680600001_r12_insertion_R_9_1_10')
statmech('2003846667223680600001_r13_insertion_ROR_1_2_5_6')
statmech('2003846667223680600001_r13_insertion_ROR_1_2_5_8')
statmech('2003846667223680600001_r13_insertion_ROR_3_2_5_6')
statmech('2003846667223680600001_r13_insertion_ROR_3_2_5_8')
statmech('2003846667223680600001_r13_insertion_RSR_9_1_2_5')
