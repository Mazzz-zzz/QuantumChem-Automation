#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import shutil
from string import Template


def create_arkane_input(species_name, smiles, output_dir=None):
    """
    Generate Arkane input files from templates for a given species.
    
    Args:
        species_name (str): Name of the species
        smiles (str): SMILES representation of the species
        output_dir (str, optional): Directory to save the files. If None, uses current directory.
    """
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to templates
    templates_dir = os.path.join(os.path.dirname(script_dir), "templates")
    arkane_template_path = os.path.join(templates_dir, "arkane_template.py")
    species_template_path = os.path.join(templates_dir, "my_species_template.py")
    
    # Create output directory if specified
    if output_dir is None:
        output_dir = os.getcwd()
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create Arkane input file
    arkane_output_path = os.path.join(output_dir, f"input_{species_name}.py")
    
    with open(arkane_template_path, 'r') as f:
        arkane_template_raw = f.read()
    
    # Change curly-brace placeholders to Template placeholders (e.g. {species} → ${species})
    # Using the brace syntax prevents unintended concatenation with following characters (e.g., "${species}_geom")
    arkane_template_raw = arkane_template_raw.replace('{species}', '${species}').replace('{smiles}', '${smiles}')

    arkane_content = Template(arkane_template_raw).substitute(
        species=species_name,
        smiles=smiles
    )
    
    with open(arkane_output_path, 'w') as f:
        f.write(arkane_content)
    
    # Create species file
    species_output_path = os.path.join(output_dir, f"my_{species_name}.py")
    
    with open(species_template_path, 'r') as f:
        species_template_raw = f.read()
    
    species_template_raw = species_template_raw.replace('{species}', '${species}')

    species_content = Template(species_template_raw).substitute(
        species=species_name,
    )
    
    with open(species_output_path, 'w') as f:
        f.write(species_content)
    
    print(f"Created Arkane input file: {arkane_output_path}")
    print(f"Created species file: {species_output_path}")
    
    return arkane_output_path, species_output_path


def main():
    parser = argparse.ArgumentParser(description='Create Arkane input files from templates')
    parser.add_argument('--species', '-s', required=True, help='Species name')
    parser.add_argument('--smiles', '-m', required=True, help='SMILES representation')
    parser.add_argument('--output', '-o', help='Output directory')
    
    args = parser.parse_args()
    
    create_arkane_input(
        species_name=args.species,
        smiles=args.smiles,
        output_dir=args.output
    )


if __name__ == "__main__":
    main()
