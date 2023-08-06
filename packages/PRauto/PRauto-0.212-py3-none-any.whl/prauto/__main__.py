#!/usr/bin/env python

from .retriever.get_fasta import *
from .retriever.get_pdb import *
from .retriever.get_ligand import *
from tqdm.auto import tqdm
from tkinter import Tk
from tkinter import filedialog

root = Tk()
root.withdraw()

mult = '\n' * 3
global search_key


def main():
    global search_key
    print(f'Step1: Retrieve FASTA files{mult}')
    print(f"""
    
########################################################################################################

This is a bulk data retrieval version of Prauto.

To make prauto work properly, the Directory, Protein Name, and Gene Name 
should have been entered in the format of prauto_order_form.csv
                                                  
#########################################################################################################
                                                                                            """)
    order_form = filedialog.askopenfilename(title='Select the order_form')
    with open(order_form, "r", encoding='UTF-8') as f:
        lines = f.readlines()[1:]
        for line in lines:
            target_dir = line.split(",")[0]
            os.chdir(target_dir)

            search_key = line.split(",")[1]
            gene_name = line.split(",")[2].strip('\n')
            dir_name = line.split(",")[2].strip('\n')
            fasta_file_path = download_fasta(search_key, dir_name)
            fasta_file_path = remove_outlier(search_key, gene_name, fasta_file_path)
            pdb_dir = os.path.dirname(fasta_file_path)

            print(f'Step2: Retrieve PDB files{mult}')
            accessions_list = extract_accessions(fasta_file_path)
            for accession in accessions_list:
                pdb_ids = search_pdb_by_accession(accession)
                if pdb_ids:
                    print(f'\nFound {len(pdb_ids)} PDB entries for {accession}')
                    download_pdb_files_by_acc(pdb_ids, accession, pdb_dir)

            print(f'Step3: Retrieve sdf files{mult}')
            for accession in accessions_list:
                sdf_file = os.path.join(pdb_dir, "ligands", f"{gene_name}_{accession}_ligands.sdf")
                if os.path.exists(sdf_file):
                    continue
                else:
                    retry_count = 0
                    max_retries = 100
                    while retry_count < max_retries:
                        try:
                            download_chembl_compounds(accession, pdb_dir, gene_name)
                            break  # Download successful, exit the retry loop
                        except Exception as e:
                            print(f"Error occurred: {str(e)}")
                            print(f"Retrying in 5 seconds... (retry count: {retry_count + 1}/{max_retries})")
                            time.sleep(5)  # Wait for 5 seconds before retrying
                            retry_count += 1
                    else:
                        print(f"Failed to download compounds for accession {accession} after {max_retries} retries.")

if __name__ == "__main__":
    main()