#!/usr/bin/env python

import re
import os
import requests


def extract_accessions(fasta_file_path):
    with open(fasta_file_path, "r") as f:
        fasta_seq = f.readlines()
    uniprot_accessions = []
    for line in fasta_seq:
        if line.startswith('>sp'):
            uniprot_accessions.append(line.split('|')[1])
    return list(set(uniprot_accessions))


def search_pdb_by_accession(accession):
    """Search the RCSB PDB API for protein structures by gene name and return a list of PDB IDs"""
    search_url = 'https://search.rcsb.org/rcsbsearch/v2/query?json={search-request}'

    query ={
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession",
                        "operator": "in",
                        "negation": False,
                        "value": [
                            accession
                        ]
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "entity_poly.rcsb_sample_sequence_length",
                        "operator": "greater_or_equal",
                        "negation": False,
                        "value": 200
                    }
                }
            ],
            "label": "text"
        },
        "return_type": "entry",
        "request_options": {
            "return_all_hits": True,
            "results_content_type": [
                "computational",
                "experimental"
            ]
         }

    }

    # Send a POST request to the RCSB PDB API to perform the search
    response = requests.post(search_url, json=query)

    # Parse the search results to get a list of PDB IDs
    pdb_ids = []
    if response.ok and response.text:
        search_results = response.json().get('result_set', [])
        pdb_ids = [entry['identifier'] for entry in search_results]
    return pdb_ids

def convert_string(input_string):
    # Extract the parts of the input string using regex
    match = re.match(r"(AF)_(\w{8})(\w{2})", input_string)
    if match:
        prefix = match.group(1)
        middle = match.group(2)[2:]
        suffix = match.group(3)
        # Construct the output string
        output_string = f"{prefix}-{middle}-{suffix}-model_v4"
        return output_string
    else:
        return input_string

def download_pdb_files_by_acc(pdb_ids, accession, save_path):
    """Download PDB files for a list of PDB IDs and save them to a directory named after the gene name"""

    for pdb_id in pdb_ids:
        pdb_id = convert_string(pdb_id)
        if 'AF-' in pdb_id:
            pdb_file_path = os.path.join(save_path, f'{pdb_id}.pdb')
            if os.path.exists(pdb_file_path):
                print(f'{pdb_id}.pdb already exists in the directory')
                continue
            response2 = requests.get(f'https://alphafold.ebi.ac.uk/files/{pdb_id}.pdb')
            if response2.ok:
                with open(pdb_file_path, 'w') as outfile:
                    outfile.write(requests.get(f'https://alphafold.ebi.ac.uk/files/{pdb_id}.pdb').text)
                print(f'Retrieved {pdb_id}.pdb')
            else:
                print(f'Failed to retrieve {pdb_id}.pdb')

        else:
            pdb_file_path = os.path.join(save_path, f'{pdb_id}_{accession}.pdb')
            if os.path.exists(pdb_file_path):
                print(f'{pdb_id}.pdb already exists in the directory')
                continue
            response = requests.get(f'https://files.rcsb.org/download/{pdb_id}.pdb')
            if response.ok:
                with open(pdb_file_path, 'w') as outfile:
                    outfile.write(response.text)
                print(f'Retrieved {pdb_id}.pdb')
            else:
                print(f'Failed to retrieve {pdb_id}.pdb')
