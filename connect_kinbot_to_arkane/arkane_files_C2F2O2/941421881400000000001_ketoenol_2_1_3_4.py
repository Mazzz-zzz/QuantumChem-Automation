#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Transition State template for Arkane calculations

# Multiplicity (default = doublet)
#spinMultiplicity = 2

# Geometry
geometry = GaussianLog('../../kinbot_jobs/C2F2O2-HIR/941421881400000000001_ketoenol_2_1_3_4.log')

# Energy
energy = {
    'CBS-QB3': Log('../../kinbot_jobs/C2F2O2-HIR/941421881400000000001_ketoenol_2_1_3_4.log'),
    'b97d-3/def2-msvp': GaussianLog('../../kinbot_jobs/C2F2O2-HIR/941421881400000000001_ketoenol_2_1_3_4.log'),
}

# Frequencies
frequencies = GaussianLog('../../kinbot_jobs/C2F2O2-HIR/941421881400000000001_ketoenol_2_1_3_4.log')


# Additional tunneling options (uncomment as needed)
# reaction.transitionState.tunneling = 'Eckart' 