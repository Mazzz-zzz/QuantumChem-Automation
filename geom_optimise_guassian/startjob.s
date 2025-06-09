#!/bin/bash
#SBATCH --account="punim0131"
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=2-00:00:00
#SBATCH --mem=5G
#SBATCH --partition=sapphire
#SBATCH --job-name=marshal_paper_opt
#SBATCH --output=marshal_paper_opt_%j.log

module purge
module load NVHPC/22.11-CUDA-11.7.0
module load Gaussian/g16c01-CUDA-11.7.0

export GAUSS_PDEF=${SLURM_CPUS_PER_TASK}

# Get absolute path to gaussian_projects
WORK_DIR="$(pwd)"
GAUSSIAN_DIR="${WORK_DIR}/gaussian_projects"

# Ensure the projects directory exists
mkdir -p "$GAUSSIAN_DIR"

# Change to the gaussian_projects directory
cd "$GAUSSIAN_DIR"

echo "--- Starting Main Optimization/Frequency Jobs ---"
# First loop: Process main .gjf files (no _<temp>K suffix)
for file in *.gjf; do
    # Skip if no files match
    [ -e "$file" ] || continue
    
    # Check if the filename does NOT contain the pattern _<digits>K.gjf
    if [[ ! "$file" =~ _[0-9]+K\.gjf$ ]]; then
        echo "Processing main job: $file..."
        # Run gaussian from the gaussian_projects directory
        g16 "$file"
        
        # Extract basename without extension
        basename=$(basename "$file" .gjf)
        
        # Generate formatted checkpoint file immediately after main job
        if [ -f "${basename}.chk" ]; then
            echo "Generating formatted checkpoint file for $basename..."
            formchk "${basename}.chk" "${basename}.fchk"
        else
            echo "Warning: Checkpoint file ${basename}.chk not found. Skipping formchk."
        fi
        
        echo "Completed main job: $file"
        echo "----------------------------------------"
    fi
done

echo "--- Starting Reanalysis Jobs ---"
# Second loop: Process reanalysis .gjf files (with _<temp>K suffix)
for file in *_*K.gjf; do
    # Skip if no files match
    [ -e "$file" ] || continue
    
    if [[ -f "$file" && "$file" =~ _[0-9]+K\.gjf$ ]]; then
        echo "Processing reanalysis job: $file..."
        g16 "$file"
        echo "Completed reanalysis job: $file"
        echo "----------------------------------------"
    fi
done

# Change back to original directory
cd "$WORK_DIR"

##DO NOT ADD/EDIT BEYOND THIS LINE##
##Job monitor command to list the resource usage
my-job-stats -a -n -s