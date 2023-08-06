import os
from setuptools import setup, find_packages, Extension
import setuptools
with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(name='PRauto',
        version = '0.212',
        packages = find_packages(include=['prauto','prauto.*']),
        url = 'https://github.com/KimJisanER/PRauto',
        license = 'MIT license',
        author = 'Ji San Kim',
        author_email = 'jisan1233@gmail.com',
        keywords = 'PDB, FASTA, sdf, Automation',
        description = """
        PRauto is a package for collecting and preprocessing protein and ligand data. 
        
        ## With prauto.py, you can perform the following tasks for a target protein:

           1. Collect FASTA file using Uniprot API
           2. Collect PDB file using RCSB PDB API
           3. Collect sdf file using ChEMBL API
        
        ## With get_preprocess.py, you can perform the following tasks:

           1. Extract the target chain from collected PDB files
           2. Align PDB files based on a chosen criterion
           3. Remove unnecessary molecules such as solvents and reagents from PDB files""",
        python_requires = '>=3',
        install_requires = required)

