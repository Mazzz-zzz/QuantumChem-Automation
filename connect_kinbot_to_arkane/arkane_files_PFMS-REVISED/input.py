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
species('1002122340540000000001', '1002122340540000000001.py', structure=SMILES('[H][O][S](=[O])(=[O])[F]'))
species('1302784824321400000001', '1302784824321400000001.py', structure=SMILES('[O][S]([O])(=[O])=[C]([F])[F]'))
species('1312673532570400000002', '1312673532570400000002.py', structure=SMILES('[H][O][S]([O])(=[O])=[C]([F])[F]'))
species('1332333552100000000002', '1332333552100000000002.py', structure=SMILES('[O]=[S](=[O])[C]([F])([F])[F]'))
species('1342503882400600000001', '1342503882400600000001.py', structure=SMILES('[H][O][S](=[O])[C]([F])([F])[F]'))
species('1492814473150000000002', '1492814473150000000002.py', structure=SMILES('[O][S](=[O])(=[O])[C]([F])([F])[F]'))
species('1502984803620600000001', '1502984803620600000001.py', structure=SMILES('[H][O][S](=[O])(=[O])[C]([F])([F])[F]'))
species('1503305764823040000001', '1503305764823040000001.py', structure=SMILES('[H][O][S]1([C]([F])([F])[F])[O][O]1'))
species('160000000000000000003', '160000000000000000003.py', structure=SMILES('[C]'))
species('170170000000000000002', '170170000000000000002.py', structure=SMILES('[H][O]'))
species('190000000000000000002', '190000000000000000002.py', structure=SMILES('[F]'))
species('200200000000000000001', '200200000000000000001.py', structure=SMILES('[H][F]'))
species('500620380000000000001', '500620380000000000001.py', structure=SMILES('[F][C][F]'))
species('690931140000000000002', '690931140000000000002.py', structure=SMILES('[F][C]([F])[F]'))
species('811611290340000000002', '811611290340000000002.py', structure=SMILES('[H][O][S](=[O])=[O]'))

# ------------------------ transition state (uncomment if needed) -------------
# No transition states found. Add any manually if needed.

# ------------------------ kinetics block  -----------------------------------
# Example of reaction definition:
# reaction(
#     label          = '{species} <=> Product1 + Product2',
#     reactants      = ['{species}'],
#     products       = ['Product1', 'Product2'],
#     transitionState= 'TS_example',
# )

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

statmech('1002122340540000000001')
thermo('1002122340540000000001', 'NASA')

statmech('1302784824321400000001')
thermo('1302784824321400000001', 'NASA')

statmech('1312673532570400000002')
thermo('1312673532570400000002', 'NASA')

statmech('1332333552100000000002')
thermo('1332333552100000000002', 'NASA')

statmech('1342503882400600000001')
thermo('1342503882400600000001', 'NASA')

statmech('1492814473150000000002')
thermo('1492814473150000000002', 'NASA')

statmech('1502984803620600000001')
thermo('1502984803620600000001', 'NASA')

statmech('1503305764823040000001')
thermo('1503305764823040000001', 'NASA')

statmech('160000000000000000003')
thermo('160000000000000000003', 'NASA')

statmech('170170000000000000002')
thermo('170170000000000000002', 'NASA')

statmech('190000000000000000002')
thermo('190000000000000000002', 'NASA')

statmech('200200000000000000001')
thermo('200200000000000000001', 'NASA')

statmech('500620380000000000001')
thermo('500620380000000000001', 'NASA')

statmech('690931140000000000002')
thermo('690931140000000000002', 'NASA')

statmech('811611290340000000002')
thermo('811611290340000000002', 'NASA')

