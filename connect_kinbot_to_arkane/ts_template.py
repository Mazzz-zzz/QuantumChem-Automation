#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Transition State template for Arkane calculations

# Multiplicity (default = doublet)
#spinMultiplicity = 2

# Geometry
geometry = GaussianLog('../../kinbot_jobs/{folder}/{ts}.log')

# Energy
energy = {
    'CBS-QB3': Log('../../kinbot_jobs/{folder}/{ts}.log'),
    'b97d-3/def2-msvp': GaussianLog('../../kinbot_jobs/{folder}/{ts}.log'),
}

# Frequencies
frequencies = GaussianLog('../../kinbot_jobs/{folder}/{ts}.log')


# Additional tunneling options (uncomment as needed)
# reaction.transitionState.tunneling = 'Eckart' 