#!/usr/bin/env python

import os
import time
from tkinter import filedialog
from Bio.PDB import *
from Bio.PDB.PDBParser import PDBParser
from tkinter import Tk
import pymol

root = Tk()
root.withdraw()


def extract_dbref_data(input_file):
    with open(input_file, 'r') as f:
        key_count = 1
        data_dict = {}
        for line in f:
            if line.startswith('DBREF'):
                chain = line[12:13].strip() or "NaN"
                try:
                    pdb_start = int(line[14:18].strip())
                except ValueError:
                    pdb_start = 0
                try:
                    pdb_end = int(line[20:24].strip())
                except ValueError:
                    pdb_end = 0
                try:
                    uniprot_start = int(line[56:60].strip())
                except ValueError:
                    uniprot_start = 0
                try:
                    uniprot_end = int(line[63:67].strip())
                except ValueError:
                    uniprot_end = 0
                db_accession = line[33:39].strip() or "NaN"
                db_id = line[42:53].strip() or "NaN"

                data_dict[key_count] = {"chain": chain, "pdb_start": pdb_start,
                                        "pdb_end": pdb_end, "db_accession": db_accession,
                                        "db_id": db_id, "uniprot_start": uniprot_start, "uniprot_end": uniprot_end}
                key_count += 1
    return data_dict


def extract_target_chains(pdb_files, target_id, output_dir):
    parser = PDBParser(QUIET=True)
    remove_dict = {}
    renumber_dict = {}
    for pdb_file in pdb_files:
        try:
            # Parse the PDB file
            structure = parser.get_structure("pdb", pdb_file)
            current_data = extract_dbref_data(pdb_file)

            target_chain = []
            for keys in current_data.keys():
                if current_data[keys]['db_id'].split('_')[0] == target_id:
                    target_chain.append(current_data[keys]['chain'])
            target_chain_ids = list(set(target_chain))
            print(f"{os.path.basename(pdb_file).replace('.pdb', '')}'s target chains : ", target_chain_ids)
            if len(target_chain_ids) == 0 :
                for chain in structure.get_chains():
                    # Get the ID of the chain and check if it should be saved
                    chain_id = chain.get_id()
                    output_file = os.path.join(output_dir,
                                               f"{os.path.basename(pdb_file).replace('.pdb', '')}_{chain_id}_not_matched.pdb")
                    print(f"{os.path.basename(output_file)} extraction completed")
                    # Save the separated chain to a PDB file
                    io = PDBIO()
                    io.set_structure(chain)
                    if not os.path.exists(os.path.dirname(output_file)):
                        os.makedirs(os.path.dirname(output_file))
                    io.save(output_file)

            else:
                for chain in structure.get_chains():
                    # Get the ID of the chain and check if it should be saved
                    chain_id = chain.get_id()
                    if chain_id in target_chain_ids:
                        output_file = os.path.join(output_dir,
                                                   f"{os.path.basename(pdb_file).replace('.pdb', '')}_{chain_id}.pdb")
                        print(f"{os.path.basename(output_file)} extraction completed")
                        # Save the separated chain to a PDB file
                        io = PDBIO()
                        io.set_structure(chain)
                        if not os.path.exists(os.path.dirname(output_file)):
                            os.makedirs(os.path.dirname(output_file))
                        io.save(output_file)

            for keys in current_data.keys():
                if current_data[keys]['chain'] in target_chain_ids and current_data[keys]['db_id'].split('_')[0] != target_id:
                    key = os.path.basename(pdb_file)
                    if key in remove_dict:
                        remove_dict[key].append({
                            "chain": current_data[keys]['chain'],
                            "db_id": current_data[keys]['db_id'],
                            "pdb_start": current_data[keys]['pdb_start'],
                            "pdb_end": current_data[keys]['pdb_end']
                        })
                    else:
                        remove_dict[key] = [{
                            "chain": current_data[keys]['chain'],
                            "db_id": current_data[keys]['db_id'],
                            "pdb_start": current_data[keys]['pdb_start'],
                            "pdb_end": current_data[keys]['pdb_end']
                        }]
                else:
                    key = os.path.basename(pdb_file)
                    if key in renumber_dict:
                        renumber_dict[key].append({
                            "chain": current_data[keys]['chain'],
                            "db_id": current_data[keys]['db_id'],
                            "pdb_start": current_data[keys]['pdb_start'],
                            "pdb_end": current_data[keys]['pdb_end'],
                            "uniprot_start": current_data[keys]['uniprot_start'],
                            "uniprot_end": current_data[keys]['uniprot_end']
                        })
                    else:
                        renumber_dict[key] = [{
                            "chain": current_data[keys]['chain'],
                            "db_id": current_data[keys]['db_id'],
                            "pdb_start": current_data[keys]['pdb_start'],
                            "pdb_end": current_data[keys]['pdb_end'],
                            "uniprot_start": current_data[keys]['uniprot_start'],
                            "uniprot_end": current_data[keys]['uniprot_end']
                        }]
        except Exception as e:
            print(f"Failed to extract chains from {pdb_file}: {e}")

    return remove_dict, renumber_dict


# 'ER0', #Tetramethyloctadecanoate
# 'OLA', #Oleic acid
# 'OLB', #(2S)-2,3-dihydroxypropyl (9Z)-octadec-9-enoate
# 'OLC', #1-Oleoyl-R-glycerol
# 'PEG', #2-(2-hydroxyethyloxy)ethanol
# '1PE', #PEG400
# 'HEX', #Hexane
# 'SO4', #Sulfate
# 'OCT', #Octane
# 'MYS', #Pentadecane
# 'D12', #Dodecane
# 'TRD', #Tridecane
# 'EDT', #EDTA
# 'D10', #Decane
# 'GOL', #Glycerol
# 'PGE', #Triethylene Glycol
# '8K6', #Octadecane
# 'PE4', #Polyethylene Glycol PEG4000
# 'STE', #Stearic acid
# 'UND', #Undecane
# 'EDO', #1,2-Ethanediol
# 'DMS', #Dimethyl sulfoxide
# 'ACN', #Acetone
# 'IPA', #Isopropanol
# 'MOH', #Methanol
# 'EOH', #Ethanol
# 'POL', #Propanol
# 'SBT', #Butanol
# '1BO', #Butanol
# 'PGO', #1,2-Propanediol
# 'BU1', #1,4-Butanediol
# 'CCN', #Acetonitrile
# 'DMF', #Dimethylformamide
# 'PLM', #Palmitic acid
# 'J40',

remove_list = ['ER0', 'OLA', 'OLB', 'OLC', 'PEG', '1PE', 'HEX', 'SO4', 'OCT', 'MYS', 'D12', 'TRD', 'EDT', 'D10', 'GOL',
               'PGE', '8K6', 'PE4', 'STE', 'UND', 'EDO', 'DMS', 'ACN', 'IPA', 'MOH', 'EOH', 'POL', 'SBT', '1BO', 'PGO',
               'BU1', 'DMF', 'PLM', 'J40']


def align_and_save_all_pdb_files(directory, ref_pdb_file, ligand_name, ligand_range, remove_dict, renumber_dict):
    # Create a new directory for aligned pdb files
    parent_dir = os.path.dirname(directory)
    new_dir_name = os.path.join(parent_dir, f"{os.path.basename(directory)}_aligned")
    os.makedirs(new_dir_name, exist_ok=True)

    # Start PyMOL and load the reference pdb file
    pymol.finish_launching()
    time.sleep(1)  # wait for PyMOL to fully load
    pymol.cmd.load(ref_pdb_file, 'ref')
    distance_cutoff = 3.0
    save = 1

    # Loop through all pdb files in the directory
    for pdb_file in os.listdir(directory):
        if pdb_file.endswith(".pdb"):

            # Load the pdb file
            pymol.cmd.load(os.path.join(directory, pdb_file), pdb_file[:-4])
            name_for_dict = '_'.join(pdb_file.split('_')[:2]) + '.pdb'

            try:
                for data in remove_dict[name_for_dict]:
                    rm_chain = data['chain']
                    rm_start = data['pdb_start']
                    rm_end = data['pdb_end']
                    if (rm_start - rm_end) > 0:
                        print(f'Wrong DBREF data: {pdb_file} , Check resi {rm_start}-{rm_end}')
                        save = 0
                    pymol.cmd.remove(f"(chain {rm_chain} and resi {rm_start}-{rm_end})")
                    print(f"{pdb_file}, resi{rm_start}-{rm_end} has been removed")

            except: pass

            try:
                for data in renumber_dict[name_for_dict]:
                    rn_chain = data['chain']
                    rn_start = data['pdb_start']
                    rn_end = data['pdb_end']
                    un_start = data['uniprot_start']
                    un_end = data['uniprot_end']
                    minus = rn_start - un_start
                    plus = rn_start - un_start

                    if rn_start != un_start or rn_end != un_end:
                        pymol.cmd.select('selection', f'chain {rn_chain} and resi {rn_start}-{rn_end}')
                        pymol.cmd.alter('selection', f'resi=str(int(resi)-{minus})')
                        pymol.cmd.select('selection2',
                                         f'resi {un_start}-{un_end} and chain "" and polymer.protein and resn ""')
                        pymol.cmd.alter('selection2', f'resi=str(int(resi)+{plus})')

                        print(f"{pdb_file}, resi{rn_start}-{rn_end} has been renumbered")

            except:
                print(pdb_file, 'renumber error')
                pass

            # Align the pdb file to the reference pdb file
            pymol.cmd.align(pdb_file[:-4], 'ref')

            pymol.cmd.origin('ref')
            pymol.cmd.zoom("all", 0.8)
            #
            # Remove the organic and solvent
            pymol.cmd.select("main_ligand", f"resn {ligand_name}")
            pymol.cmd.select("main_organic", f"bymolecule(main_ligand expand {ligand_range})")
            pymol.cmd.remove('organic and not main_organic')
            #
            pymol.cmd.select("nearby_solvent", f"solvent within {distance_cutoff} of main_organic")
            pymol.cmd.remove('solvent and not nearby_solvent')
            #
            # Remove the inorganic
            pymol.cmd.select("target", "polymer.protein")
            pymol.cmd.select("main_inorganic", f"inorganic within {distance_cutoff} of target")
            pymol.cmd.select("not_nearby_inorganic", f"inorganic and not main_inorganic")
            pymol.cmd.remove("not_nearby_inorganic")
            # #
            # #
            for mol in remove_list:
                pymol.cmd.remove(f"resn {mol}")

            # Save the aligned pdb file with a new name
            new_file_name = f"{pdb_file[:-4]}_aligned.pdb"
            if save != 0:
                pymol.cmd.save(os.path.join(new_dir_name, new_file_name), pdb_file[:-4])
            else: save = 1
            pymol.cmd.sync()  # wait for the save command to complete

            # Delete the loaded pdb file to free up memory
            pymol.cmd.delete(pdb_file[:-4])

    # Delete the reference pdb file to free up memory
    pymol.cmd.delete('ref')

    # Quit PyMOL
    pymol.cmd.quit()


if __name__ == "__main__":
    print('Step 1: Extract target chains'+'\n' * 6)
    # Select a directory using a file dialog
    dir_path = filedialog.askdirectory(title='Select a directory to work with')
    ref_pdb_file = filedialog.askopenfilename(title='Select the file you want to use as the reference',initialdir=dir_path)

    # Parse the reference PDB file
    ref_data_dict = extract_dbref_data(ref_pdb_file)
    print('\n' * 3)
    for i in ref_data_dict.keys():
        print(f'Key {i}: Chain: {ref_data_dict[i]["chain"]} DB_ID: {ref_data_dict[i]["db_id"]}'
              f'   ({ref_data_dict[i]["pdb_start"]}-{ref_data_dict[i]["pdb_end"]})')
    print('\n' * 3)
    input_key = int(input('input key number: ', ))
    target_id = ref_data_dict[input_key]['db_id'].split('_')[0]

    # Create a list of paths to PDB files in the directory
    pdb_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(".pdb")]

    # Create a directory to store the output files containing the separated chains
    output_dir = os.path.join(dir_path, f"{target_id}_target_chains")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extract the chains from the input PDB files that match the molecules in the reference PDB file
    remove_dict, renumber_dict = extract_target_chains(pdb_files, target_id, output_dir)
    print('remove_dict: ',remove_dict)
    print('\n' * 7)
    print('###########  Target chains extraction Complete  ###########'+'\n' * 2)
    print('Step 2: Start preprocessing with pymol'+'\n' * 8)
    align_ref = filedialog.askopenfilename(title='Select the file you want to use as the align criteria',initialdir=output_dir)

    with open(os.path.join(align_ref), 'r') as f:
        ligand_menu = []
        for line in f:
            if line.startswith('HETNAM'):
                print(line)
            if line.startswith('HETATM'):
                ligand_menu.append(line[17:20].replace(' ', ''))
        print(list(set(ligand_menu)))

    ligand_name = input("Enter ligand name: ")
    print('\n' * 1)
    ligand_range = input("Range around the ligand you do not want to delete(Å): ")
    print('\n' * 7)
    align_and_save_all_pdb_files(output_dir, align_ref, ligand_name, ligand_range, remove_dict, renumber_dict)
    print('\n' * 7)
    print('########### PDB Preprocessing Complete  ###########' + '\n' * 2)