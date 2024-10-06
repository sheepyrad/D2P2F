# D2P2F : DALI to PyMOL to FoldManson Script

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [In-Progress Features](#in-progress-features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setting Up the Environment](#setting-up-the-environment)
- [Usage](#usage)
  - [Preparing Your DALI Result File](#preparing-your-dali-result-file)
  - [Configuring the Script](#configuring-the-script)
  - [Running the Script](#running-the-script)
  - [Creating Your Structural Phylogenetic Tree](#creating-your-structural-phylogenetic-tree)
- [Contact](#contact)

## Introduction

D2P2F is a semi-automated script designed to streamline the processing of DALI result files into PDBs that can be uploaded to FoldManson to create structural phylogenetic trees. It extracts unique Protein Data Bank (PDB) IDs and their corresponding chains, fetches the associated structures using PyMOL, aligns them with a local PDB file, and organizes the data into dedicated folders. Users can then upload the processed PDB files to FoldManson or other tools to build structural phylogenetic trees.

- DALI: [http://ekhidna2.biocenter.helsinki.fi/dali/](http://ekhidna2.biocenter.helsinki.fi/dali/)
- FoldManson: [https://search.foldseek.com/foldmansion](https://search.foldseek.com/foldmansion)

## Features

- **Automated Extraction**: Parses DALI result files to identify unique PDB IDs and their corresponding chains, limited to the top 50 entries (modifiable).
- **PyMOL Integration**: Utilizes PyMOL to fetch PDB structures directly from the Protein Data Bank.
- **Chain Extraction and Processing**: Removes all chains except the specified one, saves extracted chains as separate PDB files, and aligns them with a local PDB file.
- **Alignment Images**: Generates and saves PNG images of the aligned structures for visualization.
- **File Management**: Organizes processed PDB files, CIF files, and alignment images into dedicated directories.
- **Comprehensive Logging**: Maintains detailed logs of all operations for easy monitoring and troubleshooting.

## In-Progress Features

- **Automated DALI Result File Cleaning**: Currently, the DALI result text file requires manual modification where the first three lines and lines after "structural equivalence" are deleted by hand. This feature is slated for automation in future updates.

    > **Note**: Manual modification of the DALI result file is necessary for the automator to function correctly. This step involves deleting the first three lines and any lines following the "structural equivalence" section.

## Installation

### Prerequisites

- **Anaconda**: Ensure that Anaconda is installed on your system. If not, download and install it from [here](https://www.anaconda.com/).
- **Git**: To clone the repository. Install Git from [here](https://git-scm.com/) if it's not already installed.

### Setting Up the Environment

An `environment.yml` file is provided to set up the required dependencies easily.

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/D2P2F.git
    cd D2P2F
    ```

2. **Create the Conda Environment**

    ```bash
    conda env create -f environment.yml
    ```

3. **Activate the Environment**

    ```bash
    conda activate D2P2F
    ```

4. **Install PyMOL (only if the anaconda fails to install it)**

    If PyMOL is not correctly installed, you can install it within the conda environment:

    ```bash
    conda install -c schrodinger pymol
    ```

    Note: The `pymolPy3` module is required by the script. If it's not installed by default, you can install it via pip:

    ```bash
    pip install pymolPy3
    ```

## Usage

### Preparing Your DALI Result File

Before running the script, you need to prepare your DALI result file.

1. **Obtain DALI Results**
   - Submit your protein structure to the DALI server.
   - Download the result file (usually a text file).

2. **Ensure Correct Format**

    The script expects the DALI result file to be in a specific format to extract the PDB IDs and chain identifiers. You may need to manually edit your DALI result file to ensure it matches this format.

    **Format Requirements**:
    - Each relevant line should start with a rank number followed by a colon.
    - After the colon, there should be whitespace, followed by a 4-letter PDB ID, a hyphen, and a single-letter chain identifier.

    **Example line**:

    ```makefile
    1:    1abc-A
    2:    2def-B
    ```

    **Regular Expression Used**:

    ```python
    match = re.search(r'^(\d+):\s+(\w{4})-(\w)', line)
    ```

    **Steps to Prepare the File**:
    - Remove Unnecessary Lines: Delete any header or footer lines that do not contain the PDB entries.
    - Format Entries: Ensure that each line containing a PDB entry matches the required format.

    **Note**: If your DALI result file does not match this format, the script will not be able to extract the PDB IDs and chain identifiers correctly.

### Configuring the Script

Before running the script, you need to configure several variables in the script to match your environment and data.

1. **Set the Path to Your DALI Result File**

    In the `main()` function in the download.py (or download_top50.py), locate the following line:

    ```python
    dali_result_path = '6sb3A.txt'  # Path to your DALI result file
    ```

    Replace `'6sb3A.txt'` with the path to your own DALI result file.

    **Example**:

    ```python
    dali_result_path = 'my_dali_results.txt'  # Path to your DALI result file
    ```

2. **Set the Output Directories**

    The script saves processed files to specific directories. You can customize these directories in the `main()` function:

    ```python
    output_directory = 'processed_pdbs_top50'  # Directory to save the processed PDB files
    downloaded_pdbs_directory = 'downloaded_pdbs_top50'  # Directory to save the downloaded CIF files
    alignment_images_directory = 'alignment_images_top50'  # Directory to save the alignment images
    ```

    You can change the directory names as needed.

3. **Specify the Local PDB File for Alignment**

    The script aligns the fetched PDB structures with a local PDB file. In the `process_pdb_files` function, locate the following line:

    ```python
    local_pdb_path = "/path/to/your/local_structure.pdb"
    ```

    Replace the path with the path to your own local PDB file that you wish to use for alignment.

    **Example**:

    ```python
    local_pdb_path = "/home/XXX/XXX/local_structure.pdb"
    ```

    **Note**: Ensure that the local PDB file exists at the specified location.

4. **Adjust the Limit of PDB Entries (Optional)**

    By using the download_top50.py, the script processes the top 50 entries from the DALI result file. You can adjust this limit by changing the `limit` parameter in the `extract_unique_pdb_ids_and_chains` function call in the `main()` function:

    ```python
    pdb_chain_dict = extract_unique_pdb_ids_and_chains(dali_result_path, limit=50)
    ```

    Change `50` to your desired number of entries.

    For downloading all the entries, you can use the download.py.

### Running the Script

1. **Ensure Proper Environment Activation**

    Make sure the Anaconda environment is activated.

    ```bash
    conda activate D2P2F
    ```

2. **Execute the Script**

    Run the script:

    ```bash
    python download.py
    ```

    Replace `download.py` with the name of your script file (download_top50.py) if different.

3. **Monitor the Process**

    The script will perform the following actions sequentially:

    - Step 1: Extract unique PDB IDs and chains from the specified DALI result file.
    - Step 2: Initialize PyMOL without the GUI.
    - Step 3: For each PDB ID:
        - Fetch the PDB structure using PyMOL.
        - Save the fetched CIF file to the root directory.
        - Remove solvent molecules.
        - Remove all chains except the specified chain.
        - Save the specified chain as a separate PDB file in the output directory.
        - Load the local PDB file.
        - Align the fetched chain with the local PDB.
        - Generate and save a PNG image of the alignment.
        - Clear all objects in PyMOL to prepare for the next iteration.
    - Step 4: Move CIF files to the downloaded_pdbs directory.
    - Step 5: Move PNG images to the alignment_images directory.
    - Finalize: Terminate the PyMOL session.

    **Note**: The script includes delays (`time.sleep()`) to ensure that each PyMOL command completes before the next command is issued. These delays may make the script run longer but help avoid errors due to command overlap, if your computer is really slow, you may need to adjust the number to avoid errors.

4. **Check Output Directories**

    After the script completes, you can find the processed files in the specified directories:

    - **Processed PDB Files**: Located in the `processed_pdbs_top50` directory (or your specified output directory). These are the extracted chains ready for further analysis or uploading to FoldMansion.
    - **Downloaded CIF Files**: Located in the `downloaded_pdbs_top50` directory.
    - **Alignment Images**: Located in the `alignment_images_top50` directory. These are PNG images of the aligned structures.

5. **Review the Log File**

    The script generates a log file named `pymol_processing.log` that contains detailed information about the processing steps. Review this file for any errors or warnings that may have occurred during execution.

### Creating Your Structural Phylogenetic Tree

1. **Upload PDB Files to FoldManson**
    - Navigate to FoldMansion.
    - Upload the PDB files from the `processed_pdbs_top50` directory.
    - Follow the FoldManson instructions to build your structural phylogenetic tree.

2. **Use Alignment Images**
    - The alignment images in the `alignment_images_top50` directory can be used to visualize the structural alignments.
    - These images can enhance your understanding of the structural similarities and differences among the proteins.

3. **Happy Tree Building!**
    - Explore the relationships revealed by your structural phylogenetic tree.
    - Incorporate your findings into your research or presentations.

## Contact

For any questions, suggestions, or feedback, please open an issue on the GitHub repository, contact XXX@connect.hku.hk. Thank you very much!
