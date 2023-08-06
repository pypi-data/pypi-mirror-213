#!/usr/bin/env python

import os
import requests
import time
import matplotlib.pyplot as plt
from tqdm import tqdm


def download_fasta(search_term, dir_name):

    search_term=search_term.replace(' ', '%20')
    # Set the URL and parameters for the API request
    url = f'https://rest.uniprot.org/uniprotkb/stream?compressed=false&format=fasta&query=(protein_name:{search_term}%20AND%20(fragment:false))'

    # Create a timestamp string
    time_string = time.strftime("%Y%m%d", time.localtime())

    # Create a directory if it does not already exist
    directory_name = f"{dir_name}_{time_string}"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    # Check if the FASTA file already exists
    fasta_file_path = os.path.join(directory_name, f"{dir_name}.fasta")
    if os.path.isfile(fasta_file_path):
        print(f"Using existing FASTA file at {fasta_file_path}")
        return fasta_file_path

    # Send the API request
    response = requests.get(url, stream=True)
    print('Waiting for response...')

    # If the request is successful, save the file
    if response.ok:
        print('Response.OK')
        print('Saving FASTA file...')
        with open(fasta_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=2 ** 20):
                f.write(chunk)
        print(f"FASTA file saved to {fasta_file_path}")
        return fasta_file_path
    else:
        print(f"Failed to retrieve FASTA file for {search_term}")
        print('Server response code: ', response.status_code)
        if response.status_code == 429:
            print("Too many requests. Waiting for the server's response...")
            if 'Retry-After' in response.headers:
                retry_after = int(response.headers['Retry-After'])
                print(f'Please retry after {retry_after}seconds')
        return None

def remove_outlier(search_key,gene_name,fasta_file_path):
    cleaned_file_path = fasta_file_path + '_cleaned.fasta'

    # Check if cleaned file already exists
    if os.path.exists(cleaned_file_path):
        print(f"{cleaned_file_path} already exists. Skipping outlier removal and plot creation.")
        return cleaned_file_path

    # Open the file
    with open(fasta_file_path, 'r') as f:
        lines = f.readlines()
    # Extract sequences and their headers
    seqs = []
    headers = []
    seq_profile = []
    for line in lines:
        if line.startswith('>'):
            headers.append(line.strip())
            seq_profile.append('')
            seqs.append('')
        else:
            seqs[-1] += line.strip()

    # Extract lengths
    lengths = [len(seq) for seq in seqs]

    if len(seqs) == 0 :
        print('**** Empty FASTA file ****: Please check the search keywords you entered.')
        exit()
    else: pass

    # Create a boxplot of the lengths before removing outliers
    fig1, ax1 = plt.subplots()
    ax1.boxplot(lengths, vert=False)
    ax1.set_xlabel('Sequence Length')
    ax1.set_title('Boxplot of Sequence Lengths (Before Removing Outliers)')
    plt.savefig(os.path.splitext(fasta_file_path)[0] + '_boxplot_before.png')
    plt.close()

    # Calculate median and IQR
    median = sorted(lengths)[len(lengths) // 2]
    q1 = sorted(lengths)[len(lengths) // 4]
    q3 = sorted(lengths)[len(lengths) // 4 * 3]
    iqr = q3 - q1

    # Remove sequences that are more than 1.5IQR away from the median length
    cleaned_seqs = []
    cleaned_headers = []
    for seq, header, length in tqdm(zip(seqs, headers, lengths), total=len(seqs), desc='Filtering sequences'):
        if length >= q1 - 1.5 * iqr and length <= q3 + 1.5 * iqr:
            if search_key.lower() in header.lower() or gene_name.upper() in header.upper():
                if 'like' not in header:
                    cleaned_seqs.append(seq)
                    cleaned_headers.append(header)

    # Write the file again with headers
    with open(cleaned_file_path, 'w') as f:
        for i, (header, seq) in tqdm(enumerate(zip(cleaned_headers, cleaned_seqs)), total=len(cleaned_seqs),
                                     desc='Writing cleaned_seqs to file'):
            f.write(f'{header}\n{seq}\n')

    # Extract lengths of cleaned sequences
    cleaned_lengths = [len(seq) for seq in cleaned_seqs]

    # Create a boxplot of the lengths after removing outliers
    fig2, ax2 = plt.subplots()
    ax2.boxplot(cleaned_lengths, vert=False)
    ax2.set_xlabel('Sequence Length')
    ax2.set_title('Boxplot of Sequence Lengths (After Removing Outliers)')
    plt.savefig(os.path.splitext(fasta_file_path)[0] + '_boxplot_after.png')
    plt.close()

    print(f"Outliers removed from {fasta_file_path}")
    return cleaned_file_path
