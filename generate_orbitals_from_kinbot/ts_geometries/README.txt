Transition State Geometries
==========================

This directory contains transition state geometries extracted from IRC calculations.
Each reaction has its own subfolder containing:
  - Gaussian input file (.gjf) for orbital calculations
  - XYZ file for visualization

Total reactions processed: 13
Total transition states extracted: 13

To run calculations on all transition states:
  $ sbatch submit_gaussian_calculations.sh ./ts_geometries
