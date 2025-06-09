#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Transition State template for Arkane calculations

# Multiplicity (default = doublet)
#spinMultiplicity = 2

# Geometry
geometry = GaussianLog('../../kinbot_jobs/PFPra-M062X/1642764945472630600001_r13_insertion_ROR_11_10_1_2.log')

# Energy
energy = {
    'CBS-QB3': Log('../../kinbot_jobs/PFPra-M062X/1642764945472630600001_r13_insertion_ROR_11_10_1_2.log'),
    'b97d-3/def2-msvp': GaussianLog('../../kinbot_jobs/PFPra-M062X/1642764945472630600001_r13_insertion_ROR_11_10_1_2.log'),
}

# Frequencies
frequencies = GaussianLog('../../kinbot_jobs/PFPra-M062X/1642764945472630600001_r13_insertion_ROR_11_10_1_2.log')


# Additional tunneling options (uncomment as needed)
# reaction.transitionState.tunneling = 'Eckart' 