# AUTOMATION-CENTER

An automated computational chemistry workflow system for molecular reaction network exploration using Gaussian, RMG, Arkane, and KinBot.

## Overview

The AUTOMATION-CENTER provides automated workflows for computational chemistry calculations, starting from simple SMILES strings and progressing through geometry optimization, thermodynamic calculations, reaction network generation, and kinetic analysis. This system integrates multiple computational chemistry tools to provide a comprehensive analysis pipeline.

## Available Workflows

### `launch_v3.sh` - Direct KinBot Workflow
A streamlined workflow that creates KinBot jobs directly from SMILES strings.

**What it does:**
1. Takes a SMILES string as input
2. Creates KinBot job configurations
3. Automatically submits all KinBot jobs to the SLURM queue
4. Monitors job statistics

**Use cases:**
- Quick reaction exploration for known molecules
- When you already have optimized geometries or don't need Gaussian calculations
- Rapid screening of reaction pathways

### `launch_v4.sh` - Comprehensive Multi-Tool Workflow
A complete computational chemistry pipeline that integrates multiple tools.

**What it does:**
1. **Gaussian Calculations**: Generates and runs geometry optimization and frequency calculations
2. **Arkane Analysis**: Creates thermodynamic data and kinetic parameters
3. **RMG Integration**: Generates reaction networks and copies thermodynamic data to RMG database
4. **KinBot Exploration**: Creates and submits KinBot jobs based on RMG output
5. **Database Updates**: Automatically updates local RMG databases with calculated data

**Use cases:**
- Complete characterization of new molecules
- When you need accurate thermodynamic and kinetic data
- Building comprehensive reaction mechanisms
- Research-grade calculations with full traceability

## Prerequisites

### Software Requirements
- **Gaussian 16** (g16c01-CUDA-11.7.0)
- **Python 3.10.4**
- **Anaconda3/2024.02-1**
- **NVHPC/22.11-CUDA-11.7.0**

### Conda Environments
- `kinbot-dev`: For KinBot calculations
- `prepackaged_rmg_env`: For RMG and Arkane calculations

### SLURM Configuration
Both scripts are configured for:
- Account: `punim0131`
- Partition: `sapphire`
- Resources: 1 node, 2 CPUs, 8GB RAM
- Time limit: 3 days

## Usage

### Basic Setup
1. Edit the molecule parameters in the chosen launch script:
   ```bash
   LABEL="your_molecule_name"
   SMILES="your_smiles_string"
   CHARGE=0
   MULTIPLICITY=1
   ```

2. Submit the job:
   ```bash
   sbatch launch_v3.sh  # For simple workflow
   # OR
   sbatch launch_v4.sh  # For comprehensive workflow
   ```

### Expected Outputs

#### launch_v3.sh outputs:
- `kinbot_jobs_${LABEL}/`: Directory containing KinBot job files
- Individual KinBot calculation directories
- SLURM job logs: `automation_center_*.log` and `automation_center_*.err`

#### launch_v4.sh outputs:
- `gaussian_jobs/`: Gaussian input and output files
- `arkane_jobs/`: Arkane input files and thermodynamic calculations
- `rmg_jobs/`: RMG input files and reaction network output
- `kinbot_jobs/`: KinBot job directories
- Updated RMG database files

## Directory Structure

```
AUTOMATION-CENTER/
├── create_opt_jobs/          # Gaussian input generation
├── create_arkane_jobs/       # Arkane template creation
├── create_rmg_jobs/         # RMG input file generation
├── create_kinbot_jobs/      # KinBot job creation
├── gaussian_jobs/           # Gaussian calculations (generated)
├── arkane_jobs/            # Arkane calculations (generated)
├── rmg_jobs/               # RMG calculations (generated)
├── kinbot_jobs/            # KinBot calculations (generated)
├── launch_v3.sh            # Simple workflow script
├── launch_v4.sh            # Comprehensive workflow script
└── README.md               # This file
```

## Monitoring and Troubleshooting

### Job Monitoring
Both scripts include `my-job-stats -a -n -s` for monitoring resource usage and job status.

### Common Issues
1. **Environment activation failures**: Ensure conda environments are properly installed
2. **Module loading errors**: Check that all required modules are available on your system
3. **Gaussian failures**: Check `.log` files for convergence issues
4. **RMG errors**: The v4 script continues even if RMG fails (non-critical for some workflows)

### Log Files
- Main workflow logs: `automation_center_*.log` and `automation_center_*.err`
- Gaussian logs: `gaussian_jobs/*_geom.log` and `gaussian_jobs/*_freq.log`
- Individual tool outputs in their respective directories

## Examples

### Example 1: Simple molecule exploration (v3)
```bash
# Edit launch_v3.sh
LABEL="methanol"
SMILES="CO"
CHARGE=0
MULTIPLICITY=1

# Submit
sbatch launch_v3.sh
```

### Example 2: Complete analysis (v4)
```bash
# Edit launch_v4.sh
LABEL="trifluoroacetic_acid"
SMILES="C(=O)(C(F)(F)F)O"
CHARGE=0
MULTIPLICITY=1

# Submit
sbatch launch_v4.sh
```

## Contributing

When modifying the workflows:
1. Test changes on small molecules first
2. Update this README if you change functionality
3. Maintain backward compatibility where possible
4. Document any new dependencies or requirements

## Support

For issues with:
- **Gaussian calculations**: Check Gaussian documentation and convergence criteria
- **RMG/Arkane**: Consult RMG-Py documentation
- **KinBot**: Refer to KinBot documentation
- **SLURM issues**: Contact your cluster administrator
