import os
import re
import logging
import time
import shutil  # To handle file operations
import pymolPy3  # Ensure this module is correctly installed and accessible

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to INFO or WARNING to reduce verbosity
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pymol_processing.log"),
        logging.StreamHandler()
    ]
)

# Step 1: Extract Unique PDB IDs and Chains from the DALI result file (limited to top 50)
def extract_unique_pdb_ids_and_chains(file_path, limit=50):
    """
    Parses the DALI result file to extract unique PDB IDs and their corresponding chains,
    limiting the number of PDBs processed to the top 50.
    
    Args:
        file_path (str): Path to the DALI result file.
        limit (int): The maximum number of PDB entries to process (default: 50).
    
    Returns:
        dict: A dictionary with PDB IDs as keys and chain identifiers as values.
    """
    pdb_chain_dict = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                # Adjust the regex based on the actual format of your DALI result file
                match = re.search(r'^(\d+):\s+(\w{4})-(\w)', line)
                if match:
                    pdb_id = match.group(2).lower()  # PDB IDs are typically lowercase
                    chain_id = match.group(3)
                    if pdb_id not in pdb_chain_dict:
                        pdb_chain_dict[pdb_id] = chain_id
                        if len(pdb_chain_dict) >= limit:  # Stop after collecting 'limit' entries
                            break
    except Exception as e:
        logging.error(f"Error reading or processing the DALI result file: {e}")
    return pdb_chain_dict

# Step 2: Initialize PyMOL
def initialize_pymol():
    """
    Initializes PyMOL without the GUI.
    
    Returns:
        pymolPy3.pymolPy3: An instance of the PyMOL interface.
    """
    try:
        pm = pymolPy3.pymolPy3(0)  # Initialize without GUI
        logging.info("PyMOL initialized successfully.")
        return pm
    except Exception as e:
        logging.error(f"Failed to initialize PyMOL: {e}")
        raise

# Step 3: Fetch, Process, and Save PDB Files Sequentially
def process_pdb_files(pm, pdb_chain_dict, output_directory):
    """
    Fetches PDB structures, extracts specified chains, saves them as separate PDB files,
    aligns them with a local PDB file, and saves PNG images of the alignment.
    
    Args:
        pm (pymolPy3.pymolPy3): The PyMOL interface instance.
        pdb_chain_dict (dict): Dictionary with PDB IDs and their corresponding chains.
        output_directory (str): Directory to save the processed PDB files.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        logging.debug(f"Created output directory: {output_directory}")
    
    for pdb_id, chain_id in pdb_chain_dict.items():
        try:
            logging.debug(f"Processing PDB ID: {pdb_id}, Chain: {chain_id}")
            
            # Fetch the PDB structure
            fetch_command = f"fetch {pdb_id}, async=0"  # async=0 to wait for completion
            pm(fetch_command)
            logging.info(f"Fetched PDB ID: {pdb_id}")
            
            # Introduce a short delay to ensure fetching is complete
            time.sleep(3)
            
            # Save the fetched CIF to root directory
            cif_output = f"{pdb_id}.cif"
            save_cif_command = f"save {cif_output}, {pdb_id}, format=cif"
            pm(save_cif_command)
            logging.info(f"Saved CIF for PDB ID: {pdb_id} to {cif_output}")
            
            # Introduce a short delay to ensure saving is complete
            time.sleep(5)
            
            # Remove all solvent molecules
            remove_solvent_command = f"remove (all and not polymer)"
            pm(remove_solvent_command)
            logging.debug("Removed solvent molecules")

            # Introduce a short delay to ensure solvent removal is complete
            time.sleep(3)

            # Remove all chains except the specified one
            remove_command = f"remove not chain {chain_id}"
            pm(remove_command)
            logging.debug(f"Removed all chains except Chain {chain_id} for PDB ID: {pdb_id}")
            
            # Introduce a short delay to ensure removal is complete
            time.sleep(3)
            
            # Define the output PDB filename
            output_pdb = f"{pdb_id}{chain_id}.pdb"
            output_path = os.path.join(output_directory, output_pdb)
            
            # Save the specified chain to the output directory
            save_pdb_command = f"save {output_path}, chain {chain_id}"
            pm(save_pdb_command)
            logging.info(f"Saved Chain {chain_id} of PDB ID {pdb_id} to {output_path}")
            
            # Introduce a short delay to ensure saving is complete
            time.sleep(3)
            
            # Load the local PDB file
            local_pdb_path = "/path/to/your/local_structure.pdb"
            load_local_pdb_command = f"load {local_pdb_path}, local_pdb"
            pm(load_local_pdb_command)
            logging.debug(f"Loaded local PDB file: {local_pdb_path} as 'local_pdb'")
            
            # Introduce a short delay to ensure loading is complete
            time.sleep(3)
            
            # Align the fetched chain with the local PDB
            align_command = f"align {pdb_id}, local_pdb"
            pm(align_command)
            logging.info(f"Aligned {pdb_id} with local_pdb")
            
            # Introduce a short delay to ensure alignment is complete
            time.sleep(3)
            
            # Zoom to the aligned structures
            zoom_command = f"zoom"
            pm(zoom_command)
            logging.debug("Zoomed to the aligned structures")

            # Introduce a short delay to ensure zoom is complete
            time.sleep(5)
            # Orient the view for better visualization
            orient_command = f"orient"
            pm(orient_command)
            logging.debug("Oriented the view")

            # Introduce a short delay to ensure orientation is complete
            time.sleep(2)

            # Color the aligned structures
            color_command = f"color cyan, {pdb_id}"
            pm(color_command)
            logging.debug(f"Colored {pdb_id} yellow")

            # Introduce a short delay to ensure coloring is complete
            time.sleep(1)

            color_command = f"color red, local_pdb"
            pm(color_command)
            logging.debug("Colored local_pdb green")

            # Introduce a short delay to ensure coloring is complete
            time.sleep(1)

            # Save a PNG image of the alignment
            png_filename = f"{pdb_id}_{chain_id}_alignment.png"
            png_command = f"png {png_filename}, dpi=300"
            pm(png_command)
            logging.info(f"Saved alignment image to {png_filename}")
            
            # Introduce a short delay to ensure PNG is saved
            time.sleep(2)
            
            # Clear all objects in PyMOL to prepare for the next iteration
            delete_all_command = f"delete all"
            pm(delete_all_command)
            logging.debug("Deleted all objects from PyMOL")
            
            # Introduce a short delay to ensure deletion is complete
            time.sleep(2)
        
        except Exception as e:
            logging.error(f"Error processing PDB ID {pdb_id}: {e}")
            # Continue processing other PDB IDs

# Step 4: Copy CIF Files to 'downloaded_pdbs' and Delete Originals
def copy_cif_files(destination_directory, pdb_ids):
    """
    Copies CIF files from the root directory to 'downloaded_pdbs' and deletes originals to save space.
    
    Args:
        destination_directory (str): Directory to copy CIF files to.
        pdb_ids (list): List of PDB IDs whose CIF files need to be copied.
    """
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
        logging.debug(f"Created directory: {destination_directory}")
    
    for pdb_id in pdb_ids:
        source_cif = f"{pdb_id}.cif"
        destination_cif = os.path.join(destination_directory, f"{pdb_id}.cif")
        
        if os.path.exists(source_cif):
            try:
                shutil.move(source_cif, destination_cif)
                logging.info(f"Moved {source_cif} to {destination_cif}")
            except Exception as e:
                logging.error(f"Error moving {source_cif} to {destination_cif}: {e}")
        else:
            logging.warning(f"CIF file for PDB ID {pdb_id} not found in root directory.")

# Step 5: Copy PNG Files to 'alignment_images' Directory
def copy_png_files(destination_directory):
    """
    Copies all PNG files from the root directory to the specified directory.
    
    Args:
        destination_directory (str): Directory to copy PNG files to.
    """
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
        logging.debug(f"Created directory: {destination_directory}")
    
    png_files = [f for f in os.listdir('.') if f.endswith('.png')]
    
    for png_file in png_files:
        source_png = png_file
        destination_png = os.path.join(destination_directory, png_file)
        try:
            shutil.move(source_png, destination_png)
            logging.info(f"Moved {source_png} to {destination_png}")
        except Exception as e:
            logging.error(f"Error moving {source_png} to {destination_png}: {e}")

# Step 6: Main Workflow
def main():
    dali_result_path = '8a1dA.txt'  # Path to your DALI result file (remember to change the file when using this script)
    output_directory = 'processed_pdbs_top50'  # Directory to save the processed PDB files
    downloaded_pdbs_directory = 'downloaded_pdbs_top50'  # Directory to save the downloaded CIF files
    alignment_images_directory = 'alignment_images_top50'  # Directory to save the alignment images
    
    # Step 1: Extract unique PDB IDs and chains (limit to 50)
    pdb_chain_dict = extract_unique_pdb_ids_and_chains(dali_result_path, limit=50)
    if not pdb_chain_dict:
        logging.warning("No PDB IDs and chains extracted. Exiting the script.")
        return
    logging.info(f"Unique PDB IDs extracted (limited to top 50): {list(pdb_chain_dict.keys())}")
    
    # Step 2: Initialize PyMOL
    pm = initialize_pymol()
    
    # Step 3: Fetch, Process, and Save PDB Files
    process_pdb_files(pm, pdb_chain_dict, output_directory)
    
    # Step 4: Copy CIF Files to 'downloaded_pdbs' and Delete Originals
    copy_cif_files(downloaded_pdbs_directory, list(pdb_chain_dict.keys()))
    
    # Step 5: Copy PNG Files to 'alignment_images' Directory
    copy_png_files(alignment_images_directory)
    
    # Finalize PyMOL
    try:
        pm('quit')  # Terminate PyMOL session
        logging.info("PyMOL session terminated successfully.")
    except Exception as e:
        logging.error(f"Error terminating PyMOL session: {e}")

if __name__ == '__main__':
    main()