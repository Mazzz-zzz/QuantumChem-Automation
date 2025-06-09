#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Transition State template for Arkane calculations

# Multiplicity (default = doublet)
#spinMultiplicity = 2

# Geometry
geometry = GaussianLog('../../kinbot_jobs/C2F5SO3H-M062X/2003846667223680600001_r12_insertion_R_6_5_7.log')

# Energy
energy = {
    'CBS-QB3': Log('../../kinbot_jobs/C2F5SO3H-M062X/2003846667223680600001_r12_insertion_R_6_5_7.log'),
    'b97d-3/def2-msvp': GaussianLog('../../kinbot_jobs/C2F5SO3H-M062X/2003846667223680600001_r12_insertion_R_6_5_7.log'),
}

# Frequencies
frequencies = GaussianLog('../../kinbot_jobs/C2F5SO3H-M062X/2003846667223680600001_r12_insertion_R_6_5_7.log')


# Additional tunneling options (uncomment as needed)
# reaction.transitionState.tunneling = 'Eckart' 