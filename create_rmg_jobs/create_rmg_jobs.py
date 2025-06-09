#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import shutil
from string import Template


def create_rmg_input(species_name, smiles, output_dir=None):
    """
    Generate RMG input file from template for a given species.
    
    Args:
        species_name (str): Name of the species
        smiles (str): SMILES representation of the species
        output_dir (str, optional): Directory to save the file. If None, uses current directory.
    """
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to templates
    templates_dir = os.path.join(os.path.dirname(script_dir), "templates")
    rmg_template_path = os.path.join(templates_dir, "rmg_input.py")
    
    # Create output directory if specified
    if output_dir is None:
        output_dir = os.getcwd()
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create RMG input file
    rmg_output_path = os.path.join(output_dir, f"rmg_input_{species_name}.py")
    
    with open(rmg_template_path, 'r') as f:
        rmg_template_raw = f.read()
    
    # Change placeholders to Template placeholders
    rmg_template_raw = rmg_template_raw.replace('{species}', '${species}').replace('{smiles}', '${smiles}')

    rmg_content = Template(rmg_template_raw).substitute(
        species=species_name,
        smiles=smiles
    )
    
    with open(rmg_output_path, 'w') as f:
        f.write(rmg_content)
    
    print(f"Created RMG input file: {rmg_output_path}")
    
    return rmg_output_path


def main():
    parser = argparse.ArgumentParser(description='Create RMG input file from template')
    parser.add_argument('--species', '-s', required=True, help='Species name')
    parser.add_argument('--smiles', '-m', required=True, help='SMILES representation')
    parser.add_argument('--output', '-o', help='Output directory')
    
    args = parser.parse_args()
    
    create_rmg_input(
        species_name=args.species,
        smiles=args.smiles,
        output_dir=args.output
    )


if __name__ == "__main__":
    main()
