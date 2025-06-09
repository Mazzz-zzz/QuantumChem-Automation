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
species('1001482381140000000001', '1001482381140000000001.py', structure=SMILES('[F][C][C]([F])([F])[F]'))
species('1141903082400600000001', '1141903082400600000001.py', structure=SMILES('[H][O][C](=[O])[C]([F])([F])[F]'))
species('1191793072280000000002', '1191793072280000000002.py', structure=SMILES('[F][C]([F])[C]([F])([F])[F]'))
species('1201923602880000000001', '1201923602880000000001.py', structure=SMILES('[H][C]([F])([F])[C]([F])([F])[F]'))
species('1362244183860600000001', '1362244183860600000001.py', structure=SMILES('[H][O][C]([F])([F])[C]([F])([F])[F]'))
species('1452453874401930400002', '1452453874401930400002.py', structure=SMILES('[H][O][C](=[O])[C]([F])([F])[C]([F])[F]'))
species('1452453943632430600002', '1452453943632430600002.py', structure=SMILES('[H][O][C](=[O])[C]([F])[C]([F])([F])[F]'))
species('1472314214191050000002', '1472314214191050000002.py', structure=SMILES('[O]=[C][C]([F])([F])[C]([F])([F])[F]'))
species('1482484344321580600001', '1482484344321580600001.py', structure=SMILES('[H][O][C][C]([F])([F])[C]([F])([F])[F]'))
species('160000000000000000003', '160000000000000000003.py', structure=SMILES('[C]'))
species('1632594815172100000002', '1632594815172100000002.py', structure=SMILES('[O][C](=[O])[C]([F])([F])[C]([F])([F])[F]'))
species('1642764945472630600001', '1642764945472630600001.py', structure=SMILES('[H][O][C](=[O])[C]([F])([F])[C]([F])([F])[F]'))
species('1642764945472630600001_ketoenol_2_1_3_8', '1642764945472630600001_ketoenol_2_1_3_8.py', structure=SMILES('[C]'))
species('1642804254293321740001', '1642804254293321740001.py', structure=SMILES('[H][O][C]([O][F])=[C]([F])[C]([F])([F])[F]'))
species('1642804443153132880001', '1642804443153132880001.py', structure=SMILES('[H][O][C]([O][C]([F])([F])[F])=[C]([F])[F]'))
species('1642804664602161580601', '1642804664602161580601.py', structure=SMILES('[C](C(C(F)(F)F)(F)F)OO'))
species('1642804744642041580601', '1642804744642041580601.py', structure=SMILES('[H][O][C][O][C]([F])([F])[C]([F])([F])[F]'))
species('1643046107386123120601', '1643046107386123120601.py', structure=SMILES('[H][O][C]1([F])[O][C]1([F])[C]([F])([F])[F]'))
species('170170000000000000002', '170170000000000000002.py', structure=SMILES('[H][O]'))
species('190000000000000000002', '190000000000000000002.py', structure=SMILES('[F]'))
species('280280000000000000001', '280280000000000000001.py', structure=SMILES('[C]=[O]'))
species('440560320000000000001', '440560320000000000001.py', structure=SMILES('[O]=[C]=[O]'))
species('450730450170000000002', '450730450170000000002.py', structure=SMILES('[H][O][C]=[O]'))
species('500620380000000000001', '500620380000000000001.py', structure=SMILES('[F][C][F]'))
species('641041150370000000001', '641041150370000000001.py', structure=SMILES('[H][O][C](=[O])[F]'))
species('690931140000000000002', '690931140000000000002.py', structure=SMILES('[F][C]([F])[F]'))
species('761281321000200000001', '761281321000200000001.py', structure=SMILES('[H][O][C](=[O])[C][F]'))
species('781141280700000000001', '781141280700000000001.py', structure=SMILES('[O]=[C]=[C]([F])[F]'))
species('861382320600000000001', '861382320600000000001.py', structure=SMILES('[H][O][C]([F])([F])[F]'))
species('881242280000000000001', '881242280000000000001.py', structure=SMILES('[F][C]([F])([F])[F]'))
species('951592011700400000002', '951592011700400000002.py', structure=SMILES('[H][O][C](=[O])[C]([F])[F]'))

# ------------------------ transition state (uncomment if needed) -------------
transitionState('1642764945472630600001_r12_insertion_R_1_3_4', '1642764945472630600001_r12_insertion_R_1_3_4.py')
transitionState('1642764945472630600001_r12_insertion_R_1_3_8', '1642764945472630600001_r12_insertion_R_1_3_8.py')
transitionState('1642764945472630600001_r12_insertion_R_2_1_3', '1642764945472630600001_r12_insertion_R_2_1_3.py')
transitionState('1642764945472630600001_r12_insertion_R_3_1_10', '1642764945472630600001_r12_insertion_R_3_1_10.py')
transitionState('1642764945472630600001_r12_insertion_R_4_3_1', '1642764945472630600001_r12_insertion_R_4_3_1.py')
transitionState('1642764945472630600001_r12_insertion_R_5_4_3', '1642764945472630600001_r12_insertion_R_5_4_3.py')
transitionState('1642764945472630600001_r12_insertion_R_8_3_1', '1642764945472630600001_r12_insertion_R_8_3_1.py')
transitionState('1642764945472630600001_r12_insertion_R_8_3_4', '1642764945472630600001_r12_insertion_R_8_3_4.py')
transitionState('1642764945472630600001_r12_insertion_R_10_1_2', '1642764945472630600001_r12_insertion_R_10_1_2.py')
transitionState('1642764945472630600001_r12_insertion_R_10_1_3', '1642764945472630600001_r12_insertion_R_10_1_3.py')
transitionState('1642764945472630600001_r13_insertion_CO2_3_11', '1642764945472630600001_r13_insertion_CO2_3_11.py')
transitionState('1642764945472630600001_r13_insertion_ROR_4_3_1_2', '1642764945472630600001_r13_insertion_ROR_4_3_1_2.py')
transitionState('1642764945472630600001_r13_insertion_ROR_4_3_1_10', '1642764945472630600001_r13_insertion_ROR_4_3_1_10.py')
transitionState('1642764945472630600001_r13_insertion_ROR_11_10_1_2', '1642764945472630600001_r13_insertion_ROR_11_10_1_2.py')


# ------------------------ kinetics block  -----------------------------------
# Reaction definitions:
reaction(
    label          = '1642764945472630600001 <=> 1141903082400600000001 + 500620380000000000001',
    reactants      = ['1642764945472630600001'],
    products       = ['1141903082400600000001', '500620380000000000001'],
    transitionState= '1642764945472630600001_r12_insertion_R_1_3_4',
)

reaction(
    label          = '1642764945472630600001 <=> 1643046107386123120601',
    reactants      = ['1642764945472630600001'],
    products       = ['1643046107386123120601'],
    transitionState= '1642764945472630600001_r12_insertion_R_1_3_8',
)

reaction(
    label          = '1642764945472630600001 <=> 1642804744642041580601',
    reactants      = ['1642764945472630600001'],
    products       = ['1642804744642041580601'],
    transitionState= '1642764945472630600001_r12_insertion_R_2_1_3',
)

reaction(
    label          = '1642764945472630600001 <=> 1362244183860600000001 + 280280000000000000001',
    reactants      = ['1642764945472630600001'],
    products       = ['1362244183860600000001', '280280000000000000001'],
    transitionState= '1642764945472630600001_r12_insertion_R_3_1_10',
)

reaction(
    label          = '1642764945472630600001 <=> 1141903082400600000001 + 500620380000000000001',
    reactants      = ['1642764945472630600001'],
    products       = ['1141903082400600000001', '500620380000000000001'],
    transitionState= '1642764945472630600001_r12_insertion_R_4_3_1',
)

reaction(
    label          = '1642764945472630600001 <=> 1141903082400600000001 + 500620380000000000001',
    reactants      = ['1642764945472630600001'],
    products       = ['1141903082400600000001', '500620380000000000001'],
    transitionState= '1642764945472630600001_r12_insertion_R_5_4_3',
)

reaction(
    label          = '1642764945472630600001 <=> 1001482381140000000001 + 641041150370000000001',
    reactants      = ['1642764945472630600001'],
    products       = ['1001482381140000000001', '641041150370000000001'],
    transitionState= '1642764945472630600001_r12_insertion_R_8_3_1',
)

reaction(
    label          = '1642764945472630600001 <=> 761281321000200000001 + 881242280000000000001',
    reactants      = ['1642764945472630600001'],
    products       = ['761281321000200000001', '881242280000000000001'],
    transitionState= '1642764945472630600001_r12_insertion_R_8_3_4',
)



reaction(
    label          = '1642764945472630600001 <=> 1362244183860600000001 + 280280000000000000001',
    reactants      = ['1642764945472630600001'],
    products       = ['1362244183860600000001', '280280000000000000001'],
    transitionState= '1642764945472630600001_r12_insertion_R_10_1_3',
)

reaction(
    label          = '1642764945472630600001 <=> 1201923602880000000001 + 440560320000000000001',
    reactants      = ['1642764945472630600001'],
    products       = ['1201923602880000000001', '440560320000000000001'],
    transitionState= '1642764945472630600001_r13_insertion_CO2_3_11',
)

reaction(
    label          = '1642764945472630600001 <=> 1642804443153132880001',
    reactants      = ['1642764945472630600001'],
    products       = ['1642804443153132880001'],
    transitionState= '1642764945472630600001_r13_insertion_ROR_4_3_1_2',
)

reaction(
    label          = '1642764945472630600001 <=> 781141280700000000001 + 861382320600000000001',
    reactants      = ['1642764945472630600001'],
    products       = ['781141280700000000001', '861382320600000000001'],
    transitionState= '1642764945472630600001_r13_insertion_ROR_4_3_1_10',
)

reaction(
    label          = '1642764945472630600001 <=> 1642804664602161580601',
    reactants      = ['1642764945472630600001'],
    products       = ['1642804664602161580601'],
    transitionState= '1642764945472630600001_r13_insertion_ROR_11_10_1_2',
)




# ------------------------- high-P-limit kinetics fits ------------------------
kinetics(
    label = '1642764945472630600001 <=> 1141903082400600000001 + 500620380000000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

kinetics(
    label = '1642764945472630600001 <=> 1362244183860600000001 + 280280000000000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

kinetics(
    label = '1642764945472630600001 <=> 1141903082400600000001 + 500620380000000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

kinetics(
    label = '1642764945472630600001 <=> 1141903082400600000001 + 500620380000000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

kinetics(
    label = '1642764945472630600001 <=> 1001482381140000000001 + 641041150370000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

kinetics(
    label = '1642764945472630600001 <=> 761281321000200000001 + 881242280000000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

kinetics(
    label = '1642764945472630600001 <=> 1362244183860600000001 + 280280000000000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

kinetics(
    label = '1642764945472630600001 <=> 1201923602880000000001 + 440560320000000000001',
    Tmin  = (300,  'K'),
    Tmax  = (2000, 'K'),
    Tcount= 20,
)

kinetics(
    label = '1642764945472630600001 <=> 781141280700000000001 + 861382320600000000001',
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

statmech('1001482381140000000001')
thermo('1001482381140000000001', 'NASA')

statmech('1141903082400600000001')
thermo('1141903082400600000001', 'NASA')

statmech('1191793072280000000002')
thermo('1191793072280000000002', 'NASA')

statmech('1201923602880000000001')
thermo('1201923602880000000001', 'NASA')

statmech('1362244183860600000001')
thermo('1362244183860600000001', 'NASA')

statmech('1452453874401930400002')
thermo('1452453874401930400002', 'NASA')

statmech('1452453943632430600002')
thermo('1452453943632430600002', 'NASA')

statmech('1472314214191050000002')
thermo('1472314214191050000002', 'NASA')

statmech('1482484344321580600001')
thermo('1482484344321580600001', 'NASA')

statmech('160000000000000000003')
thermo('160000000000000000003', 'NASA')

statmech('1632594815172100000002')
thermo('1632594815172100000002', 'NASA')

statmech('1642764945472630600001')
thermo('1642764945472630600001', 'NASA')

statmech('1642804254293321740001')
thermo('1642804254293321740001', 'NASA')

statmech('1642804443153132880001')
thermo('1642804443153132880001', 'NASA')

statmech('1642804664602161580601')
thermo('1642804664602161580601', 'NASA')

statmech('1642804744642041580601')
thermo('1642804744642041580601', 'NASA')

statmech('1643046107386123120601')
thermo('1643046107386123120601', 'NASA')


statmech('170170000000000000002')
thermo('170170000000000000002', 'NASA')

statmech('190000000000000000002')
thermo('190000000000000000002', 'NASA')

statmech('280280000000000000001')
thermo('280280000000000000001', 'NASA')

statmech('440560320000000000001')
thermo('440560320000000000001', 'NASA')

statmech('450730450170000000002')
thermo('450730450170000000002', 'NASA')

statmech('500620380000000000001')
thermo('500620380000000000001', 'NASA')

statmech('641041150370000000001')
thermo('641041150370000000001', 'NASA')

statmech('690931140000000000002')
thermo('690931140000000000002', 'NASA')

statmech('761281321000200000001')
thermo('761281321000200000001', 'NASA')

statmech('781141280700000000001')
thermo('781141280700000000001', 'NASA')

statmech('861382320600000000001')
thermo('861382320600000000001', 'NASA')

statmech('881242280000000000001')
thermo('881242280000000000001', 'NASA')

statmech('951592011700400000002')
thermo('951592011700400000002', 'NASA')

statmech('1642764945472630600001_r12_insertion_R_1_3_4')
statmech('1642764945472630600001_r12_insertion_R_1_3_8')
statmech('1642764945472630600001_r12_insertion_R_2_1_3')
statmech('1642764945472630600001_r12_insertion_R_3_1_10')
statmech('1642764945472630600001_r12_insertion_R_4_3_1')
statmech('1642764945472630600001_r12_insertion_R_5_4_3')
statmech('1642764945472630600001_r12_insertion_R_8_3_1')
statmech('1642764945472630600001_r12_insertion_R_8_3_4')
statmech('1642764945472630600001_r12_insertion_R_10_1_2')
statmech('1642764945472630600001_r12_insertion_R_10_1_3')
statmech('1642764945472630600001_r13_insertion_CO2_3_11')
statmech('1642764945472630600001_r13_insertion_ROR_4_3_1_2')
statmech('1642764945472630600001_r13_insertion_ROR_4_3_1_10')
statmech('1642764945472630600001_r13_insertion_ROR_11_10_1_2')
statmech('1642764945472630600001_ketoenol_2_1_3_8')
