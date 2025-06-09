#!/usr/bin/env python
# -*- coding: utf-8 -*-
spinMultiplicity = 1

geometry = GaussianLog('../gaussian_jobs/C2F5SO3H_geom.log')

energy = {
    'CBS-QB3': Log('../gaussian_jobs/C2F5SO3H_freq.log'),
    #'b97d-3/def2-msvp': -39.741993184, #GaussianLog('CH3F_freq.log'),
    'b97d-3/def2-msvp': GaussianLog('../gaussian_jobs/C2F5SO3H_geom.log'),
   
}

frequencies = GaussianLog('../gaussian_jobs/C2F5SO3H_freq.log')

rotors = [],
