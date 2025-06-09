#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Transition State template for Arkane calculations

# Multiplicity (default = doublet)
#spinMultiplicity = 2

# Geometry
geometry = GaussianLog('../../kinbot_jobs/CF3COOH-HIR/1141903082400600000001_r13_insertion_CO2_3_8.log')

# Energy
energy = {
    'CBS-QB3': Log('../../kinbot_jobs/CF3COOH-HIR/1141903082400600000001_r13_insertion_CO2_3_8.log'),
    'b97d-3/def2-msvp': GaussianLog('../../kinbot_jobs/CF3COOH-HIR/1141903082400600000001_r13_insertion_CO2_3_8.log'),
}

# Frequencies
frequencies = GaussianLog('../../kinbot_jobs/CF3COOH-HIR/1141903082400600000001_r13_insertion_CO2_3_8.log')


# Additional tunneling options (uncomment as needed)
# reaction.transitionState.tunneling = 'Eckart' 