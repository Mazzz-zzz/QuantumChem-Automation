#!/usr/bin/env python

"""
Script to generate Gaussian input files for reaction optimization study using SMILES
"""

import os
import argparse
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem

def get_connectivity_matrix(mol):
    """Generate connectivity matrix from RDKit molecule"""
    connectivity = []
    for atom in mol.GetAtoms():
        idx = atom.GetIdx() + 1  # 1-based indexing for Gaussian
        bonds = []
        for bond in atom.GetBonds():
            other_idx = bond.GetOtherAtomIdx(atom.GetIdx()) + 1
            if other_idx > idx:  # Only include forward connections
                bonds.append(f"{other_idx} 1.0")
        if bonds:
            connectivity.append(f"{idx} " + " ".join(bonds))
        else:
            connectivity.append(f"{idx}")
    return connectivity

def create_freq_input(mol, name, charge, multiplicity, output_dir="gaussian_jobs"):
    """Create a Gaussian input file with parameters"""
    output_path = Path(output_dir) / f"{name}_freq.gjf"
    
    with open(output_path, 'w') as f:
        f.write(f"%chk={Path(output_dir) / f'{name}.chk'}\n")
        # Header
        f.write("%mem=10GB\n")
        f.write("%nprocshared=8\n")
        # wb97xd/6-311++G(d,p) instead of M062X/6-31G(2df,p)
        # keep it as M062X/6-31G(2df,p)
        f.write("#P iop(7/33=1) opt=calcfc freq M062X/6-31G(2df,p) scf=tight nosym scfcyc=6000\n\n")
        
        # Title
        f.write(f"{name} - optimisation + frequencies (final coordinates)\n\n")
        
        # Charge and multiplicity
        f.write(f"{charge} {multiplicity}\n")
        
        # Coordinates
        conf = mol.GetConformer()
        for i, atom in enumerate(mol.GetAtoms()):
            pos = conf.GetAtomPosition(i)
            f.write(f"{atom.GetSymbol():2s}    {pos.x:10.6f}    {pos.y:10.6f}    {pos.z:10.6f}\n")
        
        # Connectivity matrix
        f.write("\n")
        connectivity = get_connectivity_matrix(mol)
        for line in connectivity:
            f.write(line + "\n")
        
        # End with blank line
        f.write("\n")

def create_B97D3_input(mol, name, charge, multiplicity, output_dir="gaussian_jobs"):
    """Create a B97D3/Def2SVP Gaussian input file with parameters"""
    output_path = Path(output_dir) / f"{name}_B97D3.gjf"
    
    with open(output_path, 'w') as f:
        f.write(f"%chk={Path(output_dir) / f'{name}.chk'}\n")
        # Header
        f.write("%mem=4GB\n")
        f.write("%nprocshared=8\n")
        # B97D3/Def2SVP EmpiricalDispersion=GD3BJ NOSYM OPTCYC=100 SCF=TIGHT
        # no EmpiricalDispersion=GD3BJ
        f.write("#P iop(7/33=1) opt=calcfc freq B97D3/Def2SVP EmpiricalDispersion=GD3BJ scf=tight nosym scfcyc=6000\n\n")
        # Title
        f.write(f"{name} - B97D3/Def2SVP geometry optimization\n\n")
        
        # Charge and multiplicity
        f.write(f"{charge} {multiplicity}\n")
        
        # Coordinates
        conf = mol.GetConformer()
        for i, atom in enumerate(mol.GetAtoms()):
            pos = conf.GetAtomPosition(i)
            f.write(f"{atom.GetSymbol():2s}    {pos.x:10.6f}    {pos.y:10.6f}    {pos.z:10.6f}\n")
        
        # Connectivity matrix
        f.write("\n")
        connectivity = get_connectivity_matrix(mol)
        for line in connectivity:
            f.write(line + "\n")
        
        # End with blank line
        f.write("\n")

def create_geom_input(mol, name, charge, multiplicity, output_dir="gaussian_jobs"):
    """Create a geometry optimization Gaussian input file"""
    output_path = Path(output_dir) / f"{name}_geom.gjf"
    
    with open(output_path, 'w') as f:
        f.write(f"%chk={Path(output_dir) / f'{name}.chk'}\n")
        f.write("%mem=3800MB\n")
        f.write("%nprocshared=8\n")
        #use wb97xd/6-311++G(d,p) instead of M062X/6-31G(2df,p)
        f.write("# opt=(maxcyc=999,noeigen) wb97xd/aug-cc-pVTZ NOSYM int=superfine scf=(verytight,xqc)\n\n")
        
        f.write(f"{name} - wb97xd/6-311++G(d,p) Geometry Optimization (verytight, superfine)\n\n")
        
        f.write(f"{charge} {multiplicity}\n")
        
        conf = mol.GetConformer()
        for i, atom in enumerate(mol.GetAtoms()):
            pos = conf.GetAtomPosition(i)
            f.write(f"{atom.GetSymbol():2s}    {pos.x:10.6f}    {pos.y:10.6f}    {pos.z:10.6f}\n")
        
        f.write("\n")
        connectivity = get_connectivity_matrix(mol)
        for line in connectivity:
            f.write(line + "\n")
        
        f.write("\n")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate Gaussian input files for molecules')
    parser.add_argument('--label', type=str, required=True, help='Molecule label/name')
    parser.add_argument('--smiles', type=str, required=True, help='SMILES string of the molecule')
    parser.add_argument('--charge', type=int, default=0, help='Molecular charge (default: 0)')
    parser.add_argument('--multiplicity', type=int, default=1, help='Spin multiplicity (default: 1)')
    parser.add_argument('--output-dir', type=str, default='gaussian_jobs', help='Output directory for Gaussian files')
    return parser.parse_args()

def main():
    # Parse command line arguments
    args = parse_arguments()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        # Create RDKit molecule from SMILES
        mol = Chem.MolFromSmiles(args.smiles)
        if mol is None:
            raise ValueError(f"Failed to create molecule from SMILES: {args.smiles}")
        
        # Add hydrogens
        mol = Chem.AddHs(mol)
        
        # Generate 3D coordinates
        AllChem.EmbedMolecule(mol, randomSeed=42)
        
        # Optimize with MMFF94
        AllChem.MMFFOptimizeMolecule(mol)
        
        # Create frequency calculation input file
        create_freq_input(
            mol=mol,
            name=args.label,
            charge=args.charge,
            multiplicity=args.multiplicity,
            output_dir=args.output_dir
        )
        
        # Create B97D3 geometry optimization input file
        #create_B97D3_input(
        #    mol=mol,
        #    name=args.label,
        #    charge=args.charge,
        #    multiplicity=args.multiplicity,
        #    output_dir=args.output_dir
        #)

        # Create geometry optimization input file with wb97xd/6-311++G(d,p)
        create_geom_input(
            mol=mol,
            name=args.label,
            charge=args.charge,
            multiplicity=args.multiplicity,
            output_dir=args.output_dir
        )
        
        print(f"Created input files for {args.label}")
        
    except Exception as e:
        print(f"Error processing {args.label}: {str(e)}")

if __name__ == "__main__":
    main() 