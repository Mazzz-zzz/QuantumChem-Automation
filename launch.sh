#!/bin/bash
#SBATCH --account="punim0131"
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
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
LABEL="CH3F-V1"
SMILES="CF"
CHARGE=0
MULTIPLICITY=1

# Generate Gaussian input files using the new command-line interface
python create_opt_jobs/generate_inputs.py --label "$LABEL" --smiles "$SMILES" --charge "$CHARGE" --multiplicity "$MULTIPLICITY"

# Optimise to create geom and freq files
for file in ./gaussian_jobs/*.gjf; do
    base=$(basename "$file" .gjf)
    log="./gaussian_jobs/${base}.log"
    chk="./gaussian_jobs/${base}.chk"

    #  Has this job terminated normally before?
    if [[ -f $log && -f $chk ]] && grep -q "Normal termination" "$log"; then
        echo "$base already completed -  skipping"
        continue
    fi
    
    echo "Processing $file..."
    g16 "$file"
    
    echo "Completed $file"
    echo "----------------------------------------"
done

# Run kinbot to search for reactions
#cd create_kinbot_jobs
#kinbot "$LABEL".json
#cd ..


#get all the kinbot output files
#

#conda activate kinbot-dev

conda activate prepackaged_rmg_env

# Run Arkane to create thermo file
cd create_arkane_jobs
python create_arkane_templates.py --species "$LABEL" --smiles "$SMILES" --output ../arkane_jobs
cd ..

cd arkane_jobs
Arkane.py input_$LABEL.py
cd ..
#

#Look at the thermo output in /thermo/ folder
#copy the thermo.py files to the database file
###tbd
#

#run RMG to find reactions
#cd rmg_jobs
#python create_rmg_jobs.py --species "$LABEL" --smiles "$SMILES" --log "$log_path" --output output_folder
#cd ..

#find rmg output smiles in /rmg_output/ folder
#

#loop around again and run the same process for each rmg output smiles
#






##DO NOT ADD/EDIT BEYOND THIS LINE##
##Job monitor command to list the resource usage
my-job-stats -a -n -s 