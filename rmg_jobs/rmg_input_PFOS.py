# Data sources
database(
    thermoLibraries = ['primaryThermoLibrary', 'fluorine', 'thermo'],
    reactionLibraries = [],
    seedMechanisms = [],
    kineticsDepositories = ['training'],
    kineticsFamilies = 'default',
    kineticsEstimator = 'rate rules',
)

# List of species
species(
    label='PFOS',
    reactive=True,
    structure=SMILES("C(C(C(C(C(F)(F)S(=O)(=O)O)(F)F)(F)F)(F)F)(C(C(C(F)(F)F)(F)F)(F)F)(F)F"),
)

# Reaction systems
simpleReactor(
    temperature=(1350,'K'),
    pressure=(1.0,'bar'),
    initialMoleFractions={
        "PFOS": 1.0,
    },
    terminationConversion={
        "PFOS": 0.7,
    },
    terminationTime=(1e6,'s'),
)

simulator(
    atol=1e-16,
    rtol=1e-8,
)

model(
    toleranceKeepInEdge=0.0,
    toleranceMoveToCore=0.1,
    toleranceInterruptSimulation=0.1,
    maximumEdgeSpecies=100000,
    filterReactions=True,
)

options(
    units='si',
    generateOutputHTML=True,
    generatePlots=True,
    saveEdgeSpecies=True,
    saveSimulationProfiles=True,
) 