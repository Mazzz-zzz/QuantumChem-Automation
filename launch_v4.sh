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
LABEL="CH3F-V1"
SMILES="CF"
CHARGE=0
MULTIPLICITY=1

# Generate Gaussian input files using the new command-line interface
python create_opt_jobs/generate_inputs.py --label "$LABEL" --smiles "$SMILES" --charge "$CHARGE" --multiplicity "$MULTIPLICITY"


set -uo pipefail          # safer bash but allow errors to continue
shopt -s nullglob          # ignore empty globs

# ── Loop over every geometry-only input ──────────────────────────────────────
for geom in ./gaussian_jobs/*_geom.gjf; do
    base=${geom%_geom.gjf}          # strip suffix → common stem
    geom_log=${base}_geom.log
    freq_inp=${base}_freq.gjf
    freq_log=${base}_freq.log

    ## 1  Geometry optimisation
    if [[ -f $geom_log ]] && grep -q "Normal termination" "$geom_log"; then
        echo "[✓] Geometry done for $base"
    else
        echo "[→] Running geometry for $base"
        g16 "$geom"
        if ! grep -q "Normal termination" "$geom_log"; then
            echo "[✗] Geometry failed for $base — skipping its freq step"
            echo "--------------------------------------------------------"
            continue
        fi
    fi

    ## 2  Frequency job (only if input exists)
    if [[ ! -f $freq_inp ]]; then
        echo "[!] No frequency input found for $base — skipping"
        echo "--------------------------------------------------------"
        continue
    fi

    if [[ -f $freq_log ]] && grep -q "Normal termination" "$freq_log"; then
        echo "[✓] Frequencies already done for $base"
    else
        echo "[→] Running frequency for $base"
        g16 "$freq_inp"
        grep -q "Normal termination" "$freq_log" \
            && echo "[✓] Frequency finished OK for $base" \
            || echo "[✗] Frequency failed for $base"
    fi

    echo "--------------------------------------------------------"
done



# Run kinbot to search for reactions
#cd create_kinbot_jobs
#kinbot "$LABEL".json
#cd ..


#get all the kinbot output files
#

#conda activate kinbot-dev

conda activate prepackaged_rmg_env

# Run Arkane to create thermo and 
cd create_arkane_jobs
python create_arkane_templates.py --species "$LABEL" --smiles "$SMILES" --output ../arkane_jobs
cd ..

#start Arkane
cd arkane_jobs
Arkane.py input_$LABEL.py
cd ..


#Look at the thermo output in /thermo/ folder, copy the thermo.py files to the database file
cp arkane_jobs/RMG_libraries/thermo.py /home/akhalilov/.conda/envs/prepackaged_rmg_env/share/rmgdatabase/thermo/libraries
echo "Thermo files copied to database"

# make RMG input file
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

# Create KinBot jobs from RMG output
echo "--------------------------------------------------------"
echo "Creating KinBot jobs from RMG output..."

# Create output directory for KinBot jobs
KINBOT_JOBS_DIR="kinbot_jobs_${LABEL}"
mkdir -p $KINBOT_JOBS_DIR

# Run the KinBot job creator script
cd create_kinbot_jobs
python create_kinbot_job.py
cd ..

conda activate kinbot-dev || echo "Failed to activate KinBot environment, but continuing..."

# Option 1: Automatically submit all KinBot jobs
echo "--------------------------------------------------------"
echo "Submitting KinBot jobs..."
cd kinbot_jobs
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

# Option 2: Just report the jobs are ready
# echo "--------------------------------------------------------"
# echo "KinBot jobs created in ${KINBOT_JOBS_DIR}"
# echo "To submit the jobs, run:"
# echo "cd ${KINBOT_JOBS_DIR}"
# echo "sbatch run_SPECIES_NAME.sh"

echo "--------------------------------------------------------"
echo "Workflow completed!"
echo "Check ${KINBOT_JOBS_DIR} for KinBot job results"

#find rmg output smiles in /rmg_output/ folder
#

#loop around again and run the same process for each rmg output smiles
#






##DO NOT ADD/EDIT BEYOND THIS LINE##
##Job monitor command to list the resource usage
my-job-stats -a -n -s 