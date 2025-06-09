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


set -uo pipefail          # safer bash but allow errors to continue
shopt -s nullglob          # ignore empty globs


#activate env for arkane and rmg
conda activate prepackaged_rmg_env

# Call create_arkane_v2.py with folder parameter ($LABEL) and output parameter
cd AUTOMATION-CENTER/connect_kinbot_to_arkane
python create_arkane_v2.py "$LABEL" --output "arkane_files-${LABEL}"

#start Arkane
cd arkane_files-${LABEL}
Arkane.py input.py

cd RMG_libraries

#copy thermo.py files to database
cp thermo.py /home/akhalilov/.conda/envs/prepackaged_rmg_env/share/rmgdatabase/thermo/libraries
echo "Thermo files copied to database"

#copy reactions.py files to database
cp reactions.py /home/akhalilov/.conda/envs/prepackaged_rmg_env/share/rmgdatabase/kinetics/libraries
echo "reactions files copied to database"


# ------------------------------------------------------------
#make RMG input file
cd create_rmg_jobs
python create_rmg_jobs.py --species "$LABEL" --smiles "$SMILES" --output ../rmg_jobs
cd ..

#run RMG to find reactions
cd rmg_jobs
# Use set +e to temporarily disable error checking for the RMG run
set +e
rmg.py rmg_input_$LABEL.py
RMG_STATUS=$?
set -uo pipefail  # Re-enable error checking
if [ $RMG_STATUS -ne 0 ]; then
    echo "RMG calculation failed with status $RMG_STATUS, but continuing with workflow..."
fi
cd ..

# Check if the chemkin file was created
CHEMKIN_FILE="rmg_jobs/chemkin/chem_annotated.inp"
if [ -f "$CHEMKIN_FILE" ]; then
    echo "Chemkin file found: $CHEMKIN_FILE"
else
    echo "Warning: Chemkin file not found."
fi





##DO NOT ADD/EDIT BEYOND THIS LINE##
##Job monitor command to list the resource usage