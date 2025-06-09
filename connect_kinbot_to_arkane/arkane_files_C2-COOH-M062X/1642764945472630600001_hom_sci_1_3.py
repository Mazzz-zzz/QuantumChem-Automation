#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Transition State template for Arkane calculations

# Multiplicity (default = doublet)
#spinMultiplicity = 2

# Geometry
geometry = GaussianLog('../../kinbot_jobs/CF3COOH-M062X/1642764945472630600001_hom_sci_1_3.log')

# Energy
energy = {
    'CBS-QB3': Log('../../kinbot_jobs/CF3COOH-M062X/1642764945472630600001_hom_sci_1_3.log'),
    'b97d-3/def2-msvp': GaussianLog('../../kinbot_jobs/CF3COOH-M062X/1642764945472630600001_hom_sci_1_3.log'),
}

# Frequencies
frequencies = GaussianLog('../../kinbot_jobs/CF3COOH-M062X/1642764945472630600001_hom_sci_1_3.log')


# Additional tunneling options (uncomment as needed)
# reaction.transitionState.tunneling = 'Eckart' 