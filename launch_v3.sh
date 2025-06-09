#!/bin/bash
#SBATCH --account="punim0131"
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=3-00:00:00
#SBATCH --mem=8G
#SBATCH --partition=sapphire
#SBATCH --job-name=my_automation_center
#SBATCH --output=automation_center_%j.log
#SBATCH --error=automation_center_%j.err

# Load required modules
module purge
module load NVHPC/22.11-CUDA-11.7.0
module load Gaussian/g16c01-CUDA-11.7.0
module load Python/3.10.4
module load Anaconda3/2024.02-1

# Initialize conda
eval "$(conda shell.bash hook)"

# Activate KinBot environment
conda activate kinbot-dev


### --- Stage 1: Convert SMILES to optimized geometry
# Define molecule parameters
LABEL="CF3COOH-NEW"
SMILES="C(=O)(C(F)(F)F)O"
CHARGE=0
MULTIPLICITY=1



# For V3, we want to run kinbot now.
# Create KinBot jobs from SMILES
echo "--------------------------------------------------------"
echo "Creating KinBot job from SMILES"

# Create output directory for KinBot jobs
KINBOT_JOBS_DIR="kinbot_jobs_${LABEL}"
mkdir -p $KINBOT_JOBS_DIR

# Run the KinBot job creator script with SMILES
cd create_kinbot_jobs
python create_kinbot_job_from_smiles.py --smiles "$SMILES" --output_dir "../$KINBOT_JOBS_DIR" --multiplicity "$MULTIPLICITY"
cd ..


# Option 1: Automatically submit all KinBot jobs
echo "--------------------------------------------------------"
echo "Submitting KinBot jobs..."
cd $KINBOT_JOBS_DIR
for dir in */; do
  if [ -d "$dir" ]; then
    echo "Entering directory $dir..."
    cd "$dir"
    for script in run_*.sh; do
      if [ -f "$script" ]; then
        echo "Submitting $script..."
        sbatch "$script"
      fi
    done
    cd ..
  fi
done
cd ..

my-job-stats -a -n -s 