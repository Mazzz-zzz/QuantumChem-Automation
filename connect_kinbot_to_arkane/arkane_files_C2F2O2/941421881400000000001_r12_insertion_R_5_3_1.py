#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Transition State template for Arkane calculations

# Multiplicity (default = doublet)
#spinMultiplicity = 2

# Geometry
geometry = GaussianLog('../../kinbot_jobs/C2F2O2-HIR/941421881400000000001_r12_insertion_R_5_3_1.log')

# Energy
energy = {
    'CBS-QB3': Log('../../kinbot_jobs/C2F2O2-HIR/941421881400000000001_r12_insertion_R_5_3_1.log'),
    'b97d-3/def2-msvp': GaussianLog('../../kinbot_jobs/C2F2O2-HIR/941421881400000000001_r12_insertion_R_5_3_1.log'),
}

# Frequencies
frequencies = GaussianLog('../../kinbot_jobs/C2F2O2-HIR/941421881400000000001_r12_insertion_R_5_3_1.log')


# Additional tunneling options (uncomment as needed)
# reaction.transitionState.tunneling = 'Eckart' 