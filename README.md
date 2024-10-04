# DALI-PyMOL Processor

![DALI-PyMOL Processor Logo](logo.png) <!-- Replace with your logo if available -->

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [In-Progress Features](#in-progress-features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setting Up the Anaconda Environment](#setting-up-the-anaconda-environment)
- [Usage](#usage)
  - [Configuring the Script](#configuring-the-script)
  - [Running the Processor](#running-the-processor)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

**DALI-PyMOL Processor** is an automated tool designed to streamline the processing of DALI (Distance-matrix ALIgnment) result files. It extracts unique Protein Data Bank (PDB) IDs and their corresponding chains, fetches the associated structures using PyMOL, and organizes the data efficiently by saving specific chains and managing CIF files to conserve disk space. This processor is ideal for researchers and bioinformaticians looking to handle structural equivalence data with ease.

## Features

- **Automated Extraction**: Parses DALI result files to identify unique PDB IDs and their corresponding chains.
- **PyMOL Integration**: Utilizes PyMOL to fetch PDB structures directly from the Protein Data Bank.
- **Chain Extraction**: Removes all chains except the specified one, allowing focused analysis on regions of interest.
- **File Management**: Saves extracted chains as separate PDB files and manages CIF files by copying them to a dedicated directory and deleting originals to save space.
- **Comprehensive Logging**: Maintains detailed logs of all operations for easy monitoring and troubleshooting.

## In-Progress Features

- **Automated DALI Result File Cleaning**: Currently, the DALI result text file requires manual modification where the first three lines and lines after "structural equivalence" are deleted by hand. This feature is slated for automation in future updates.

  *Note: Manual modification of the DALI result file is necessary for the processor to function correctly. This step involves deleting the first three lines and any lines following the "structural equivalence" section.*

## Installation

### Prerequisites

- **Anaconda**: Ensure that Anaconda is installed on your system. If not, download and install it from [here](https://www.anaconda.com/products/distribution).
- **Git**: To clone the repository. Install Git from [here](https://git-scm.com/downloads) if it's not already installed.

### Setting Up the Anaconda Environment

An `environment.yml` file is provided to set up the required dependencies easily.

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/DALI-PyMOL-Processor.git
   cd DALI-PyMOL-Processor
