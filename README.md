# D2P2F : DALI to PyMol to FoldManson script

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [In-Progress Features](#in-progress-features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setting Up the Anaconda Environment](#setting-up-the-anaconda-environment)
- [Usage](#usage)
  - [Configuring the Script](#configuring-the-script)
  - [Running it](#running-it)
- [Contact](#contact)

## Introduction

D2P2F is an semi-automated script designed to streamline the processing of DALI result files to PDBs that could be uploaded to FoldManson to create structual phylogeny trees. It extracts unique Protein Data Bank (PDB) IDs and their corresponding chains, fetches the associated structures using PyMOL, and organizes the data into one folder. Users can then upload the PDBs to FoldManson to build the strutual phylogeny tree.

To use DALI: http://ekhidna2.biocenter.helsinki.fi/dali/
To use FoldManson: https://search.foldseek.com/foldmason

## Features

- **Automated Extraction**: Parses DALI result files to identify unique PDB ID hits and their corresponding chains (selects one if multiple chain in PDB is hit).
- **PyMOL Integration**: Utilizes PyMOL to fetch PDB structures directly from the Protein Data Bank.
- **Chain Extraction**: Removes all chains except chain extracted from the first ste[].
- **File Management**: Saves extracted chains as separate PDB files and manages CIF files by copying them to a dedicated directory and deleting originals to save space.
- **Comprehensive Logging**: Maintains detailed logs of all operations for easy monitoring and troubleshooting.

## In-Progress Features

- **Automated DALI Result File Cleaning**: Currently, the DALI result text file requires manual modification where the first three lines and lines after "structural equivalence" are deleted by hand. This feature is slated for automation in future updates.

    > **Note**: Manual modification of the DALI result file is necessary for the automator to function correctly. This step involves deleting the first three lines and any lines following the "structural equivalence" section.

## Installation

### Prerequisites

- **Anaconda**: Ensure that Anaconda is installed on your system. If not, download and install it from [here](https://www.anaconda.com/products/individual).
- **Git**: To clone the repository. Install Git from [here](https://git-scm.com/downloads) if it's not already installed.

### Setting Up the Anaconda Environment

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

## Usage

### Configuring the Script

Before running the automator, you need to configure the script to point to your DALI result text file.

1. **Locate the Script**

    Copy the `download.py` script to a directory containing the DALI results text file

2. **Modify the DALI Result File Path**

    Locate the following line in the `main()` function:

    ```python
    dali_result_path = '8a1dA.txt'  # Path to your DALI result file
    ```

    Replace `'8a1dA.txt'` with the path to your own DALI results text file.

    Example:

    ```python
    dali_result_path = 'MY_DALI_RESULTS.txt'  # DALI result file in that folder
    ```

### Running the Processor

1. **Ensure Proper Environment Activation**

    Make sure the Anaconda environment is activated.

    ```bash
    conda activate P2D2F
    ```

2. **Execute the Script**

    Run the `download.py` script (in the directory where your processed DALI results txt is located!).

    ```bash
    python download.py
    ```

3. **Monitor the Process**

    The script will perform the following actions sequentially:
    - Extract unique PDB IDs and chains from the specified DALI result file.
    - Initialize PyMOL without the GUI.
    - Fetch each PDB structure using PyMOL.
    - Save the fetched CIF files to the root directory.
    - Extract and save the specified chains as separate PDB files in the `processed_pdbs` directory.
    - Move CIF files to the `downloaded_pdbs` directory and delete the originals to conserve space.
    - Terminate the PyMOL session.

4. **Check Output Directories**
    - **processed_pdbs**: Contains the extracted chain PDB files.
    - **downloaded_pdbs**: Contains the copied CIF files from the root directory.

5. **Upload to FoldManson**
    - **Upload**: Upload the pdbs in "processed_pdbs" directory to FoldManson
    - **Happy tree building!**
  
## Contact

For any questions, suggestions, or feedback, please open an issue on the GitHub repository or contact XXX@connect.hku.hk Thank you very much!
