#!/usr/bin/env python

import os
from chembl_webresource_client.settings import Settings
from chembl_webresource_client.new_client import new_client
from functools import lru_cache
from tqdm import tqdm
from itertools import islice

def chunked_iterable(iterable, chunk_size):
    iterator = iter(iterable)
    while True:
        chunk = list(islice(iterator, chunk_size))
        if not chunk:
            break
        yield chunk

def download_chembl_compounds(accession, save_path,gene_name):
    # Create the "ligands" directory if it does not exist
    if not os.path.exists(os.path.join(save_path, "ligands")):
        os.makedirs(os.path.join(save_path, "ligands"))

    targets_api = new_client.target
    compounds_api = new_client.molecule
    bioactivities_api = new_client.activity

    targets = targets_api.get(
        target_components__accession=accession,
        target_type__in=['SINGLE PROTEIN', 'PROTEIN FAMILY']
    ).only("target_chembl_id")
    targets_id = list(set([target['target_chembl_id'] for target in targets]))

    if len(targets_id) != 0:
        target_columns_list = ['assay_chembl_id', 'molecule_chembl_id', 'molecule_name', 'molecule_max_phase', 'molecular_weight', 'alogp',
                               'standard_type', 'standard_relation', 'standard_value', 'standard_units',
                               'pchembl_value', 'assay_type', 'target_name', 'target_organism', 'target_type']

        for target in targets_id:

            bioactivities = bioactivities_api.filter(target_chembl_id=target,
                                                     standard_type__in=["IC50", "EC50", "Ki", "Kd"],
                                                     assay_type__in=["B", "F"], relation__in=['=', '<', '<=']).only(
                *target_columns_list)

            bioactivities_list = list(bioactivities)

            compound_columns_list = ["molecule_chembl_id", 'molecule_structures', 'molecule_properties', 'mw_freebase']
            for bioactivity_chunk in chunked_iterable(bioactivities_list, 100):
                compounds = compounds_api.filter(
                    molecule_type='Small molecule',
                    molecule_chembl_id__in=[x['molecule_chembl_id'] for x in bioactivity_chunk],
                    molecule_properties__mw_freebase__lte=700,
                    molfile__isnull=False
                ).only(*compound_columns_list)

                compounds_list = [record for record in compounds]

                if len(compounds_list) != 0:
                    for record in tqdm(compounds_list, total=len(compounds_list),
                                       desc=f'Retrieving ligands for {accession}'):
                        if record.get('molecule_structures') and record['molecule_structures'].get('molfile') is not None:

                            mol_id = record['molecule_chembl_id']
                            file_name = f"{accession}_{mol_id}.sdf"
                            file_path = os.path.join(save_path, "ligands", file_name)
                            if os.path.exists(file_path):
                                continue
                            mol_file = ''
                            molfile = record['molecule_structures']['molfile']
                            targets_chembl = f"> <target_chembl_id>\n{target}\n"
                            # target_accession 추후에 뺄지 정하기
                            target_accession = f"\n> <target_accession>\n{accession}\n"
                            mw_freebase = f"\n> <mw_freebase>\n{record['molecule_properties']['mw_freebase']}\n"
                            alogp = f"\n> <alogp>\n{record['molecule_properties']['alogp']}\n"
                            mol_file += molfile
                            mol_file += targets_chembl
                            mol_file += target_accession
                            mol_file += mw_freebase
                            mol_file += alogp
                            mol_file += "\n> <bioactivities>\n"

                            pChEMBL_ki = 0
                            pChEMBL_kd = 0
                            pChEMBL_ec = 0
                            pChEMBL_ic = 0

                            for i in bioactivities_list:
                                if i['molecule_chembl_id'] == record['molecule_chembl_id']:
                                    bioactivities_str = f"assay_chembl_id: {i['assay_chembl_id']}, assay_type: {i['assay_type']}, pchembl_value: {i['pchembl_value']}, {i['standard_type']}{i['standard_relation']}{i['standard_value']}{i['standard_units']}\n"
                                    mol_file += bioactivities_str

                                    if i['standard_type'] =='Ki' and i['pchembl_value'] is not None:
                                            if float(i['pchembl_value']) > float(pChEMBL_ki):
                                                pChEMBL_ki = str(i['pchembl_value'])

                                    if i['standard_type'] =='Kd' and i['pchembl_value'] is not None:
                                            if float(i['pchembl_value']) > float(pChEMBL_kd):
                                                pChEMBL_kd = str(i['pchembl_value'])

                                    if i['standard_type'] =='IC50' and i['pchembl_value'] is not None:
                                            if float(i['pchembl_value']) > float(pChEMBL_ic):
                                                pChEMBL_ic = str(i['pchembl_value'])

                                    if i['standard_type'] =='EC50' and i['pchembl_value'] is not None:
                                            if float(i['pchembl_value']) > float(pChEMBL_ec):
                                                pChEMBL_ec = str(i['pchembl_value'])

                            pChEMBL_value_Ki = f"\n> <pChEMBL_value_Ki>\n{pChEMBL_ki}\n".replace("\n0\n", "\nNone\n")
                            pChEMBL_value_Kd = f"\n> <pChEMBL_value_Kd>\n{pChEMBL_kd}\n".replace("\n0\n", "\nNone\n")
                            pChEMBL_value_IC50 = f"\n> <pChEMBL_value_IC50>\n{pChEMBL_ic}\n".replace("\n0\n", "\nNone\n")
                            pChEMBL_value_EC50 = f"\n> <pChEMBL_value_EC50>\n{pChEMBL_ec}\n".replace("\n0\n", "\nNone\n")

                            mol_file += pChEMBL_value_Ki
                            mol_file += pChEMBL_value_Kd
                            mol_file += pChEMBL_value_IC50
                            mol_file += pChEMBL_value_EC50

                            with open(file_path, 'w') as outfile:
                                outfile.write(mol_file)
    merge_sdf_files(os.path.join(save_path, "ligands"), gene_name, accession)

def merge_sdf_files(sdf_directory, gene_name, accession):
    # List the filenames of the input SDF files
    files = os.listdir(sdf_directory)
    sdf_files = [os.path.join(sdf_directory, file) for file in files if file.endswith(".sdf")
                 and file.startswith(f"{accession}")]

    if len(sdf_files) != 0:
        # Open the output file for writing
        with open(os.path.join(sdf_directory, f"{gene_name}_{accession}_ligands.sdf"), "w") as outfile:
            # Loop over the input files
            for i, filename in enumerate(sdf_files):
                # Open the input file for reading
                with open(filename, "r") as infile:
                    for line in infile:
                        # Write each line to the output file
                        outfile.write(line)
                if len(sdf_files) != i+1:
                    outfile.write("\n$$$$\n")
                else:
                    pass
                os.remove(filename)



