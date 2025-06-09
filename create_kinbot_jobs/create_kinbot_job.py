#!/usr/bin/env python3
"""
KinBot Job Creator - Generates KinBot job configuration files based on RMG flux analysis.

This script processes RMG output (chemkin files) to identify species with the highest flux,
and creates KinBot job configurations for further analysis.
"""

import os
import json
import argparse
import shutil
import re
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
import cantera as ct


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Create KinBot job configurations from RMG/Chemkin data')
    parser.add_argument('--mechanism', type=str, default='../rmg_jobs/chemkin/chem_annotated.inp', help='Path to chemkin mechanism file')
    parser.add_argument('--species_dict', type=str, default='../rmg_jobs/chemkin/species_dictionary.txt', help='Path to RMG species dictionary for extracting SMILES')
    parser.add_argument('--template', type=str, default='../templates/kinbot-template.json', 
                        help='Template KinBot job file (either a path or filename in templates directory)')
    parser.add_argument('--top', type=int, default=5, help='Number of top flux species to generate jobs for')
    parser.add_argument('--output_dir', type=str, default='../kinbot_jobs', help='Output directory for job files')
    parser.add_argument('--temperature', type=float, default=1000.0, help='Temperature in K for flux analysis')
    parser.add_argument('--pressure', type=float, default=101325.0, help='Pressure in Pa for flux analysis')
    parser.add_argument('--time', type=float, default=1.0, help='Simulation time in seconds for flux analysis')
    return parser.parse_args()


def parse_chemkin_species(mechanism_file):
    """Extract species names from Chemkin mechanism file."""
    species_list = []
    in_species_section = False
    
    with open(mechanism_file, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Check if we've entered the SPECIES section
            if line.upper() == "SPECIES":
                in_species_section = True
                continue
                
            # Check if we've left the SPECIES section
            if in_species_section and "END" in line.upper():
                break
                
            # Extract species from the line
            if in_species_section and line and not line.startswith("!"):
                # Remove comments
                if "!" in line:
                    line = line.split("!", 1)[0].strip()
                
                # Split by whitespace and add species
                for species in line.split():
                    if species:
                        species_list.append(species)
    
    return species_list


def parse_chemkin_reactions(mechanism_file):
    """Extract reactions and flux pairs from Chemkin mechanism file."""
    reactions = []
    flux_pairs = {}
    in_reactions_section = False
    current_reaction = None
    
    with open(mechanism_file, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Check if we've entered the REACTIONS section
            if "REACTIONS" in line.upper():
                in_reactions_section = True
                continue
                
            # Check if we've left the REACTIONS section
            if in_reactions_section and "END" in line.upper():
                break
            
            # Skip comments and empty lines
            if not in_reactions_section or not line or line.startswith("!"):
                continue
                
            # Check for flux pairs in comments
            if "Flux pairs:" in line:
                if current_reaction:
                    # Extract flux pairs
                    flux_info = line.split("Flux pairs:")[1].strip()
                    pairs = []
                    
                    # Parse each pair (format: species1, species2;)
                    for pair in flux_info.split(";"):
                        if pair.strip():
                            parts = pair.strip().split(",")
                            if len(parts) == 2:
                                species1 = parts[0].strip()
                                species2 = parts[1].strip()
                                pairs.append((species1, species2))
                    
                    flux_pairs[current_reaction] = pairs
            
            # Check for reaction definition
            elif "=" in line and not line.startswith("!"):
                # Extract reaction equation (before any rate parameters)
                rxn_parts = line.split()
                reaction_eq = ""
                for part in rxn_parts:
                    reaction_eq += part + " "
                    if "=" in part:
                        break
                
                current_reaction = reaction_eq.strip()
                reactions.append(current_reaction)
    
    return reactions, flux_pairs


def convert_chemkin_to_cantera(chemkin_file):
    """Convert Chemkin to Cantera format for flux analysis."""
    output_file = 'converted_mech.yaml'
    
    try:
        import subprocess
        cmd = ['ck2yaml', '--input', chemkin_file, '--output', output_file]
        
        subprocess.run(cmd, check=True)
        return output_file
    except Exception as e:
        print(f"Error converting chemkin to cantera: {e}")
        print("Make sure 'ck2yaml' is installed and in your PATH.")
        return None


def analyze_flux(mech_file, species_list, T, P, sim_time):
    """Analyze species flux using Cantera."""
    try:
        # Load the mechanism
        gas = ct.Solution(mech_file)
        
        # Set initial conditions - equal mole fractions
        X = {species: 1.0/len(species_list) for species in species_list 
             if species in gas.species_names and species not in ['Ar', 'He', 'Ne', 'N2']}
        
        if not X:
            print("Warning: No valid species found. Using default initialization.")
            gas.TP = T, P
            gas.set_equivalence_ratio(1.0, 'C', 'O2:1.0, N2:3.76')
        else:
            gas.TPX = T, P, X
        
        # Create reactor and run simulation
        r = ct.IdealGasReactor(gas)
        sim = ct.ReactorNet([r])
        sim.advance(sim_time)
        
        # Get flux data
        flux_data = pd.DataFrame({
            'species': gas.species_names,
            'net_flux': gas.net_production_rates,  # kmol·m⁻³·s⁻¹
        })
        
        # Sort by absolute flux
        flux_data = flux_data.reindex(flux_data.net_flux.abs().sort_values(ascending=False).index)
        
        return flux_data
        
    except Exception as e:
        print(f"Error analyzing flux: {e}")
        return None


def extract_smiles_from_chemkin_name(species_name):
    """Extract potential SMILES information from a Chemkin species name."""
    # Remove index/ID parts like (1) from CH3F-V1(1)
    base_name = re.sub(r'\(\d+\)$', '', species_name)
    
    # No more hardcoded dictionary - returning None to let the get_smiles_for_species
    # function handle parsing from the species dictionary
    return None


def parse_species_dictionary(species_dict_file):
    """Parse a species dictionary file to extract SMILES."""
    smiles_dict = {}
    if not species_dict_file or not os.path.exists(species_dict_file):
        return smiles_dict
        
    try:
        with open(species_dict_file, 'r') as f:
            content = f.read()
            
        # Split by species entries
        species_entries = re.split(r'\n\s*\n', content)
        
        for entry in species_entries:
            lines = entry.strip().split('\n')
            if not lines:
                continue
                
            # First line contains the species name
            species_name = lines[0].strip()
            
            # Look for SMILES in the entry
            smiles = None
            for line in lines:
                if 'SMILES' in line:
                    smiles_match = re.search(r'SMILES:\s*([^\s]+)', line)
                    if smiles_match:
                        smiles = smiles_match.group(1)
                        break
                        
            if species_name and smiles:
                smiles_dict[species_name] = smiles
                
        return smiles_dict
    except Exception as e:
        print(f"Error parsing species dictionary: {e}")
        return {}


def parse_rmg_species_dictionary(species_dict_file):
    """
    Parse an RMG species dictionary file to extract SMILES using RMG's molecule tools.
    
    Args:
        species_dict_file (str): Path to the RMG species dictionary file
        
    Returns:
        dict: Dictionary mapping species names to their SMILES representations
    """
    smiles_dict = {}
    if not species_dict_file or not os.path.exists(species_dict_file):
        return smiles_dict
    
    try:
        # Import RMG libraries - these should be available in the prepackaged_rmg_env
        try:
            from rmgpy.molecule import Molecule
            rmg_available = True
        except ImportError:
            print("WARNING: RMG-Py not available. Using fallback method for adjacency list parsing.")
            rmg_available = False
        
        with open(species_dict_file, 'r') as f:
            content = f.read()
        
        # Split by species entries (empty line separates entries)
        species_entries = re.split(r'\n\s*\n', content)
        
        for entry in species_entries:
            if not entry.strip():
                continue
                
            lines = entry.strip().split('\n')
            if not lines:
                continue
            
            # First line contains the species name (might include ID in parentheses)
            species_name_line = lines[0].strip()
            species_name_match = re.match(r'^([^(]+)(?:\((\d+)\))?$', species_name_line)
            
            if species_name_match:
                species_name = species_name_match.group(1).strip()
                
                if rmg_available:
                    # Try to convert adjacency list to SMILES using RMG
                    try:
                        mol = Molecule().from_adjacency_list('\n'.join(lines))
                        smiles = mol.to_smiles()
                        smiles_dict[species_name] = smiles
                        
                        # Also store with the ID if present
                        if species_name_line != species_name:
                            smiles_dict[species_name_line] = smiles
                    except Exception as e:
                        print(f"Error converting adjacency list for {species_name}: {str(e)}")
                else:
                    # Fallback method to manually convert simple adjacency lists
                    # This is limited but can handle basic cases
                    try:
                        smiles = convert_adjacency_to_smiles(lines)
                        if smiles:
                            smiles_dict[species_name] = smiles
                            
                            # Also store with the ID if present
                            if species_name_line != species_name:
                                smiles_dict[species_name_line] = smiles
                    except Exception as e:
                        print(f"Error with fallback conversion for {species_name}: {str(e)}")
        
        return smiles_dict
    except Exception as e:
        print(f"Error parsing RMG species dictionary: {e}")
        return smiles_dict


def convert_adjacency_to_smiles(adjacency_lines):
    """
    Basic converter from RMG adjacency list to SMILES for common molecules.
    This is a fallback when RMG is not available.
    
    Args:
        adjacency_lines (list): List of strings representing the adjacency list
        
    Returns:
        str: SMILES string or None if conversion fails
    """
    # Extract species name from first line
    species_name = adjacency_lines[0].strip().split('(')[0].strip()
    
    # Check for simple cases first
    simple_cases = {
        'Ar': '[Ar]',
        'He': '[He]',
        'Ne': '[Ne]',
        'N2': 'N#N',
        'H': '[H]',
        'H2': '[H][H]',
    }
    
    if species_name in simple_cases:
        return simple_cases[species_name]
    
    # Check for multiplicity in second line
    multiplicity = 1
    if len(adjacency_lines) > 1 and adjacency_lines[1].strip().startswith('multiplicity'):
        try:
            multiplicity = int(adjacency_lines[1].strip().split()[1])
            atom_lines = adjacency_lines[2:]
        except:
            atom_lines = adjacency_lines[1:]
    else:
        atom_lines = adjacency_lines[1:]
    
    # Extract atoms and bonds
    atoms = {}
    bonds = {}
    
    for line in atom_lines:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split()
        if len(parts) < 3:
            continue
            
        # Extract atom index and element
        atom_idx = int(parts[0])
        atom_element = parts[1]
        
        # Extract electron configuration
        unpaired = 0
        for part in parts:
            if part.startswith('u'):
                unpaired_match = re.match(r'u(\d+)', part)
                if unpaired_match:
                    unpaired = int(unpaired_match.group(1))
        
        atoms[atom_idx] = {'element': atom_element, 'unpaired': unpaired}
        
        # Extract bonds
        for part in parts[3:]:
            if '{' in part and '}' in part:
                bond_match = re.match(r'\{(\d+),([^}]+)\}', part)
                if bond_match:
                    bond_idx = int(bond_match.group(1))
                    bond_type = bond_match.group(2)
                    
                    # Convert RMG bond types to SMILES bond types
                    bond_map = {'S': '-', 'D': '=', 'T': '#', 'B': ''}
                    bond_smiles = bond_map.get(bond_type, '-')
                    
                    # Store the bond
                    bond_key = tuple(sorted([atom_idx, bond_idx]))
                    bonds[bond_key] = bond_smiles
    
    # For very simple molecules, attempt to build SMILES directly
    if len(atoms) <= 10:  # Limit to small molecules
        # Try using RDKit to build the molecule
        try:
            from rdkit import Chem
            from rdkit.Chem import AllChem
            
            mol = Chem.RWMol()
            atom_map = {}
            
            # Add atoms
            for idx, atom_info in atoms.items():
                element = atom_info['element']
                unpaired = atom_info['unpaired']
                
                if element == 'H':
                    atom = Chem.Atom('H')
                    atom.SetNumRadicalElectrons(unpaired)
                    atom_idx = mol.AddAtom(atom)
                    atom_map[idx] = atom_idx
                elif element == 'C':
                    atom = Chem.Atom('C')
                    atom.SetNumRadicalElectrons(unpaired)
                    atom_idx = mol.AddAtom(atom)
                    atom_map[idx] = atom_idx
                elif element == 'O':
                    atom = Chem.Atom('O')
                    atom.SetNumRadicalElectrons(unpaired)
                    atom_idx = mol.AddAtom(atom)
                    atom_map[idx] = atom_idx
                elif element == 'N':
                    atom = Chem.Atom('N')
                    atom.SetNumRadicalElectrons(unpaired)
                    atom_idx = mol.AddAtom(atom)
                    atom_map[idx] = atom_idx
                elif element == 'F':
                    atom = Chem.Atom('F')
                    atom.SetNumRadicalElectrons(unpaired)
                    atom_idx = mol.AddAtom(atom)
                    atom_map[idx] = atom_idx
                elif element == 'Cl':
                    atom = Chem.Atom('Cl')
                    atom.SetNumRadicalElectrons(unpaired)
                    atom_idx = mol.AddAtom(atom)
                    atom_map[idx] = atom_idx
                elif element == 'Br':
                    atom = Chem.Atom('Br')
                    atom.SetNumRadicalElectrons(unpaired)
                    atom_idx = mol.AddAtom(atom)
                    atom_map[idx] = atom_idx
                elif element == 'I':
                    atom = Chem.Atom('I')
                    atom.SetNumRadicalElectrons(unpaired)
                    atom_idx = mol.AddAtom(atom)
                    atom_map[idx] = atom_idx
                elif element == 'S':
                    atom = Chem.Atom('S')
                    atom.SetNumRadicalElectrons(unpaired)
                    atom_idx = mol.AddAtom(atom)
                    atom_map[idx] = atom_idx
            
            # Add bonds
            for (atom1, atom2), bond_type in bonds.items():
                if atom1 in atom_map and atom2 in atom_map:
                    if bond_type == '-':
                        mol.AddBond(atom_map[atom1], atom_map[atom2], Chem.BondType.SINGLE)
                    elif bond_type == '=':
                        mol.AddBond(atom_map[atom1], atom_map[atom2], Chem.BondType.DOUBLE)
                    elif bond_type == '#':
                        mol.AddBond(atom_map[atom1], atom_map[atom2], Chem.BondType.TRIPLE)
            
            # Convert to SMILES
            Chem.SanitizeMol(mol)
            smiles = Chem.MolToSmiles(mol)
            return smiles
            
        except Exception as e:
            print(f"RDKit conversion failed: {e}")
    
    # Handle special cases based on species name
    if species_name == 'CH3F-V1':
        return 'CF'
    elif species_name == 'CH2F':
        return '[CH2]F'
    elif species_name == 'C2H4F2':
        return 'FCCF'  # 1,2-difluoroethane
    
    # Failed to convert
    return None


def get_smiles_for_species(species_name, species_dict_file=None):
    """Get SMILES for a species, using various methods."""
    # Try to get from RMG species dictionary first
    if species_dict_file and os.path.exists(species_dict_file):
        # Try RMG adjacency list format first
        rmg_smiles_dict = parse_rmg_species_dictionary(species_dict_file)
        
        # Check exact name
        if species_name in rmg_smiles_dict:
            print(f"Found SMILES for '{species_name}' in RMG dictionary")
            return rmg_smiles_dict[species_name]
            
        # Also check for name with ID removed (e.g. CH3F-V1(1) -> CH3F-V1)
        base_name = re.sub(r'\(\d+\)$', '', species_name)
        if base_name != species_name and base_name in rmg_smiles_dict:
            print(f"Found SMILES for base name '{base_name}' in RMG dictionary")
            return rmg_smiles_dict[base_name]
        
        # Fall back to regular species dictionary format
        smiles_dict = parse_species_dictionary(species_dict_file)
        if species_name in smiles_dict:
            print(f"Found SMILES for '{species_name}' in species dictionary")
            return smiles_dict[species_name]
        
        if base_name != species_name and base_name in smiles_dict:
            print(f"Found SMILES for base name '{base_name}' in species dictionary")
            return smiles_dict[base_name]
    
    # If no SMILES is found in the dictionary, notify the user
    print(f"Warning: No SMILES found for species '{species_name}' in the species dictionary.")
    
    # Simple fallback for very basic species
    simple_species = {
        'H': '[H]',
        'H2': '[H][H]',
        'O': '[O]',
        'O2': 'O=O',
        'N2': 'N#N',
        'CO': '[C-]#[O+]',
        'CO2': 'O=C=O',
        'CH4': 'C',
        'C2H4': 'C=C',
        'C2H6': 'CC',
        'CH3OH': 'CO',
        'H2O': 'O',
        'Ar': '[Ar]',
        'He': '[He]',
        'Ne': '[Ne]',
        'CH3F': 'CF',
        'CH3F-V1': 'CF',
        'CH2F': '[CH2]F',
        'C2H4F2': 'FCCF'
    }
    
    # Check for the species name directly
    if species_name in simple_species:
        print(f"Using built-in SMILES for species '{species_name}': {simple_species[species_name]}")
        return simple_species[species_name]
    
    # Check for the species name with ID removed
    if base_name in simple_species:
        print(f"Using built-in SMILES for base name '{base_name}': {simple_species[base_name]}")
        return simple_species[base_name]
        
    print(f"Could not determine SMILES for '{species_name}'. Using 'C' as default.")
    return 'C'  # Default to methane as absolute fallback


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
            config['smiles'] = smiles  # Use the SMILES from species dictionary
            config['mult'] = multiplicity  # Set the multiplicity
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
    
    # Parse Chemkin file to extract species
    print(f"Parsing Chemkin mechanism file: {args.mechanism}")
    species_list = parse_chemkin_species(args.mechanism)
    reactions, flux_pairs = parse_chemkin_reactions(args.mechanism)
    
    print(f"Found {len(species_list)} species and {len(reactions)} reactions")
    
    # Parse species dictionary to get SMILES
    species_multiplicity = {}  # Dictionary to store multiplicities

    if args.species_dict and os.path.exists(args.species_dict):
        print(f"Parsing species dictionary: {args.species_dict}")
        
        # Extract multiplicity information from the species dictionary
        with open(args.species_dict, 'r') as f:
            content = f.read()
            
        # Split by species entries
        species_entries = re.split(r'\n\s*\n', content)
        
        for entry in species_entries:
            lines = entry.strip().split('\n')
            if not lines:
                continue
                
            # First line contains the species name
            species_name_line = lines[0].strip()
            
            # Default multiplicity is 1 (closed shell)
            mult = 1
            
            # Check if multiplicity is explicitly stated
            if len(lines) > 1 and 'multiplicity' in lines[1]:
                try:
                    mult = int(lines[1].strip().split()[1])
                except:
                    pass
                    
            species_multiplicity[species_name_line] = mult
            
            # Also store without ID if present
            base_name = re.sub(r'\(\d+\)$', '', species_name_line)
            if base_name != species_name_line:
                species_multiplicity[base_name] = mult
        
        rmg_smiles = parse_rmg_species_dictionary(args.species_dict)
        regular_smiles = parse_species_dictionary(args.species_dict)
        print(f"Found {len(rmg_smiles)} SMILES from RMG dictionary and {len(regular_smiles)} from regular dictionary")
        print(f"Found multiplicity information for {len(species_multiplicity)} species")
        
        # Show a few examples of parsed SMILES
        if rmg_smiles:
            print("\nExample RMG SMILES:")
            count = 0
            for species, smiles in rmg_smiles.items():
                mult = species_multiplicity.get(species, 1)
                print(f"  {species}: {smiles} (multiplicity: {mult})")
                count += 1
                if count >= 5:
                    break
    else:
        print(f"Warning: Species dictionary file not found: {args.species_dict}")
        print("Will use fallback methods for SMILES generation.")
    
    # Convert to Cantera for flux analysis
    cantera_file = convert_chemkin_to_cantera(args.mechanism)
    if not cantera_file:
        print("Error: Failed to convert Chemkin to Cantera format.")
        return
    
    # Analyze flux
    flux_data = analyze_flux(cantera_file, species_list, args.temperature, args.pressure, args.time)
    if flux_data is None:
        print("Error analyzing flux. Exiting.")
        return
    
    # Filter out inert species
    inert_species = ['Ar', 'He', 'Ne', 'N2']
    flux_data = flux_data[~flux_data['species'].isin(inert_species)]
    
    # Display top species by flux
    print("\nTop species by absolute flux:")
    print(flux_data.head(args.top))
    
    # Create KinBot jobs for top species
    created_jobs = []
    processed_species = []
    for i, row in flux_data.head(args.top).iterrows():
        species_name = row['species']
        print(f"\nProcessing species: {species_name}")
        
        # Get SMILES for the species
        smiles = get_smiles_for_species(species_name, args.species_dict)
        print(f"  Using SMILES: {smiles}")
        
        # Get multiplicity for the species
        multiplicity = species_multiplicity.get(species_name, 1)  # Default to 1 if not found
        
        # For radicals with specific naming patterns, set appropriate multiplicity
        if species_name in ['H', 'O', 'OH', 'CH3']:
            multiplicity = 2  # Common radicals
        
        print(f"  Using multiplicity: {multiplicity}")
        
        # Validate SMILES
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            print(f"  WARNING: Invalid SMILES format: {smiles}")
            print(f"  Attempting to sanitize/fix SMILES...")
            
            # Try some common fixes
            fixed_smiles = smiles
            
            # 1. Try adding brackets to atom symbols if needed
            if not any(c == '[' for c in smiles) and re.search(r'[A-Z][a-z]', smiles):
                # Convert patterns like "Br" to "[Br]" if not already bracketed
                for atom in ['Br', 'Cl', 'Na', 'Li', 'Si', 'Al', 'Ca', 'Mg', 'Fe']:
                    if atom in smiles and f'[{atom}]' not in smiles:
                        fixed_smiles = fixed_smiles.replace(atom, f'[{atom}]')
            
            # 2. Try removing unusual bonds or characters
            fixed_smiles = re.sub(r'[^A-Za-z0-9\[\]\(\)\.\+\-=#:]', '', fixed_smiles)
            
            # Check if fixed
            mol = Chem.MolFromSmiles(fixed_smiles)
            if mol is not None:
                print(f"  Fixed SMILES: {fixed_smiles}")
                smiles = fixed_smiles
            else:
                print(f"  Skipping KinBot job creation for {species_name} - could not fix SMILES")
                continue
            
        # Create KinBot job
        job_file = create_kinbot_job(template_path, species_name, smiles, args.output_dir, multiplicity)
        if job_file:
            created_jobs.append(job_file)
            clean_name = re.sub(r'[^a-zA-Z0-9_-]', '', species_name)
            processed_species.append(clean_name)
            print(f"  Created KinBot job file: {job_file}")
    
    print(f"\nCreated {len(created_jobs)} KinBot job files in species-specific directories under {args.output_dir}")
    if created_jobs:
        print("\nTo run a KinBot job, navigate to the species directory and submit the run script:")
        for species in processed_species:
            print(f"cd {args.output_dir}/{species}")
            print(f"sbatch run_{species}.sh")
            print("")
    
    # Clean up temporary files
    if os.path.exists(cantera_file):
        os.remove(cantera_file)


if __name__ == "__main__":
    main()
