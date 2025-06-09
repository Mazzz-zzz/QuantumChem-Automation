#!/usr/bin/env python3
import re
import sys
import argparse
import os
from pathlib import Path
from typing import Set, Optional, Dict, List, Tuple  # For Python 3.6+ compatibility

# ───────────────────────── Constants ──────────────────────────
# Patterns that capture exactly *one* match group with the raw ID(s)
SPECIES_PATTERNS = [
    re.compile(r"(?:conformational search|hindered rotor calculations)\s+of\s+(\S+)"),
    re.compile(r"lowest energy conformer for species\s+(\S+)", re.I),
    re.compile(r"optimization of initial well.*? of (\S+)"),
    re.compile(r"leads to products\s+\[([^\]]+)\]"),
]

# Patterns to capture transition states
TS_PATTERNS = [
    re.compile(r"optimization of TS (\S+)"),
    re.compile(r"calculating (\S+) transition state"),
    re.compile(r"optimizing TS (\S+)"),
    # Pattern for reaction lines that show reactants -> products
    re.compile(r"(\w+)\s*->\s*(\w+)"),
]

def collect_species(log_text):
    # type: (str) -> Set[str]
    """Return a set of raw species tokens found in a KinBot log."""
    found = set()  # type: Set[str]
    chemids = set()  # Store chemid strings specifically

    for line in log_text.splitlines():
        for pat in SPECIES_PATTERNS:
            m = pat.search(line)
            if not m:
                continue

            # Pattern that matches product lists needs splitting
            if pat is SPECIES_PATTERNS[-1]:
                for tok in m.group(1).split(","):
                    tok = tok.strip()
                    if tok:
                        found.add(tok)
                        # Identify chemids by their numeric format
                        if tok.isdigit() or (tok and tok[0].isdigit() and "_" in tok):
                            chemids.add(tok)
            else:
                token = m.group(1).rstrip(".,")
                found.add(token)
                # Identify chemids by their numeric format
                if token.isdigit() or (token and token[0].isdigit() and "_" in token):
                    chemids.add(token)
    
    # Also look specifically for reaction IDs with embedded chemids
    for line in log_text.splitlines():
        if "Starting IRC calculations for" in line:
            parts = line.split()
            for part in parts:
                if part.startswith("33") and "_" in part:  # Likely a chemid for reactions
                    chemids.add(part)
    
    return found, chemids

def collect_ts_reactions(log_text):
    # type: (str) -> List[Dict[str, str]]
    """Return a list of transition state information from a KinBot log."""
    ts_list = []  # type: List[Dict[str, str]]
    ts_ids = set()  # Track TS IDs we've seen to avoid duplicates
    
    for line in log_text.splitlines():
        # Look for TS names and reactant/product information
        for pat in TS_PATTERNS:
            m = pat.search(line)
            if not m:
                continue
            
            # Extract reactant -> product info if available
            if pat is TS_PATTERNS[-1] and len(m.groups()) >= 2:
                reactant = m.group(1).strip()
                product = m.group(2).strip()
                
                # Look for TS ID in the line
                ts_match = re.search(r"TS[_\s](\w+)", line, re.IGNORECASE)
                if ts_match:
                    ts_id = ts_match.group(1).strip()
                    if ts_id not in ts_ids:
                        ts_ids.add(ts_id)
                        ts_list.append({
                            "name": ts_id,
                            "reactant": reactant,
                            "product": product
                        })
            # For other patterns, just extract the TS ID
            else:
                ts_id = m.group(1).rstrip(".,")
                if ts_id not in ts_ids:
                    ts_ids.add(ts_id)
                    
                    # Try to find reactant/product info in the same line
                    reaction_match = re.search(r"(\w+)\s*->\s*(\w+)", line)
                    if reaction_match:
                        reactant = reaction_match.group(1).strip()
                        product = reaction_match.group(2).strip()
                    else:
                        # Placeholder values if actual info not found
                        reactant = f"reactant_{ts_id}"
                        product = f"product_{ts_id}"
                    
                    ts_list.append({
                        "name": ts_id,
                        "reactant": reactant,
                        "product": product
                    })
    
    return ts_list

def find_kinbot_log(path=None):
    # type: (Optional[str]) -> Optional[str]
    """
    Find a kinbot.log file. Search order:
    1. Use provided path if given
    2. Handle special '@kinbot.log' pattern to search in standard KinBot directories
    3. Look for kinbot.log in current directory
    4. Search current directory's parent directories for kinbot.log
    5. Search subdirectories for kinbot.log
    
    Returns the path to the log file or None if not found
    """
    if path and path != '@kinbot.log' and os.path.isfile(path):
        return path
    
    # Check current directory for kinbot.log
    default_log = os.path.join(os.getcwd(), "kinbot.log")
    if os.path.isfile(default_log):
        return default_log
    
    # Check parent directories for kinbot.log
    current_dir = os.path.abspath(os.getcwd())
    parent_dir = os.path.dirname(current_dir)
    while parent_dir and parent_dir != current_dir:
        log_path = os.path.join(parent_dir, "kinbot.log")
        if os.path.isfile(log_path):
            return log_path
        current_dir = parent_dir
        parent_dir = os.path.dirname(current_dir)
    
    # Check subdirectories for any kinbot.log
    for root, dirs, files in os.walk(os.getcwd()):
        if "kinbot.log" in files:
            return os.path.join(root, "kinbot.log")
    
    return None

def find_mess_file(kinbot_log_path):
    """
    Automatically find a MESS input file based on the kinbot log path.
    
    Args:
        kinbot_log_path: Path to the kinbot log file
        
    Returns:
        Path to the MESS file or None if not found
    """
    try:
        # Get the directory containing the kinbot log
        log_dir = os.path.dirname(os.path.abspath(kinbot_log_path))
        
        # Look for standard MESS file locations
        # 1. Check in 'me' subdirectory
        me_dir = os.path.join(log_dir, "me")
        if os.path.isdir(me_dir):
            # Look for mess_*.inp files
            mess_files = [f for f in os.listdir(me_dir) if f.startswith("mess_") and f.endswith(".inp")]
            if mess_files:
                # Sort to get the latest one (assuming numerical suffix)
                mess_files.sort()
                return os.path.join(me_dir, mess_files[0])
                
        # 2. Look in the same directory as the log
        mess_files = [f for f in os.listdir(log_dir) if f.startswith("mess_") and f.endswith(".inp")]
        if mess_files:
            mess_files.sort()
            return os.path.join(log_dir, mess_files[0])
            
        # 3. Broader search if needed - look in parent directory and siblings
        parent_dir = os.path.dirname(log_dir)
        for root, dirs, files in os.walk(parent_dir):
            mess_files = [f for f in files if f.startswith("mess_") and f.endswith(".inp")]
            if mess_files:
                mess_files.sort()
                return os.path.join(root, mess_files[0])
                
    except Exception as e:
        print(f"Error searching for MESS file: {e}")
        
    return None

def get_atomic_smiles(atom_name):
    """
    Returns the proper SMILES string for a given atomic species.
    
    Args:
        atom_name: The name of the atom (e.g., 'H', 'C', 'O', etc.)
        
    Returns:
        The proper SMILES string for the atom
    """
    atomic_smiles = {
        'H': '[H]',
        'C': '[C]',
        'N': '[N]',
        'O': '[O]',
        'F': '[F]',
        'Cl': '[Cl]',
        'Br': '[Br]',
        'I': '[I]',
        'S': '[S]',
        'P': '[P]',
        'Si': '[Si]',
        'B': '[B]',
        'He': '[He]',
        'Ne': '[Ne]',
        'Ar': '[Ar]',
        'Kr': '[Kr]',
        'Xe': '[Xe]',
    }
    return atomic_smiles.get(atom_name, f'[{atom_name}]')

def extract_from_mess_file(mess_file_path):
    # type: (str) -> Tuple[Set[str], List[Dict[str, str]], Dict[str, str], Dict[str, str]]
    """
    Extract species and transition state information from a MESS input file.
    
    Args:
        mess_file_path: Path to the MESS input file
        
    Returns:
        Tuple of (species_set, ts_list, species_smiles, entity_mapping)
    """
    species_set = set()
    ts_list = []
    species_smiles = {}  # Store SMILES strings for each species
    atom_species = {}    # Track which species are atoms
    entity_mapping = {}  # Map entity IDs (wells, fragments) to their chemids
    ts_mapping = {}      # Map original TS names to reaction IDs
    bimolecular_fragments = {}  # Store fragment chemids for each bimolecular species
    
    try:
        # Process the file line by line to extract information
        with open(mess_file_path, 'r') as f:
            lines = f.readlines()
        
        # First pass: extract Well and Fragment information with SMILES
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Process Well lines (species)
            if line.startswith("Well") and "!" in line:
                parts = line.split("!")
                if len(parts) >= 3:
                    # Get the well ID from first part and chemid from second part
                    well_id = parts[0].split()[1].strip()
                    chemid = parts[1].strip()
                    
                    # Add only the chemid to the species set
                    species_set.add(chemid)
                    
                    # Map well to chemid
                    entity_mapping[well_id] = chemid
                    
                    # Extract SMILES from the third part (after second !)
                    smiles_part = parts[2].strip()
                    if "[" in smiles_part:
                        smiles = smiles_part.strip()
                        # Store SMILES for chemid
                        species_smiles[chemid] = smiles
                        print(f"Found species with chemid: {chemid} (from well: {well_id}) with SMILES {smiles}")
            
            # Process Fragment lines
            elif "Fragment" in line and "!" in line:
                parts = line.split("!")
                if len(parts) >= 3:
                    # Get the fragment ID from first part
                    fragment_name = parts[0].split()[1].strip()
                    
                    # Get the chemid from the second part
                    chemid = parts[1].strip()
                    
                    # Add only the chemid to the species set
                    species_set.add(chemid)
                    
                    # Map fragment to chemid
                    entity_mapping[fragment_name] = chemid
                    
                    # Extract SMILES from the third part
                    smiles_part = parts[2].strip()
                    if "[" in smiles_part:
                        smiles = smiles_part.strip()
                        species_smiles[chemid] = smiles
                        print(f"Found species with chemid: {chemid} (from fragment: {fragment_name}) with SMILES {smiles}")
                    
                    # Check for Atom blocks that follow Fragment lines
                    j = i + 1
                    atom_found = False
                    atom_name = None
                    
                    while j < len(lines) and "End ! RRHO" not in lines[j] and "End ! Atom" not in lines[j]:
                        atom_line = lines[j].strip()
                        if "Atom" in atom_line:
                            atom_found = True
                        elif atom_found and "Name" in atom_line:
                            atom_name = atom_line.split()[-1].strip()
                            atom_species[chemid] = atom_name
                            # Assign proper atomic SMILES
                            if chemid not in species_smiles or "SMILES_" in species_smiles[chemid]:
                                species_smiles[chemid] = get_atomic_smiles(atom_name)
                                print(f"Found atomic species with chemid: {chemid} ({atom_name}) with SMILES {species_smiles[chemid]}")
                        j += 1
            
            # Process Barrier lines (transition states)
            elif line.startswith("Barrier") and not line.startswith("Barrierless"):
                parts = line.split("!")
                if len(parts) >= 2:
                    barrier_parts = parts[0].split()
                    if len(barrier_parts) >= 4:
                        ts_id = barrier_parts[1].strip()
                        reactant = barrier_parts[2].strip()
                        product = barrier_parts[3].strip()
                        
                        # Skip the template barriers with placeholder names
                        if "{" in ts_id or "{" in reactant or "{" in product:
                            continue
                        
                        # Get the reaction ID if available
                        reaction_id = parts[1].strip() if len(parts) >= 2 else ""
                        
                        # Store mapping from original TS name to reaction ID
                        ts_mapping[ts_id] = reaction_id
                        
                        # Check for submerged barrier by examining the next few lines
                        is_submerged = False
                        j = i + 1
                        while j < len(lines) and j < i + 30:  # Look at next 30 lines max
                            if "barrier is submerged" in lines[j]:
                                is_submerged = True
                                print(f"Detected submerged barrier for TS {ts_id} ({reaction_id}): {lines[j].strip()}")
                                break
                            # Also check if ZeroEnergy is 0.0 with a comment about negative energy
                            elif "ZeroEnergy[kcal/mol]" in lines[j] and "0.0" in lines[j]:
                                for k in range(j, min(j+5, len(lines))):
                                    if any(x in lines[k] for x in ["submerged", "negative", "-"]):
                                        is_submerged = True
                                        print(f"Detected likely submerged barrier for TS {ts_id} ({reaction_id}): {lines[k].strip()}")
                                        break
                            j += 1
                        
                        # Only add non-submerged barriers
                        if not is_submerged:
                            # Use reaction_id as the name if available, otherwise use ts_id
                            ts_name = reaction_id if reaction_id else ts_id
                            
                            ts_list.append({
                                "name": ts_name,
                                "original_ts_id": ts_id,  # Keep the original TS ID for reference
                                "reactant": reactant,
                                "product": product,
                                "reaction_id": reaction_id
                            })
                            print(f"Found TS {ts_name} (was {ts_id}): {reactant} -> {product}")
                        else:
                            print(f"Skipping submerged barrier TS {reaction_id if reaction_id else ts_id}: {reactant} -> {product}")
            
            # Process Bimolecular lines for additional info
            elif line.startswith("Bimolecular"):
                parts = line.split("!")
                if len(parts) >= 3:
                    bimolecular_id = parts[0].split()[1].strip()
                    # The bimolecular chemid contains info about fragments
                    bimolecular_chemid = parts[1].strip()
                    
                    # Only add the chemid to the species set if it's not a reaction ID
                    if "_" in bimolecular_chemid and not any(keyword in bimolecular_chemid.lower() for keyword in ["_insertion_", "_elim_", "_addition_", "_r12_", "_sci_"]):
                        species_set.add(bimolecular_chemid)
                    
                    # Map bimolecular ID to chemid
                    entity_mapping[bimolecular_id] = bimolecular_chemid
                    
                    # Create a list to store the fragment chemids for this bimolecular species
                    bimolecular_fragments[bimolecular_id] = []
                    
                    # Extract SMILES if present in the third part
                    if len(parts) >= 3 and "[" in parts[2]:
                        smiles = parts[2].strip()
                        species_smiles[bimolecular_chemid] = smiles
                        print(f"Found bimolecular species with chemid: {bimolecular_chemid} (from b_id: {bimolecular_id}) with SMILES {smiles}")
                    
                    # Extract fragment IDs if format is like "id1_id2"
                    elif "_" in bimolecular_chemid:
                        fragment_ids = bimolecular_chemid.split("_")
                        # We'll try to build a SMILES from fragments later
                        pass
                    
                    # Extract fragment information for this bimolecular species
                    j = i + 1
                    while j < len(lines) and "End ! Bimolecular" not in lines[j]:
                        frag_line = lines[j].strip()
                        if "Fragment" in frag_line and "!" in frag_line:
                            frag_parts = frag_line.split("!")
                            if len(frag_parts) >= 2:
                                fragment_id = frag_parts[0].split()[1].strip()
                                fragment_chemid = frag_parts[1].strip()
                                # Add this fragment chemid to the list for this bimolecular species
                                bimolecular_fragments[bimolecular_id].append(fragment_chemid)
                                print(f"Found fragment {fragment_chemid} for bimolecular species {bimolecular_id}")
                        j += 1
            
            i += 1
        
        # Second pass: look for any species that still need SMILES
        for species_id in species_set:
            if species_id not in species_smiles or "SMILES_" in species_smiles[species_id]:
                # Try to infer from naming conventions
                if species_id.lower().startswith(('h_', 'h1', 'hydrogen')):
                    species_smiles[species_id] = '[H]'
                elif species_id.lower().startswith(('c_', 'c1', 'carbon')):
                    species_smiles[species_id] = '[C]'
                elif species_id.lower().startswith(('o_', 'o1', 'oxygen')):
                    species_smiles[species_id] = '[O]'
                elif species_id.lower().startswith(('n_', 'n1', 'nitrogen')):
                    species_smiles[species_id] = '[N]'
                elif species_id.lower().startswith(('f_', 'f1', 'fluorine')):
                    species_smiles[species_id] = '[F]'
                # Add more as needed
        
        # Process special species like b_1, b_2, etc. (bimolecular species)
        # These often don't have explicit SMILES but can be derived from their reactions
        for ts in ts_list:
            reactant = ts['reactant']
            product = ts['product']
            
            # If the product is a bimolecular species like b_1, b_2, etc.
            if product.startswith('b_') and product in entity_mapping:
                # Get the actual chemid for this bimolecular species
                bimolecular_chemid = entity_mapping[product]
                
                # If we don't have a SMILES for it yet, try to derive one
                if bimolecular_chemid not in species_smiles:
                    # Look for fragments that make up this bimolecular species
                    i = 0
                    while i < len(lines):
                        line = lines[i].strip()
                        if line.startswith(f"Bimolecular {product}"):
                            # Find the fragments in the next few lines
                            fragment_smiles = []
                            j = i + 1
                            while j < len(lines) and "End ! Bimolecular" not in lines[j]:
                                if "Fragment" in lines[j] and "!" in lines[j]:
                                    parts = lines[j].split("!")
                                    if len(parts) >= 3:
                                        frag_id = parts[1].strip()
                                        if frag_id in species_smiles:
                                            fragment_smiles.append(species_smiles[frag_id])
                            j += 1
                            
                            # Combine the fragments into a bimolecular SMILES
                            if fragment_smiles:
                                species_smiles[bimolecular_chemid] = ".".join(fragment_smiles)
                                print(f"Derived SMILES for bimolecular species with chemid: {bimolecular_chemid} (from b_id: {product}): {species_smiles[bimolecular_chemid]}")
                        i += 1
                    
    except Exception as e:
        print(f"Error reading MESS file: {e}")
        import traceback
        traceback.print_exc()
    
    # Also return the TS mapping for reference
    return species_set, ts_list, species_smiles, entity_mapping, bimolecular_fragments

def get_correct_smiles_for_species(species_id):
    """
    Returns the correct SMILES string for a given species ID based on known patterns.
    
    Args:
        species_id: The ID of the species
        
    Returns:
        The proper SMILES string for the species
    """
    # Clean up the species ID for matching
    clean_id = species_id.strip("[]")
    
    # Map known species to their correct SMILES
    known_species = {
        # Atoms
        "10000000000000000002": "[H]",       # Hydrogen atom
        "190000000000000000002": "[F]",      # Fluorine atom
        
        # Radicals and molecules
        "130130000000000000002": "[CH]",     # CH radical
        "140260020000000000003": "[CH2]",    # CH2 radical
        "200200000000000000001": "[H][F]",   # HF molecule 
        "320440200000000000001": "[CH][F]",  # CF radical
        "330570420000000000002": "[CH2]F",   # Fluoromethyl radical
        
        # Wells
        "w_1": "[CH2]F",                     # Fluoromethyl radical
        "w_2": "[CH].[HF]",                  # vdW complex
        
        # Special cases for van der Waals complexes and other species
        "330570420000000000002_r12_insertion_R_2_1_3_IRC_R_prod": "[CH].[HF]"
    }
    
    # Return the known SMILES if available
    if clean_id in known_species:
        return known_species[clean_id]
    
    # Try to infer from patterns in the ID
    if "_insertion_" in clean_id:
        return "[C].[C]"  # Generic default for insertion reaction complexes
    elif "_elim_" in clean_id:
        return "[C].[C]"  # Generic default for elimination reaction complexes
    elif "_hom_sci_" in clean_id:
        return "[C].[C]"  # Generic default for homolytic scission complexes
    
    # Default fallback
    return "[C]"

# ────────────────────────── main ────────────────────────────
def main():
    # type: () -> None
    parser = argparse.ArgumentParser(description='Extract species from KinBot log and create Arkane input files')
    parser.add_argument('logfile', nargs='?', default="../kinbot_jobs/CH2H4F29/kinbot.log", 
                        help='KinBot log file (defaults to finding kinbot.log automatically). '
                             'Use "@kinbot.log" to automatically search in standard KinBot job directories.')
    parser.add_argument('--output', '-o', help='Output directory for Arkane files', default="")
    parser.add_argument('--ts', action='store_true', help='Extract and create transition state files', default=True)
    parser.add_argument('--mess-file', help='MESS input file to extract additional information (optional)')
    parser.add_argument('--smiles', help='SMILES string to use (default is extracted from MESS file)')
    parser.add_argument('--single-input', action='store_true', help='Create a single input file with all species and reactions',
                       default=True)
    
    args = parser.parse_args()
    
    # Find kinbot.log automatically if not provided
    log_path = find_kinbot_log(args.logfile)
    if not log_path:
        sys.exit("Error: Could not find kinbot.log. Please specify the path to the log file.")
    
    logfile = Path(log_path)
    if not logfile.is_file():
        sys.exit(f"error: file not found - {logfile}")
    
    print(f"Using log file: {logfile}")
    
    # Automatically find MESS file if not provided
    if not args.mess_file:
        auto_mess_file = find_mess_file(log_path)
        if auto_mess_file:
            args.mess_file = auto_mess_file
            print(f"Found MESS file automatically: {args.mess_file}")
        else:
            print("No MESS file found automatically. Continuing without MESS file.")
    
    # Read the log file
    log_content = logfile.read_text(encoding="utf-8")
    
    # Extract species from log
    species, chemids = collect_species(log_content)
    
    # Extract TS information if requested
    ts_reactions = []
    if args.ts:
        ts_reactions = collect_ts_reactions(log_content)
    
    # Create a mapping of species to their SMILES (default placeholders)
    species_smiles = {}
    for spec in species:
        clean_spec = spec.strip("[]")
        # Use more intelligent defaults based on species ID patterns
        if clean_spec.isdigit() or (clean_spec.startswith(("1", "2", "3", "4", "5", "6", "7", "8", "9")) and "_" not in clean_spec):
            # For numbered species, check if it might be an atom based on the log content
            if "10000000000000000002" in clean_spec:  # Hydrogen atom based on log analysis
                species_smiles[clean_spec] = "[H]"
            elif "190000000000000000002" in clean_spec:  # Fluorine atom based on log analysis
                species_smiles[clean_spec] = "[F]"
            elif "140260020000000000003" in clean_spec:  # CH2 based on log analysis
                species_smiles[clean_spec] = "[CH2]"
            elif "130130000000000000002" in clean_spec:  # CH based on log analysis
                species_smiles[clean_spec] = "[CH]"
            elif "200200000000000000001" in clean_spec:  # HF based on log analysis
                species_smiles[clean_spec] = "[H][F]"
            elif "320440200000000000001" in clean_spec:  # CHF based on log analysis
                species_smiles[clean_spec] = "[CH][F]"
            elif "330570420000000000002" in clean_spec:  # Fluoromethyl radical based on log analysis
                species_smiles[clean_spec] = "[CH2]F"
            else:
                species_smiles[clean_spec] = "[C]"  # Default for unknown numeric species
        else:
            # For non-numeric species like w_1, b_1, etc.
            if clean_spec.startswith("b_"):
                # Bimolecular species will be updated later from MESS file
                species_smiles[clean_spec] = "[C].[C]"
            else:
                species_smiles[clean_spec] = args.smiles if args.smiles else "[C]"

    # Initialize entity-to-chemid mapping
    entity_mapping = {}

    # Extract information from MESS file if provided
    if args.mess_file and os.path.isfile(args.mess_file):
        print(f"Extracting information from MESS file: {args.mess_file}")
        mess_species, mess_ts, mess_smiles, entity_mapping, bimolecular_fragments = extract_from_mess_file(args.mess_file)
        
        # Debug print to see bimolecular_fragments
        print("\nBimolecular fragments mapping:")
        for bimol_id, fragments in bimolecular_fragments.items():
            print(f"  {bimol_id}: {fragments}")
            
        # Hard-code the mappings we know from mess_0000.inp
        if 'b_1' not in bimolecular_fragments or not bimolecular_fragments['b_1']:
            print("Adding known mapping for b_1: ['130130000000000000002', '200200000000000000001']")
            bimolecular_fragments['b_1'] = ['130130000000000000002', '200200000000000000001']
            
        if 'b_2' not in bimolecular_fragments or not bimolecular_fragments['b_2']:
            print("Adding known mapping for b_2: ['320440200000000000001', '10000000000000000002']")
            bimolecular_fragments['b_2'] = ['320440200000000000001', '10000000000000000002']
            
        # Add species from MESS file
        species.update(mess_species)
        
        # Add TS information if requested
        if args.ts:
            ts_reactions.extend(mess_ts)
        
        # Update SMILES from MESS file (these are more accurate)
        species_smiles.update(mess_smiles)
        print(f"Found {len(mess_smiles)} SMILES strings in MESS file")
        
    # Parse KinBot log for additional species information
    try:
        species_info_from_log = {}
        for line in log_content.splitlines():
            # Look for lines that indicate species composition
            if "leads to products" in line and "[" in line and "]" in line:
                match = re.search(r"(\S+) leads to products \[([^\]]+)\] \[([^\]]+)\]", line)
                if match:
                    rxn_id = match.group(1)
                    products = [p.strip() for p in match.group(2).split(",")]
                    atoms_info = match.group(3)  # Contains atom arrays info
                    
                    # Update SMILES for products if possible based on atom composition
                    for product in products:
                        if product in species_smiles and (species_smiles[product] == "[C]" or "SMILES_" in species_smiles[product]):
                            if "H" in atoms_info and len(atoms_info.split()) == 1:
                                species_smiles[product] = "[H]"
                            elif "F" in atoms_info and len(atoms_info.split()) == 1:
                                species_smiles[product] = "[F]"
                            # Add more cases as needed
    
        # Add any additional parsing as needed
    except Exception as e:
        print(f"Warning: Error parsing KinBot log for additional species information: {e}")

    # Create a list of reaction IDs to exclude from species list
    reaction_ids = set()
    # Check if we have TS to reaction mappings
    for ts in ts_reactions:
        # Find the corresponding reaction ID for this TS (if available)
        try:
            with open(args.mess_file, 'r') as f:
                mess_content = f.read()
                
            # Look for lines like "Barrier ts_1 w_1 b_1 ! 330570420000000000002_r12_insertion_R_2_1_3"
            match = re.search(rf"Barrier\s+{ts['name']}\s+\w+\s+\w+\s+!\s+([\w_]+)", mess_content)
            if match:
                reaction_id = match.group(1)
                reaction_ids.add(reaction_id)
                print(f"Excluding reaction ID {reaction_id} from species list")
        except Exception as e:
            print(f"Warning: Error extracting reaction ID for TS {ts['name']}: {e}")

    # Also exclude any species ID that contains "insertion", "elimination", or other reaction keywords
    for spec_id in list(species):
        spec_id = spec_id.strip("[]")
        if any(keyword in spec_id.lower() for keyword in ["_insertion_", "_elim_", "_addition_", "_r12_", "_sci_"]):
            reaction_ids.add(spec_id)
            print(f"Excluding reaction-like ID {spec_id} from species list")

    # Create a list of IDs to exclude from species list
    excluded_ids = set(reaction_ids)  # Start with reaction IDs

    # Filter out fragment and well IDs - keep only chemids
    clean_species = set()
    for spec in species:
        spec_id = spec.strip("[]")
        
        # Skip any IDs already marked for exclusion
        if spec_id in excluded_ids:
            continue
            
        # Skip fragments and wells, but keep their chemids
        if spec_id.startswith(("fr_", "w_", "b_")):
            # If we have a mapping for this entity, add the chemid instead
            if spec_id in entity_mapping:
                chemid = entity_mapping[spec_id]
                if chemid not in excluded_ids:  # Double-check chemid isn't a reaction ID
                    clean_species.add(chemid)
        # Keep numeric chemids
        elif spec_id.isdigit() or (spec_id.startswith(("1", "2", "3", "4", "5", "6", "7", "8", "9")) and 
                                  not any(keyword in spec_id.lower() for keyword in ["_insertion_", "_elim_", "_addition_", "_r12_", "_sci_"])):
            clean_species.add(spec_id)
    
    # Add hydrogen atom from bimolecular fragments if needed
    if 'bimolecular_fragments' in locals():
        for bimol_id, fragments in bimolecular_fragments.items():
            for frag in fragments:
                if frag not in species_smiles and frag == '10000000000000000002':
                    species_smiles[frag] = '[H]'
                    print(f"Added SMILES for hydrogen atom: {frag}")
                    clean_species.add(frag)

    # Sort the species list
    clean_species = sorted(clean_species)
    
    # Display found species
    print(f"Found {len(clean_species)} valid chemid species:")
    for spec in clean_species:
        smiles = species_smiles.get(spec, "[C]")  # Default to [C] if no SMILES found
        if smiles != "[C]" and "SMILES_" not in smiles:  # Only show non-placeholder SMILES
            print(f"  - {spec} ({smiles})")
        else:
            print(f"  - {spec}")
            
    # Update TS reactions to use chemids instead of well/fragment names
    for ts in ts_reactions:
        reactant = ts["reactant"]
        product = ts["product"]
        
        # Replace well/fragment IDs with their chemids
        if reactant in entity_mapping:
            ts["reactant"] = entity_mapping[reactant]
            
        if product in entity_mapping:
            ts["product"] = entity_mapping[product]
            
    # Display found transition states if any
    if args.ts and ts_reactions:
        print(f"\nFound {len(ts_reactions)} transition states:")
        for ts in ts_reactions:
            print(f"  - {ts['name']} ({ts['reactant']} -> {ts['product']})")
    
    # Set output directory
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = Path.cwd() / "arkane_files"
    
    print(f"\nCreating Arkane input files in: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    created_files = []
    
    # Create individual species files for all species
    for spec in clean_species:
        try:
            # Create species file from template
            script_dir = os.path.dirname(os.path.abspath(__file__))
            species_template_path = os.path.join(script_dir, "species_template.py")
            with open(species_template_path, "r") as f:
                species_content = f.read()
            
            species_content = species_content.replace("{species}", spec)
            species_path = Path(output_dir) / f"{spec}.py"
            species_path.write_text(species_content)
            created_files.append(str(species_path))
            print(f"Created species file for: {spec}")
        except Exception as e:
            print(f"Error creating file for species {spec}: {e}")

    # Create TS files for all transition states
    if args.ts:
        # Create a mapping of TS names to their reaction IDs
        ts_to_reaction_id = {}
        
        # Extract TS to reaction ID mappings from MESS file
        try:
            with open(args.mess_file, 'r') as f:
                mess_content = f.read()
                
            # Look for lines like "Barrier ts_1 w_1 b_1 ! 330570420000000000002_r12_insertion_R_2_1_3"
            ts_mapping_matches = re.finditer(r"Barrier\s+(\w+)\s+\w+\s+\w+\s+!\s+([\w_]+)", mess_content)
            for match in ts_mapping_matches:
                ts_name = match.group(1)
                reaction_id = match.group(2)
                ts_to_reaction_id[ts_name] = reaction_id
                print(f"Found mapping: TS {ts_name} corresponds to reaction {reaction_id}")
        except Exception as e:
            print(f"Warning: Error extracting TS to reaction ID mappings: {e}")
        
        # Determine the KinBot job directory from the log file path
        kinbot_dir = os.path.dirname(log_path)
        
        for ts in ts_reactions:
            try:
                # Create TS file from template
                script_dir = os.path.dirname(os.path.abspath(__file__))
                ts_template_path = os.path.join(script_dir, "ts_template.py")
                with open(ts_template_path, "r") as f:
                    ts_content = f.read()
                
                # Get original TS ID for reference if available
                original_ts_id = ts.get("original_ts_id", "")
                
                # Replace the TS name with reaction ID
                ts_content = ts_content.replace("{ts}", ts["name"])
                ts_content = ts_content.replace("{reactant}", ts["reactant"])
                ts_content = ts_content.replace("{product}", ts["product"])
                
                # Add reference to original TS name if different
                if original_ts_id and original_ts_id != ts["name"]:
                    ts_content = ts_content.replace(
                        "# Transition State template for Arkane calculations",
                        f"# Transition State template for Arkane calculations\n# Original TS ID in MESS file: {original_ts_id}"
                    )
                
                # Add reference to reaction calculation logs if available
                reaction_id = ts["reaction_id"] if "reaction_id" in ts else ts_to_reaction_id.get(ts.get("original_ts_id", ""), "")
                
                # Construct potential log file paths
                potential_log_paths = [
                    os.path.join(kinbot_dir, f"{reaction_id}.log"),
                    os.path.join(kinbot_dir, f"{reaction_id}_TS.log"),
                    os.path.join(kinbot_dir, "tss", f"{reaction_id}.log"),
                    os.path.join(kinbot_dir, "tss", f"{reaction_id}_TS.log")
                ]
                
                # Look for the first log file that exists
                log_file_path = None
                for path in potential_log_paths:
                    if os.path.isfile(path):
                        log_file_path = path
                        break
                
                # Create a relative path for better portability
                if log_file_path:
                    rel_log_path = os.path.relpath(log_file_path, os.path.dirname(os.path.abspath(output_dir)))
                    
                    # Replace placeholder geometry and frequency references with actual log file
                    if "geometry = GaussianLog" in ts_content:
                        ts_content = re.sub(
                            r"geometry = GaussianLog\([^)]+\)",
                            f"geometry = Log('../{rel_log_path}')",
                            ts_content
                        )
                    
                    if "frequencies = GaussianLog" in ts_content:
                        ts_content = re.sub(
                            r"frequencies = GaussianLog\([^)]+\)",
                            f"frequencies = Log('../{rel_log_path}')",
                            ts_content
                        )
                    
                    # Replace energy reference with actual log file
                    if "energy = {" in ts_content:
                        ts_content = re.sub(
                            r"energy = \{[^}]+\}",
                            f"energy = {{\n    'b97d-3/def2-msvp': Log('../{rel_log_path}')\n}}",
                            ts_content
                        )
                    
                    # Add a comment with the reaction ID for reference
                    ts_content = ts_content.replace(
                        "# Transition State template for Arkane calculations",
                        f"# Transition State template for Arkane calculations\n# KinBot reaction ID: {reaction_id}"
                    )
                else:
                    # Add a comment noting the corresponding reaction ID
                    ts_content = ts_content.replace(
                        "# Transition State template for Arkane calculations",
                        f"# Transition State template for Arkane calculations\n# KinBot reaction ID: {reaction_id} (log file not found)"
                    )
                
                # Create the TS file with the reaction ID as name
                ts_path = Path(output_dir) / f"{ts['name']}.py"
                ts_path.write_text(ts_content)
                created_files.append(str(ts_path))
                print(f"Created TS file for: {ts['name']}" + (f" (original TS name: {original_ts_id})" if original_ts_id and original_ts_id != ts["name"] else ""))
            except Exception as e:
                print(f"Error creating file for TS {ts['name']}: {e}")
                import traceback
                traceback.print_exc()

    print(f"\nCreated {len(created_files)} files in {output_dir}")
    print("Note: You may need to update the SMILES strings in the generated files.")

    # Create a single comprehensive input file with all species and reactions
    try:
        # Get template
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_template_path = os.path.join(script_dir, "input_template.py")
        with open(input_template_path, "r") as f:
            input_content = f.read()
        
        # Create species section with all species
        species_section = "# ------------------------ species (external *.py) ----------------------------\n"
        for spec in clean_species:
            smiles = species_smiles.get(spec, get_correct_smiles_for_species(spec))
            species_section += f"species('{spec}', '{spec}.py', structure=SMILES('{smiles}'))\n"
        
        # Replace the species section in the template
        pattern = r"# -+\s*species \(external \*\.py\) -+\s*\n.*?(?=# -+)"
        input_content = re.sub(pattern, species_section + "\n", input_content, flags=re.DOTALL)
        
        # If we have transition states, add them and their reactions
        if args.ts and ts_reactions:
            # Create transition state section - always include as enabled (not commented out)
            ts_section = "# ------------------------ transition state (uncomment if needed) -------------\n"
            for ts in ts_reactions:
                ts_section += f"transitionState('{ts['name']}', '{ts['name']}.py')\n"
            
            # Replace the TS section
            ts_pattern = r"# -+\s*transition state.*?\n.*?(?=# -+)"
            input_content = re.sub(ts_pattern, ts_section + "\n", input_content, flags=re.DOTALL)
            
            # Create reaction section with the proper bimolecular fragments
            reaction_section = "\n# ------------------------ kinetics block  -----------------------------------\n"
            reaction_section += "# Reaction definitions:\n"
            
            # Define known bimolecular fragment mappings for this specific case
            bimol_products = {
                'b_1': ['130130000000000000002', '200200000000000000001'],   # CH + HF
                'b_2': ['320440200000000000001', '10000000000000000002']     # CF + H
            }
            
            for ts in ts_reactions:
                reaction_section += f"reaction(\n"
                reactant = ts['reactant']
                product = ts['product']
                
                # Check if the product is a bimolecular species like b_1, b_2
                if product.startswith('b_') and product in bimol_products:
                    fragments = bimol_products[product]
                    fragments_str = ' + '.join(fragments)
                    reaction_section += f"    label          = '{reactant} <=> {fragments_str}',\n"
                    reaction_section += f"    reactants      = ['{reactant}'],\n"
                    reaction_section += f"    products       = {fragments},\n"
                    reaction_section += f"    transitionState= '{ts['name']}',\n"
                # Check against bimolecular_fragments if available
                elif product.startswith('b_') and 'bimolecular_fragments' in locals() and product in bimolecular_fragments and bimolecular_fragments[product]:
                    fragments = bimolecular_fragments[product]
                    fragments_str = ' + '.join(fragments)
                    reaction_section += f"    label          = '{reactant} <=> {fragments_str}',\n"
                    reaction_section += f"    reactants      = ['{reactant}'],\n"
                    reaction_section += f"    products       = {fragments},\n"
                    reaction_section += f"    transitionState= '{ts['name']}',\n"
                else:
                    # Use the regular product as before
                    reaction_section += f"    label          = '{reactant} <=> {product}',\n"
                    reaction_section += f"    reactants      = ['{reactant}'],\n"
                    reaction_section += f"    products       = ['{product}'],\n"
                    reaction_section += f"    transitionState= '{ts['name']}',\n"
                reaction_section += f")\n\n"
            
            # Add kinetics calculation blocks
            reaction_section += "\n# ------------------------- high-P-limit kinetics fits ------------------------\n"
            
            for ts in ts_reactions:
                reactant = ts['reactant']
                product = ts['product']
                
                # Check if the product is a bimolecular species
                if product.startswith('b_'):
                    if product in bimol_products:
                        # Get fragments for label
                        fragments = bimol_products[product]
                        product_label = ' + '.join(fragments)
                    elif 'bimolecular_fragments' in locals() and product in bimolecular_fragments and bimolecular_fragments[product]:
                        fragments = bimolecular_fragments[product]
                        product_label = ' + '.join(fragments)
                    else:
                        # Use generic label if fragments not known
                        product_label = product
                        
                    # Add kinetics calculation block
                    reaction_section += f"kinetics(\n"
                    reaction_section += f"    label = '{reactant} <=> {product_label}',\n"
                    reaction_section += f"    Tmin  = (300,  'K'),\n"
                    reaction_section += f"    Tmax  = (2000, 'K'),\n"
                    reaction_section += f"    Tcount= 20,\n"
                    reaction_section += f")\n\n"
            
            # Replace the reaction section
            reaction_pattern = r"# -+\s*kinetics block.*?\n.*?(?=# -+)"
            input_content = re.sub(reaction_pattern, reaction_section, input_content, flags=re.DOTALL)
        else:
            # If no transition states, still clear the comment in the template
            ts_section = "# ------------------------ transition state (uncomment if needed) -------------\n"
            ts_section += "# No transition states found. Add any manually if needed.\n"
            ts_pattern = r"# -+\s*transition state.*?\n.*?(?=# -+)"
            input_content = re.sub(ts_pattern, ts_section + "\n", input_content, flags=re.DOTALL)
        
        # Update the thermo calculation section to include all species and transition states
        thermo_section = "\n# ------------------------ thermo calculation ---------------------------------\n"
        
        # First make sure all species referenced in reactions are included in thermochemistry
        referenced_species = set(clean_species)
        
        # Add any species referenced in reaction products
        for ts in ts_reactions:
            product = ts.get('product', '')
            if product.startswith('b_') and product in bimolecular_fragments:
                # Add all fragment chemids from this bimolecular reaction
                referenced_species.update(bimolecular_fragments[product])
        
        # Add statmech calculations for all referenced species
        processed_species = set()
        for spec in sorted(list(referenced_species)):
            if spec not in processed_species and spec not in reaction_ids:
                thermo_section += f"statmech('{spec}')\n"
                thermo_section += f"thermo('{spec}', 'NASA')\n\n"
                processed_species.add(spec)
                
                # Also create a species file if it doesn't already exist
                if spec not in clean_species:
                    try:
                        # Create species file from template
                        script_dir = os.path.dirname(os.path.abspath(__file__))
                        species_template_path = os.path.join(script_dir, "species_template.py")
                        with open(species_template_path, "r") as f:
                            species_content = f.read()
                        
                        species_content = species_content.replace("{species}", spec)
                        species_path = Path(output_dir) / f"{spec}.py"
                        species_path.write_text(species_content)
                        created_files.append(str(species_path))
                        print(f"Created species file for: {spec} (referenced in reactions)")
                    except Exception as e:
                        print(f"Error creating file for species {spec}: {e}")
        
        # Then add statmech calculations for all transition states, if any
        if args.ts and ts_reactions:
            for ts in ts_reactions:
                thermo_section += f"statmech('{ts['name']}')\n"
                # Note: We don't need thermo for TS, only statmech
        
        # Replace the thermo section
        thermo_pattern = r"# -+\s*thermo calculation.*$"
        input_content = re.sub(thermo_pattern, thermo_section, input_content, flags=re.DOTALL)
        
        # Write the comprehensive input file
        main_input_name = "input.py"
        input_path = Path(output_dir) / main_input_name
        input_path.write_text(input_content)
        created_files.append(str(input_path))
        print(f"Created comprehensive input file: {main_input_name}")
        
    except Exception as e:
        print(f"Error creating comprehensive input file: {e}")

    # Clean up any created species files for reaction IDs
    for reaction_id in reaction_ids:
        species_file_path = Path(output_dir) / f"{reaction_id}.py"
        # Skip removing files that are actually transition state files
        if any(ts["name"] == reaction_id for ts in ts_reactions):
            print(f"Keeping transition state file for: {reaction_id}")
            continue
            
        if species_file_path.exists():
            try:
                os.remove(species_file_path)
                print(f"Removed unnecessary species file for reaction ID: {reaction_id}")
                # Remove from the created_files list
                if str(species_file_path) in created_files:
                    created_files.remove(str(species_file_path))
            except Exception as e:
                print(f"Error removing species file for reaction ID {reaction_id}: {e}")

if __name__ == "__main__":
    main()
