#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Transition State template for Arkane calculations

# Multiplicity (default = doublet)
#spinMultiplicity = 2

# Geometry
geometry = GaussianLog('../../kinbot_jobs/C2F5SO3H-M062X/2003846667223680600001_r13_insertion_ROR_1_2_5_6.log')

# Energy
energy = {
    'CBS-QB3': Log('../../kinbot_jobs/C2F5SO3H-M062X/2003846667223680600001_r13_insertion_ROR_1_2_5_6.log'),
    'b97d-3/def2-msvp': GaussianLog('../../kinbot_jobs/C2F5SO3H-M062X/2003846667223680600001_r13_insertion_ROR_1_2_5_6.log'),
}

# Frequencies
frequencies = GaussianLog('../../kinbot_jobs/C2F5SO3H-M062X/2003846667223680600001_r13_insertion_ROR_1_2_5_6.log')


# Additional tunneling options (uncomment as needed)
# reaction.transitionState.tunneling = 'Eckart' 