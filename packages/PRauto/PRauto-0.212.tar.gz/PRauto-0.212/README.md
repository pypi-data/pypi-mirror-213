# PRauto
 
#### PRauto is a tool that provides two main functionalities: [ Data Retrieval ] and [ Data Preprocessing ]                                                               in Bioinformatic and Chemoinformatics.
_______________________________________________________________________________________________________________________________________
### Install
To install the PRauto, users can input the following command in the command-line interface:
  
```bash
   pip install PRauto
```
If you have problems with PyMOL dependency, try:
```bash
   conda install -c conda-forge pymol-open-source
```

###
### Data Retrieval
  
#### To use the Data Retrieval feature, users can input the following command in the command-line interface:

```bash
   python -m prauto.retriever
```
   
   
![PRauto_retrieve map](https://user-images.githubusercontent.com/96029849/233053221-6cd73e81-9836-496d-b917-d4b31e02308f.png)

This tool allows users to retrieve the FASTA file of a target protein sequence via a search query in the UniProt API.  
Additionally, using the UniProt accession number, PRauto retrieves the PDB files of target protein from the RCSB PDB API and  
sdf files of ligands that interact with the target protein from the ChEMBL API.

#### The output of this feature includes : 
1. the target protein sequences in a FASTA file format 
2. PDB files of the target protein structures
3. sdf files of the ligands that interact with the target protein

________________________________________________________________________________________________________________________________________
###
### Data Preprocessing

#### To use the Data Preprocessing feature, users can input the following command in the command-line interface:

```bash
   python -m prauto.prepauto
```
   
   
![PRauto_prep drawio](https://user-images.githubusercontent.com/96029849/233054348-8caf262e-c06e-4b72-bb4e-3ea624830e06.png)

This tool processes PDB files that are located in a single directory.  
It extracts only the chain(s) that correspond to the target protein and aligns them according to the reference PDB file.  
It also removes any unnecessary molecules that are not involved in the binding of the primary ligand.  
In a PSE PyMOL session, these unnecessary molecules are hidden rather than being removed.

#### The output of this feature includes : 
1. preprocessed PDB files
2. PSE PyMOL session file.

___________________________________________________________________________________________________________________________________________
