# KinBot Job Creator

This script automates the creation of KinBot job configurations based on RMG mechanism flux analysis. It identifies the species with the highest fluxes in a chemical mechanism and prepares input files for KinBot to analyze their reaction pathways.

## Requirements

- Python 3.6+
- RDKit
- Cantera
- Pandas
- NumPy

## Installation

Ensure you have the required packages installed:

```bash
conda activate kinbot-dev  # Or your preferred environment
pip install cantera pandas numpy rdkit
```

## Usage

```bash
python create_kinbot_job.py --mechanism path/to/mechanism.yaml [options]
```

### Command Line Arguments

- `--mechanism`: Path to chemical mechanism file (Chemkin .inp or Cantera .yaml)
- `--thermo`: Path to thermo file (if using Chemkin format)
- `--species`: Path to species dictionary (if using Chemkin format)
- `--template`: Template KinBot job file (default: CH3F-V1.json)
- `--smiles`: SMILES string of the target species
- `--temperature`: Simulation temperature in K (default: 900)
- `--pressure`: Simulation pressure in Pa (default: 1e5)
- `--time`: Simulation time in seconds (default: 0.5)
- `--top`: Number of top flux species to generate jobs for (default: 5)
- `--output_dir`: Output directory for job files (default: kinbot_jobs)

### Example

Converting a Chemkin mechanism to analyze fluxes and generate KinBot jobs:

```bash
python create_kinbot_job.py \
  --mechanism path/to/chem.inp \
  --thermo path/to/thermo.dat \
  --species path/to/species_dictionary.txt \
  --smiles "CH3F-V1:1" \
  --temperature 900 \
  --pressure 101325 \
  --time 0.5 \
  --top 10 \
  --output_dir kinbot_jobs_ch3f
```

If you already have a Cantera yaml mechanism:

```bash
python create_kinbot_job.py \
  --mechanism path/to/chem.yaml \
  --smiles "CH3F-V1:1" \
  --top 10
```

## Understanding RMG Flux Analysis

The script uses the approach described in the RMG flux analysis guide:

1. Loads your mechanism into Cantera
2. Sets initial conditions (temperature, pressure, composition)
3. Runs a simulation to steady state
4. Analyzes species net production rates
5. Ranks species by absolute flux values
6. Creates KinBot jobs for the top N species

This approach allows you to:
- Find the most important species in your mechanism
- Identify species worth investigating with KinBot
- Automate the creation of KinBot job files

## Running KinBot Jobs

After generating job files:

```bash
cd kinbot_jobs
sbatch run_SPECIES_NAME.sh
```

## Notes

- The `get_smiles_from_species_name()` function needs customization for your specific species dictionary format
- 3D structure generation uses RDKit's ETKDG algorithm
- Custom templates can be provided to change KinBot parameters 