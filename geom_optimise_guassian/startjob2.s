#!/bin/bash
#SBATCH --account="punim0131"
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --time=2-00:00:00
#SBATCH --mem=20G
#SBATCH --partition=sapphire
#SBATCH --job-name=temp_reanalysis
#SBATCH --output=temp_reanalysis_%j.log

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

echo "--- Starting Temperature Reanalysis Jobs ---"
# Process only temperature-specific .gjf files
for file in *_*K.gjf; do
    # Skip if no files match
    [ -e "$file" ] || continue
    
    if [[ -f "$file" && "$file" =~ _[0-9]+K\.gjf$ ]]; then
        echo "Processing temperature reanalysis job: $file..."
        g16 "$file"
        
        # Check if the job completed successfully
        if [ $? -eq 0 ]; then
            echo "Successfully completed reanalysis job: $file"
        else
            echo "Error occurred while processing: $file"
            echo "Please check the output files for details"
        fi
        echo "----------------------------------------"
    fi
done

# Change back to original directory
cd "$WORK_DIR"

##DO NOT ADD/EDIT BEYOND THIS LINE##
##Job monitor command to list the resource usage
my-job-stats -a -n -s 