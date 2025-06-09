#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Species template for Arkane calculations

# Multiplicity
#spinMultiplicity = 1

# Geometry
geometry = GaussianLog('../../kinbot_jobs/PFPra-M062X/280280000000000000001_well.log')

# Energy
energy = {
    'CBS-QB3': Log('../../kinbot_jobs/PFPra-M062X/280280000000000000001_well.log'),
    #'b97d-3/def2-msvp': -39.741993184, #GaussianLog('CH3F_freq.log'),
    'b97d-3/def2-msvp': GaussianLog('../../kinbot_jobs/PFPra-M062X/280280000000000000001_well.log'),
}

# Frequencies
frequencies = GaussianLog('../../kinbot_jobs/PFPra-M062X/280280000000000000001_well.log')

# Rotors (placeholder)
rotors = [],

# Additional settings (optional)
# Use for more complex molecules with symmetry
# symmetryNumber = 1
