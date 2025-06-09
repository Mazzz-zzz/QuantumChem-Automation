#!/usr/bin/env python3
"""
KinBot Job Creator - Generates KinBot job configuration files from SMILES strings.

This script takes SMILES strings as input and creates KinBot job configurations for further analysis.
"""

import os
import json
import argparse
import shutil
import re
from rdkit import Chem
from rdkit.Chem import AllChem


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Create KinBot job configurations from SMILES strings')
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--smiles_list', type=str, help='Path to file containing SMILES strings (one per line)')
    input_group.add_argument('--smiles', type=str, help='Comma-separated list of SMILES strings')
    
    # Other arguments
    parser.add_argument('--template', type=str, default='../templates/kinbot-template.json', 
                        help='Template KinBot job file (either a path or filename in templates directory)')
    parser.add_argument('--output_dir', type=str, default='../kinbot_jobs', help='Output directory for job files')
    parser.add_argument('--multiplicity', type=int, default=1, help='Multiplicity for SMILES input (default: 1)')
    return parser.parse_args()


def generate_3d_coords(smiles):
    """Generate 3D coordinates from SMILES string using RDKit."""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
            
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, AllChem.ETKDG())
        
        # Get coordinates in KinBot format
        atoms = []
        for atom in mol.GetAtoms():
            atoms.append(atom.GetSymbol())
        
        coords = mol.GetConformer().GetPositions()
        
        # Format for KinBot
        structure = []
        for i, atom in enumerate(atoms):
            structure.extend([atom, coords[i][0], coords[i][1], coords[i][2]])
            
        return structure
    except Exception as e:
        print(f"Error generating 3D coordinates: {e}")
        return None


def create_kinbot_job(template_file, species_name, smiles, output_dir, multiplicity=1):
    """Create a KinBot job configuration file from template."""
    try:
        # Clean species name for filename (remove parentheses, etc.)
        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '', species_name)
        
        # Create species-specific subdirectory
        species_dir = os.path.join(output_dir, clean_name)
        os.makedirs(species_dir, exist_ok=True)
        
        # Check if template is a JSON file or a template path
        if template_file.endswith('.json'):
            # Load existing template JSON file
            with open(template_file, 'r') as f:
                config = json.load(f)
                
            # Update configuration
            config['title'] = clean_name
            config['smiles'] = smiles
            config['mult'] = multiplicity
        else:
            # Template file contains placeholders
            with open(template_file, 'r') as f:
                template_content = f.read()
                
            # Replace template placeholders
            template_content = template_content.replace('{species_name}', clean_name)
            template_content = template_content.replace('{smiles}', smiles)
            template_content = template_content.replace('{multiplicity}', str(multiplicity))
            
            # Load the JSON after replacements
            config = json.loads(template_content)
        
        # Get 3D structure if not already specified
        if 'structure' not in config and smiles:
            structure = generate_3d_coords(smiles)
            if structure:
                config['structure'] = structure
            else:
                print(f"Warning: Could not generate 3D structure for {species_name} with SMILES {smiles}")
                return None
        
        # Write configuration to species subdirectory
        output_file = os.path.join(species_dir, f"{clean_name}.json")
        with open(output_file, 'w') as f:
            json.dump(config, f, indent=4)
            
        # Copy queue template to species subdirectory
        queue_template = config.get('queue_template', 'defaultqueue.sbatch')
        if os.path.exists(queue_template):
            shutil.copy(queue_template, species_dir)
            
        # Create run script in species subdirectory
        create_run_script(clean_name, species_dir)
        
        return output_file
    except Exception as e:
        print(f"Error creating KinBot job: {e}")
        return None


def create_run_script(species_name, output_dir):
    """Create a run script for the KinBot job."""
    script_content = f"""#!/bin/bash
#SBATCH --account="punim0131"
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3-00:00:00
#SBATCH --mem=8G
#SBATCH --partition=sapphire
#SBATCH --job-name=kinbot_{species_name}
#SBATCH --output=kinbot_%j.log
#SBATCH --error=kinbot_%j.err

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

# Run KinBot
kinbot {species_name}.json

##DO NOT ADD/EDIT BEYOND THIS LINE##
##Job monitor command to list the resource usage
my-job-stats -a -n -s 
"""
    
    script_path = os.path.join(output_dir, f"run_{species_name}.sh")
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Make executable
    os.chmod(script_path, 0o755)


def process_smiles_input(smiles_list, template_path, output_dir, multiplicity=1):
    """Process a list of SMILES strings to create KinBot jobs.
    
    Args:
        smiles_list (list): List of SMILES strings
        template_path (str): Path to the KinBot template file
        output_dir (str): Output directory for job files
        multiplicity (int): Default multiplicity to use
        
    Returns:
        list: List of created job files
    """
    created_jobs = []
    processed_species = []
    
    for i, smiles in enumerate(smiles_list):
        smiles = smiles.strip()
        if not smiles:
            continue
            
        print(f"\nProcessing SMILES: {smiles}")
        
        # Generate a species name from the SMILES if not provided
        # For simplicity, we'll use "species_N" where N is the index
        species_name = f"species_{i+1}"
        
        # Validate SMILES
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            print(f"  WARNING: Invalid SMILES format: {smiles}")
            print(f"  Skipping KinBot job creation for this SMILES")
            continue
        
        # Create KinBot job
        job_file = create_kinbot_job(template_path, species_name, smiles, output_dir, multiplicity)
        if job_file:
            created_jobs.append(job_file)
            clean_name = re.sub(r'[^a-zA-Z0-9_-]', '', species_name)
            processed_species.append(clean_name)
            print(f"  Created KinBot job file: {job_file}")
    
    return created_jobs, processed_species


def main():
    """Main function."""
    args = parse_arguments()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Get the proper template path
    if not os.path.exists(args.template):
        # Check if it's in the templates directory 
        script_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(os.path.dirname(script_dir), "templates")
        template_path = os.path.join(templates_dir, args.template)
        if not os.path.exists(template_path):
            print(f"Error: Template file not found: {args.template}")
            return
    else:
        template_path = args.template
    
    # Process SMILES input
    smiles_list = []
    
    if args.smiles:
        # Parse comma-separated SMILES list
        smiles_list = [s.strip() for s in args.smiles.split(',')]
        print(f"Processing {len(smiles_list)} SMILES from command line input")
    
    elif args.smiles_list:
        # Read SMILES from file (one per line)
        if not os.path.exists(args.smiles_list):
            print(f"Error: SMILES list file not found: {args.smiles_list}")
            return
            
        with open(args.smiles_list, 'r') as f:
            smiles_list = [line.strip() for line in f if line.strip()]
        print(f"Processing {len(smiles_list)} SMILES from file: {args.smiles_list}")
    
    # Process the SMILES list
    created_jobs, processed_species = process_smiles_input(
        smiles_list, 
        template_path, 
        args.output_dir, 
        args.multiplicity
    )
    
    print(f"\nCreated {len(created_jobs)} KinBot job files in species-specific directories under {args.output_dir}")
    if created_jobs:
        print("\nTo run a KinBot job, navigate to the species directory and submit the run script:")
        for species in processed_species:
            print(f"cd {args.output_dir}/{species}")
            print(f"sbatch run_{species}.sh")
            print("")


if __name__ == "__main__":
    main()
