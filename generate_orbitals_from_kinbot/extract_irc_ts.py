#!/usr/bin/env python3
"""
Script to extract only transition state geometries from IRC calculation files.

This script:
1. Searches for IRC log files in specified directories
2. Extracts the transition state geometry (middle frame of IRC trajectory)
3. Creates Gaussian input files for orbital calculations of these transition states
"""

import os
import sys
import argparse
import re
import json
from pathlib import Path

# Atomic number to element symbol mapping
CODE = {"1" : "H", "2" : "He", "3" : "Li", "4" : "Be", "5" : "B", \
"6"  : "C", "7"  : "N", "8"  : "O", "9" : "F", "10" : "Ne", \
"11" : "Na" , "12" : "Mg" , "13" : "Al" , "14" : "Si" , "15" : "P", \
"16" : "S"  , "17" : "Cl" , "18" : "Ar" , "19" : "K"  , "20" : "Ca", \
"21" : "Sc" , "22" : "Ti" , "23" : "V"  , "24" : "Cr" , "25" : "Mn", \
"26" : "Fe" , "27" : "Co" , "28" : "Ni" , "29" : "Cu" , "30" : "Zn", \
"31" : "Ga" , "32" : "Ge" , "33" : "As" , "34" : "Se" , "35" : "Br", \
"36" : "Kr" , "37" : "Rb" , "38" : "Sr" , "39" : "Y"  , "40" : "Zr", \
"41" : "Nb" , "42" : "Mo" , "43" : "Tc" , "44" : "Ru" , "45" : "Rh", \
"46" : "Pd" , "47" : "Ag" , "48" : "Cd" , "49" : "In" , "50" : "Sn", \
"51" : "Sb" , "52" : "Te" , "53" : "I"  , "54" : "Xe" , "55" : "Cs", \
"56" : "Ba" , "57" : "La" , "58" : "Ce" , "59" : "Pr" , "60" : "Nd", \
"61" : "Pm" , "62" : "Sm" , "63" : "Eu" , "64" : "Gd" , "65" : "Tb", \
"66" : "Dy" , "67" : "Ho" , "68" : "Er" , "69" : "Tm" , "70" : "Yb", \
"71" : "Lu" , "72" : "Hf" , "73" : "Ta" , "74" : "W"  , "75" : "Re", \
"76" : "Os" , "77" : "Ir" , "78" : "Pt" , "79" : "Au" , "80" : "Hg", \
"81" : "Tl" , "82" : "Pb" , "83" : "Bi" , "84" : "Po" , "85" : "At", \
"86" : "Rn" , "87" : "Fr" , "88" : "Ra" , "89" : "Ac" , "90" : "Th", \
"91" : "Pa" , "92" : "U"  , "93" : "Np" , "94" : "Pu" , "95" : "Am", \
"96" : "Cm" , "97" : "Bk" , "98" : "Cf" , "99" : "Es" ,"100" : "Fm", \
"101": "Md" ,"102" : "No" ,"103" : "Lr" ,"104" : "Rf" ,"105" : "Db", \
"106": "Sg" ,"107" : "Bh" ,"108" : "Hs" ,"109" : "Mt" ,"110" : "Ds", \
"111": "Rg" ,"112" : "Uub","113" : "Uut","114" : "Uuq","115" : "Uup", \
"116": "Uuh","117" : "Uus","118" : "Uuo"}

def find_irc_log_files(base_dir):
    """Find all IRC log files in the specified directory and subdirectories."""
    base_path = Path(base_dir).resolve()
    print(f"Searching for IRC log files in: {base_path}")
    
    irc_log_files = []
    
    # Walk through directories and find IRC log files
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.log') and ('_IRC_F' in file or '_IRC_R' in file):
                log_path = Path(os.path.join(root, file))
                irc_log_files.append(log_path)
    
    if not irc_log_files:
        print(f"WARNING: No IRC log files found in {base_dir}")
        return []
    
    print(f"Found {len(irc_log_files)} IRC log files")
    
    # Print some of the found files for verification
    if len(irc_log_files) > 0:
        print("\nSample of files found:")
        for file in irc_log_files[:min(5, len(irc_log_files))]:
            print(f"  - {file}")
        if len(irc_log_files) > 5:
            print(f"  ... and {len(irc_log_files) - 5} more")
    
    return irc_log_files

def extract_irc_frames(log_file):
    """Extract molecular geometries from IRC log file."""
    frames = []
    reaction_coords = []
    
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        # Find all "Standard orientation" or "Input orientation" sections
        orientation_indices = []
        for i, line in enumerate(lines):
            if "Standard orientation:" in line or "Input orientation:" in line:
                orientation_indices.append(i)
        
        # Try to extract IRC step information
        for i, line in enumerate(lines):
            if "IRC-IRC-IRC" in line and "Point Number" in lines[i+1]:
                try:
                    point_line = lines[i+1]
                    point_match = re.search(r'Point Number\s+(\d+)', point_line)
                    if point_match:
                        step_num = int(point_match.group(1))
                        reaction_coords.append(step_num)
                except (IndexError, ValueError):
                    pass
        
        # If we couldn't find IRC points, just number them sequentially
        if not reaction_coords:
            reaction_coords = list(range(len(orientation_indices)))
        
        # Extract coordinates from each orientation section
        for idx, orient_idx in enumerate(orientation_indices):
            try:
                # Get the IRC step number or use sequential numbering
                step_num = reaction_coords[idx] if idx < len(reaction_coords) else idx
                
                # Skip header lines to reach coordinate data
                i = orient_idx + 5
                atoms = []
                
                # Read atom coordinates until we hit the separator
                while i < len(lines) and "-----" not in lines[i]:
                    parts = lines[i].split()
                    if len(parts) >= 6:
                        atom_idx = parts[0]
                        atom_num = parts[1]
                        symbol = CODE.get(atom_num, "X")  # Use X for unknown elements
                        x, y, z = float(parts[3]), float(parts[4]), float(parts[5])
                        atoms.append((symbol, x, y, z))
                    i += 1
                
                # Only add if we found atoms
                if atoms:
                    # Create timestep label
                    if "_IRC_F" in str(log_file):
                        direction = "Forward"
                    elif "_IRC_R" in str(log_file):
                        direction = "Reverse"
                    else:
                        direction = "Unknown"
                        
                    timestep = f"IRC {direction} Point {step_num}"
                    frames.append((timestep, atoms, step_num, direction))
            except Exception as e:
                print(f"Error extracting frame {idx} from {log_file}: {str(e)}")
        
        return frames
        
    except Exception as e:
        print(f"Error reading {log_file}: {str(e)}")
        return []

def get_successful_reactions(base_dir):
    """Find all successful IRC reactions by parsing kinbot_monitor.out files."""
    successful_reactions = {}
    
    # Walk through directories and find monitor files
    for root, dirs, files in os.walk(Path(base_dir)):
        if "kinbot_monitor.out" in files:
            monitor_file = os.path.join(root, "kinbot_monitor.out")
            try:
                with open(monitor_file, 'r') as f:
                    for line in f.readlines():
                        parts = line.strip().split()
                        if len(parts) >= 3 and parts[0] == "-1":  # Successful reaction
                            reaction_name = parts[2]
                            # Check if this is an IRC reaction (either r12_insertion, r13_insertion, etc.)
                            if any(marker in reaction_name for marker in ["_r12_", "_r13_", "_intra_"]):
                                successful_reactions[reaction_name] = True
            except Exception as e:
                print(f"Error reading {monitor_file}: {str(e)}")
    
    print(f"Found {len(successful_reactions)} successful IRC reactions")
    return successful_reactions

def extract_transition_state_from_log(log_file):
    """Extract transition state geometry directly from log file."""
    frames = extract_irc_frames(log_file)
    
    if not frames:
        return None
    
    # For IRC calculations, the transition state is at the beginning of the IRC
    # For forward IRC, it's the first frame; for reverse IRC, it's also the first frame
    # We'll just take the first frame from either direction
    return frames[0] if frames else None

def create_gaussian_input_file(molecule, reaction_name, timestep, atoms, output_dir, 
                              method="wb97xd", basis="6-311++G(d,p)"):
    """Create a Gaussian input file for a transition state."""
    # Create base name for files
    base_name = f"{reaction_name}_TS"
    
    # Create a subfolder for this reaction
    reaction_dir = Path(output_dir) / reaction_name
    reaction_dir.mkdir(parents=True, exist_ok=True)
    
    # Create Gaussian input file
    gjf_file = reaction_dir / f"{base_name}.gjf"
    
    # Skip if the file already exists
    if gjf_file.exists():
        print(f"  - Input file already exists: {gjf_file}")
        return str(gjf_file)
    
    with open(gjf_file, 'w') as f:
        f.write(f"%chk={base_name}.chk\n")
        f.write("%mem=8GB\n")
        f.write("%nprocshared=4\n")
        f.write(f"# {method}/{basis} NoSymm pop=full density=current\n\n")
        f.write(f"{molecule} Transition State - {timestep}\n\n")
        f.write("0 1\n")
        for symbol, x, y, z in atoms:
            f.write(f"{symbol:2s}  {x:12.6f}  {y:12.6f}  {z:12.6f}\n")
        f.write("\n")
    
    # Also save an XYZ file for visualization
    xyz_file = reaction_dir / f"{base_name}.xyz"
    with open(xyz_file, 'w') as f:
        f.write(f"{len(atoms)}\n")
        f.write(f"{molecule} Transition State - {timestep}\n")
        for symbol, x, y, z in atoms:
            f.write(f"{symbol} {x:12.6f} {y:12.6f} {z:12.6f}\n")
    
    print(f"  - Created input file: {gjf_file}")
    print(f"  - Created XYZ file: {xyz_file}")
    return str(gjf_file)

def extract_ts_from_combined_trajectory(xyz_file):
    """Extract the transition state frame from a combined XYZ trajectory file."""
    # Read the XYZ file
    frames = []
    try:
        with open(xyz_file, 'r') as f:
            lines = f.readlines()
        
        i = 0
        while i < len(lines):
            try:
                n_atoms = int(lines[i].strip())
                timestep = lines[i+1].strip()
                atoms = []
                for j in range(n_atoms):
                    atom_line = lines[i+2+j].strip().split()
                    atoms.append((atom_line[0], float(atom_line[1]), float(atom_line[2]), float(atom_line[3])))
                frames.append((timestep, atoms))
                i += n_atoms + 2
            except (ValueError, IndexError):
                break
    except Exception as e:
        print(f"Error reading {xyz_file}: {str(e)}")
        return None
    
    if not frames:
        print(f"  ERROR: No frames found in {xyz_file}")
        return None
    
    # The transition state is in the middle of the combined trajectory
    ts_index = len(frames) // 2
    return frames[ts_index]

def process_irc_files(irc_files, output_dir="./ts_geometries", successful_reactions=None, 
                     method="wb97xd", basis="6-311++G(d,p)"):
    """Process IRC log files and extract transition state geometries."""
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Store information about all generated TS files
    all_ts_inputs = {}
    
    # Group IRC files by reaction
    reaction_groups = {}
    for log_file in irc_files:
        filename = log_file.name
        
        # Extract reaction name
        match = re.match(r'(.+?)_(IRC_[FR])', filename)
        if match:
            reaction_name = match.group(1)
            irc_type = match.group(2)
        else:
            # Fallback if pattern is different
            reaction_name = filename.split('_IRC_')[0]
            irc_type = "IRC_F" if "_IRC_F" in filename else "IRC_R"
        
        if reaction_name not in reaction_groups:
            reaction_groups[reaction_name] = {}
        
        reaction_groups[reaction_name][irc_type] = log_file
    
    # Process each reaction
    processed_reactions = 0
    for reaction_name, files in reaction_groups.items():
        # Skip unsuccessful reactions if we have a filter
        if successful_reactions is not None and reaction_name not in successful_reactions:
            print(f"Skipping reaction {reaction_name} as it did not lead to products")
            continue
            
        print(f"Processing reaction: {reaction_name}")
        processed_reactions += 1
        
        # Prefer to use the forward IRC file if available
        log_file = files.get("IRC_F", files.get("IRC_R"))
        if not log_file:
            print(f"  WARNING: No IRC log file found for {reaction_name}")
            continue
        
        # Extract transition state directly from the log file
        ts_frame = extract_transition_state_from_log(log_file)
        
        if not ts_frame:
            print(f"  WARNING: Could not extract transition state for {reaction_name}")
            continue
        
        # Parse the molecule name from the reaction name (first part before underscore)
        molecule = reaction_name.split('_')[0]
        
        # Create Gaussian input for the transition state
        timestep, atoms, step_num, direction = ts_frame
        gjf_file = create_gaussian_input_file(
            molecule, reaction_name, timestep, atoms, output_dir, 
            method, basis
        )
        
        # Add to the list of TS inputs
        all_ts_inputs[reaction_name] = {
            "input_file": gjf_file,
            "molecule": molecule,
            "timestep": timestep
        }
        
        print(f"  - Extracted transition state for {reaction_name}")
        print("----------------------------------------")
    
    # Write the summary JSON file
    summary_file = Path(output_dir) / "ts_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(all_ts_inputs, f, indent=2)
        
    # Create a README file with instructions
    readme_file = Path(output_dir) / "README.txt"
    with open(readme_file, 'w') as f:
        f.write("Transition State Geometries\n")
        f.write("==========================\n\n")
        f.write(f"This directory contains transition state geometries extracted from IRC calculations.\n")
        f.write(f"Each reaction has its own subfolder containing:\n")
        f.write(f"  - Gaussian input file (.gjf) for orbital calculations\n")
        f.write(f"  - XYZ file for visualization\n\n")
        f.write(f"Total reactions processed: {processed_reactions}\n")
        f.write(f"Total transition states extracted: {len(all_ts_inputs)}\n\n")
        f.write(f"To run calculations on all transition states:\n")
        f.write(f"  $ sbatch submit_gaussian_calculations.sh {output_dir}\n")
    
    print(f"\nSummary of transition state files saved to: {summary_file}")
    print(f"Successfully processed {processed_reactions} out of {len(reaction_groups)} reactions")
    return all_ts_inputs

def main():
    parser = argparse.ArgumentParser(description="Extract transition state geometries from IRC calculations")
    parser.add_argument("--irc-dir", default="../AUTOMATION-CENTER/kinbot_jobs/C2-SO3-NEW",
                        help="Base directory containing KinBot results with IRC calculations (default: ../AUTOMATION-CENTER/kinbot_jobs/CF3COOH-HIR)")
    parser.add_argument("--output-dir", default="./ts_geometries",
                        help="Directory to store transition state geometries and input files (default: ./ts_geometries)")
    parser.add_argument("--method", default="wb97xd",
                        help="Computational method to use (default: wb97xd)")
    parser.add_argument("--basis", default="6-311++G(d,p)",
                        help="Basis set to use (default: 6-311++G(d,p))")
    parser.add_argument("--all-reactions", action="store_true",
                        help="Process all reactions, even those without products")
    
    args = parser.parse_args()
    
    # Find IRC log files
    print("Searching for IRC log files...")
    irc_files = find_irc_log_files(args.irc_dir)
    
    if not irc_files:
        print("No IRC log files found. Cannot extract transition states.")
        return
    
    # Find successful reactions (only if we're filtering)
    successful_reactions = None
    if not args.all_reactions:
        print("\nIdentifying successful IRC reactions...")
        successful_reactions = get_successful_reactions(args.irc_dir)
        print(f"Found {len(successful_reactions)} successful IRC reactions")
    
    # Process IRC files and extract transition states
    print("\n=== Extracting transition state geometries ===")
    all_ts_inputs = process_irc_files(
        irc_files, 
        output_dir=args.output_dir,
        successful_reactions=successful_reactions,
        method=args.method,
        basis=args.basis
    )
    
    # Count total TS inputs
    total_ts_inputs = len(all_ts_inputs)
    
    print(f"\nSummary:")
    print(f"Extracted {total_ts_inputs} transition state geometries")
    print(f"All transition state files have been saved to: {args.output_dir}")
    print(f"\nNext steps:")
    print(f"1. Review the transition state geometries in the XYZ files")
    print(f"2. Run Gaussian calculations on the transition states:")
    print(f"   $ sbatch submit_gaussian_calculations.sh {args.output_dir}")

if __name__ == "__main__":
    main() 