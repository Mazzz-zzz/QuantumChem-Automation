#!/bin/bash
#SBATCH --account="punim0131"
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=24:00:00
#SBATCH --mem=8G
#SBATCH --partition=sapphire
#SBATCH --job-name=IRC_orbitals
#SBATCH --output=IRC_orbitals_%j.log

# Help message
usage() {
    echo "Usage: $0 [OPTIONS] [INPUT_DIR]"
    echo "Run orbital calculations on geometries extracted from IRC paths"
    echo
    echo "Options:"
    echo "  -t, --time HOURS      Set time limit in hours (default: 24)"
    echo "  -m, --memory GB       Set memory limit in GB (default: 8)"
    echo "  -o, --output DIR      Set output directory for calculations (default: ./orbital_results)"
    echo "  -i, --input DIR       Set input directory with Gaussian input files (default: ./orbital_inputs)"
    echo "  -s, --static DIR      Include static frames (reactants, TS, products) from DIR (default: ./static_orbital_results)"
    echo "  --no-static           Skip processing of static frames"
    echo "  -h, --help            Show this help message"
    echo
    echo "If no INPUT_DIR is specified, the default ./orbital_inputs will be used."
    echo
    exit 1
}

# Default directories and settings
INPUT_DIR="./orbital_inputs"
STATIC_DIR="./static_orbital_results"
OUTPUT_DIR="./orbital_results"
TIME_LIMIT="24:00:00"
MEMORY="8G"
PROCESS_STATIC=true

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--time)
            TIME_LIMIT="$2:00:00"
            shift 2
            ;;
        -m|--memory)
            MEMORY="${6}G"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -i|--input)
            INPUT_DIR="$2"
            shift 2
            ;;
        -s|--static)
            STATIC_DIR="$2"
            shift 2
            ;;
        --no-static)
            PROCESS_STATIC=false
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            # If an argument is provided without a flag, assume it's the input directory
            INPUT_DIR="$1"
            shift
            ;;
    esac
done

# Check that input directory exists
if [ ! -d "$INPUT_DIR" ]; then
    echo "ERROR: Input directory does not exist: $INPUT_DIR"
    echo "Please run the irc_to_orbitals.py script first to create input files,"
    echo "or specify a different input directory with the --input flag."
    exit 1
fi

# Check for static directory if processing static files
if $PROCESS_STATIC; then
    if [ ! -d "$STATIC_DIR" ]; then
        echo "WARNING: Static frames directory does not exist: $STATIC_DIR"
        echo "Will skip processing static frames."
        PROCESS_STATIC=false
    fi
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Load required modules
module purge
module load NVHPC/22.11-CUDA-11.7.0
module load Gaussian/g16c01-CUDA-11.7.0

export GAUSS_PDEF=4

echo "Starting orbital calculations"
echo "Input directory: $INPUT_DIR"
if $PROCESS_STATIC; then
    echo "Static frames directory: $STATIC_DIR"
fi
echo "Output directory: $OUTPUT_DIR"
echo "------------------------------------------------"

# Function to check for existing calculations
check_existing_calc() {
    local log_file="$1"
    local base_name="$2"
    
    if [ -f "$log_file" ]; then
        echo "  - Calculation already exists: $log_file"
        return 0
    else
        echo "  - Setting up calculation for: $base_name"
        return 1
    fi
}

# Function to process a set of Gaussian input files
process_gjf_files() {
    local input_base_dir="$1"
    local file_type="$2"
    local counter=0
    local success=0
    local failed=0
    local skipped=0
    
    # Get a sorted list of all input files
    mapfile -t GJF_FILES < <(find "$input_base_dir" -name "*.gjf" | sort)
    local gjf_count=${#GJF_FILES[@]}
    
    if [ "$gjf_count" -eq 0 ]; then
        echo "No .gjf files found in $input_base_dir"
        return
    fi
    
    echo "Found $gjf_count Gaussian input files to process in $file_type"
    echo "------------------------------------------------"
    
    for gjf_file in "${GJF_FILES[@]}"; do
        counter=$((counter + 1))
        
        # Get base name and directory
        base_name=$(basename "$gjf_file" .gjf)
        input_dir=$(dirname "$gjf_file")
        
        # Extract molecule and reaction type from directory structure
        rel_path=${input_dir#$input_base_dir/}
        molecule=$(echo "$rel_path" | cut -d '/' -f1)
        reaction_type=$(echo "$rel_path" | cut -d '/' -f2)
        
        # Create corresponding output directory - ensure it exists
        output_subdir="$OUTPUT_DIR/$molecule/$reaction_type"
        mkdir -p "$output_subdir"
        
        # Output files
        log_file="$output_subdir/${base_name}.log"
        
        echo "[$counter/$gjf_count] Processing $file_type: $base_name"
        echo "  - Input file: $gjf_file"
        echo "  - Output directory: $output_subdir"
        
        # Check if calculation already exists
        if ! check_existing_calc "$log_file" "$base_name"; then
            # Verify input file exists
            if [ ! -f "$gjf_file" ]; then
                echo "  ✗ ERROR: Input file does not exist: $gjf_file"
                failed=$((failed + 1))
                echo "------------------------------------------------"
                continue
            fi
            
            # Copy input file to output directory
            cp "$gjf_file" "$output_subdir/"
            
            # Run Gaussian calculation
            echo "  - Running Gaussian calculation..."
            
            # Ensure we're in the output directory before running Gaussian
            if ! cd "$output_subdir"; then
                echo "  ✗ ERROR: Cannot change to output directory: $output_subdir"
                failed=$((failed + 1))
                echo "------------------------------------------------"
                continue
            fi
            
            # Run Gaussian and capture output
            g16 "${base_name}.gjf" > "${base_name}_g16.out" 2>&1
            G16_STATUS=$?
            
            # Check if calculation succeeded
            if [ $G16_STATUS -eq 0 ]; then
                echo "  - Gaussian calculation completed successfully"
                
                # Generate cube files
                if [ -f "${base_name}.chk" ]; then
                    echo "  - Generating formatted checkpoint and cube files"
                    formchk "${base_name}.chk"
                    cubegen 0 MO=HOMO "${base_name}.fchk" "${base_name}_homo.cube" 80 h
                    cubegen 0 MO=LUMO "${base_name}.fchk" "${base_name}_lumo.cube" 80 h
                    cubegen 0 density "${base_name}.fchk" "${base_name}_density.cube" 80 h
                    ## Adding potential too!
                    cubegen 0 Potential=scf "${base_name}.fchk" "${base_name}_pot.cube" 80 h
                    echo "  ✓ Successfully created cube files"
                    success=$((success + 1))
                else
                    echo "  ✗ ERROR: Checkpoint file not found"
                    failed=$((failed + 1))
                fi
            else
                echo "  ✗ ERROR: Gaussian calculation failed with status $G16_STATUS"
                echo "  - See ${output_subdir}/${base_name}_g16.out for details"
                failed=$((failed + 1))
            fi
            
            # Return to original directory
            cd "$SLURM_SUBMIT_DIR" || cd /tmp
        else
            skipped=$((skipped + 1))
        fi
        
        echo "------------------------------------------------"
    done
    
    echo "$file_type calculation summary:"
    echo "  - Total input files: $gjf_count"
    echo "  - Successfully processed: $success"
    echo "  - Failed: $failed"
    echo "  - Skipped (already existed): $skipped"
    echo "------------------------------------------------"
    
    # Return the counts via global variables
    TOTAL_COUNT=$((TOTAL_COUNT + gjf_count))
    TOTAL_SUCCESS=$((TOTAL_SUCCESS + success))
    TOTAL_FAILED=$((TOTAL_FAILED + failed))
    TOTAL_SKIPPED=$((TOTAL_SKIPPED + skipped))
}

# Initialize counters for all files
TOTAL_COUNT=0
TOTAL_SUCCESS=0
TOTAL_FAILED=0
TOTAL_SKIPPED=0

# Process the standard IRC trajectory files
process_gjf_files "$INPUT_DIR" "IRC trajectory frames"

# Process static files if enabled
if $PROCESS_STATIC; then
    process_gjf_files "$STATIC_DIR" "static key frames"
fi

echo "All orbital calculations completed"
echo "Overall Summary:"
echo "  - Total input files: $TOTAL_COUNT"
echo "  - Successfully processed: $TOTAL_SUCCESS"
echo "  - Failed: $TOTAL_FAILED"
echo "  - Skipped (already existed): $TOTAL_SKIPPED"
echo

# Count generated files
LOG_COUNT=$(find "$OUTPUT_DIR" -name "*.log" | wc -l)
CUBE_COUNT=$(find "$OUTPUT_DIR" -name "*.cube" | wc -l)
echo "Number of completed calculations: $LOG_COUNT"
echo "Number of cube files generated: $CUBE_COUNT"

if [ "$CUBE_COUNT" -gt 0 ]; then
    echo "Results were generated in the following locations:"
    find "$OUTPUT_DIR" -type d -not -path "$OUTPUT_DIR" | sort | head -n 10
    DIR_COUNT=$(find "$OUTPUT_DIR" -type d -not -path "$OUTPUT_DIR" | wc -l)
    if [ "$DIR_COUNT" -gt 10 ]; then
        echo "... and $(($DIR_COUNT - 10)) more directories"
    fi
else
    echo "WARNING: No cube files were generated. Check the log for errors."
fi

echo "Job completed"

##DO NOT ADD/EDIT BEYOND THIS LINE##
##Job monitor command to list the resource usage
my-job-stats -a -n -s 