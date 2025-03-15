import glob
import streamlit as st
import sys
import os
import itertools
import subprocess
import shutil
import pandas as pd
import app
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Add the root directory to the path so we can import from the root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import is_authenticated

# Set page title
st.set_page_config(
    page_title="Tutorial - PDB Analysis Platform",
    page_icon="🧬",
    layout="wide"
)

# Ensure user is authenticated before proceeding
if not is_authenticated():
    st.warning("Please log in to access this page.")
    st.stop()

# Page content
st.title("DuoDok Analysis")
st.write("Note: You must install the files from Github to run it.")

# Fetch user info
user_info = app.get_user_info()

# Sidebar: User Info & Logout
with st.sidebar:
    if user_info:
        st.write(f"Welcome, {user_info.get('name', 'User')}!")
        st.write(f"Email: {user_info.get('email', 'N/A')}")
        st.write("© 2025 DuoDok")
    else:
        st.write("Welcome, User! © 2025 DuoDok")

    # Logout button
    if st.button("Logout"):
        app.logout()
        st.rerun()

# Folder setup
UPLOAD_FOLDER = 'uploads'
RECEPTOR_FOLDER = 'receptors'
ANTIBODY_FOLDER = 'antibodies'
RESULTS_FOLDER = 'results'
DEFAULT_RECEPTOR_FOLDER = 'receptors/default'
DEFAULT_ANTIBODY_FOLDER = 'antibodies/default'

# Ensure all directories exist
for directory in [UPLOAD_FOLDER, RECEPTOR_FOLDER, ANTIBODY_FOLDER, RESULTS_FOLDER, DEFAULT_RECEPTOR_FOLDER, DEFAULT_ANTIBODY_FOLDER]:
    os.makedirs(directory, exist_ok=True)

def get_files_from_directory(directory):
    logger.debug(f"Getting files from directory: {directory}")
    files = [os.path.basename(f) for f in glob.glob(f"{directory}/*.pdb")]
    logger.debug(f"Found {len(files)} files: {files}")
    return files

def send_results_email(user_email, results_folder):
    logger.debug(f"Sending results email to {user_email}, results folder: {results_folder}")
    # Placeholder function for email sending (assumed you have one in your app)
    pass

def check_hdock_installed():
    """Check if HDOCK is installed and available in system path."""
    if shutil.which("./hdock") is None:
        st.error("HDOCK is not installed or not found in the system path. Please install HDOCK.")
        return False
    return True

def run_analysis(selected_receptors, selected_antibodies, user_email):
    if not selected_receptors or not selected_antibodies:
        st.error('Please select at least one receptor and one antibody.')
        return

    # Check if HDOCK is installed
    if not check_hdock_installed():
        return

    # Create a unique results folder for this run
    user_results_folder = os.path.join(RESULTS_FOLDER, user_email.replace('@', '_').replace('.', '_'))
    os.makedirs(user_results_folder, exist_ok=True)
    logger.debug(f"Results will be saved in: {user_results_folder}")

    # Set up progress tracking
    total_combinations = len(selected_receptors) * len(selected_antibodies)
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Process all combinations
    results_data = []

    for i, (receptor_name, antibody_name) in enumerate(itertools.product(selected_receptors, selected_antibodies)):
        progress = int((i / total_combinations) * 100)
        progress_bar.progress(progress)
        status_text.text(f"Processing {receptor_name} with {antibody_name}... ({i + 1}/{total_combinations})")

        receptor_path = os.path.join(DEFAULT_RECEPTOR_FOLDER if receptor_name.startswith('default_') else RECEPTOR_FOLDER, receptor_name[8:] if receptor_name.startswith('default_') else receptor_name)
        antibody_path = os.path.join(DEFAULT_ANTIBODY_FOLDER if antibody_name.startswith('default_') else ANTIBODY_FOLDER, antibody_name[8:] if antibody_name.startswith('default_') else antibody_name)

        pair_name = f"{os.path.splitext(receptor_name)[0]}_{os.path.splitext(antibody_name)[0]}"
        pair_dir = os.path.join(user_results_folder, pair_name)
        os.makedirs(pair_dir, exist_ok=True)

        # Debugging: Log receptor and antibody paths
        logger.debug(f"Receptor path: {receptor_path}, Antibody path: {antibody_path}")

        # Run HDOCK
        hdock_out = os.path.join(pair_dir, "hdock.out")
        try:
            logger.debug(f"Running HDOCK with {receptor_path} and {antibody_path}")
            subprocess.run(["./hdock", receptor_path, antibody_path, "-out", hdock_out], check=True, capture_output=True)

            # Run createpl
            complex_pdb = os.path.join(pair_dir, "Protein_Peptide.pdb")
            logger.debug(f"Running createpl with output: {hdock_out}, complex: {complex_pdb}")
            subprocess.run(["./createpl", hdock_out, complex_pdb, "-nmax", "1", "-complex", "-models"], check=True, capture_output=True)

            # Run PRODIGY
            prodigy_output = os.path.join(pair_dir, "prodigy_results.txt")
            logger.debug(f"Running PRODIGY with complex: {complex_pdb}")
            subprocess.run(["prodigy", complex_pdb], check=True, capture_output=True, text=True, stdout=open(prodigy_output, 'w'))

            # Run PLIP
            plip_command = f"python ~/plip/plip/plipcmd.py -i {complex_pdb} -yv"
            logger.debug(f"Running PLIP with command: {plip_command}")
            subprocess.run(plip_command, shell=True, check=True, capture_output=True)

            # Try to run PyMOL
            pymol_command = f"pymol {os.path.splitext(complex_pdb)[0]}_NFT_A_283.pse"
            try:
                logger.debug(f"Running PyMOL with command: {pymol_command}")
                subprocess.run(pymol_command, shell=True, check=True, capture_output=True)
            except Exception as e:
                logger.error(f"Error running PyMOL: {e}")
                pass

            # Parse PRODIGY results
            binding_energy = "N/A"
            with open(prodigy_output, 'r') as f:
                for line in f:
                    if "Predicted binding affinity" in line:
                        binding_energy = line.split(':')[1].strip()

            results_data.append({
                'Receptor': receptor_name,
                'Antibody': antibody_name,
                'Binding Energy': binding_energy,
                'Result Folder': pair_dir
            })

        except subprocess.CalledProcessError as e:
            logger.error(f"Error processing {receptor_name} with {antibody_name}: {str(e)}")
            st.error(f"Error processing {receptor_name} with {antibody_name}: {str(e)}")
            continue

    # Complete progress
    progress_bar.progress(100)
    status_text.text("Analysis complete!")

    # Create a summary table
    if results_data:
        results_df = pd.DataFrame(results_data)
        results_csv = os.path.join(user_results_folder, "results_summary.csv")
        results_df.to_csv(results_csv, index=False)

        # Send results email
        send_results_email(user_email, user_results_folder)

        st.success('Analysis complete! Results have been emailed to you.')

        # Display results summary
        st.subheader("Results Summary")
        st.dataframe(results_df)

        # Create download link for results
        shutil.make_archive(user_results_folder, 'zip', user_results_folder)
        with open(f"{user_results_folder}.zip", "rb") as file:
            btn = st.download_button(
                label="Download Results (ZIP)",
                data=file,
                file_name=f"{os.path.basename(user_results_folder)}_results.zip",
                mime="application/zip"
            )
    else:
        st.error('No results were generated. Please check the logs for errors.')

# Upload and Selection UI for Receptors and Antibodies
col1, col2 = st.columns(2)

with col1:
    st.header("Receptor Files")
    uploaded_receptor = st.file_uploader("Upload Receptor File (.pdb)", type=["pdb"], key="receptor_uploader")
    if uploaded_receptor is not None:
        file_path = os.path.join(RECEPTOR_FOLDER, uploaded_receptor.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_receptor.getbuffer())
        st.success(f"Receptor file {uploaded_receptor.name} uploaded successfully!")

    default_receptors = get_files_from_directory(DEFAULT_RECEPTOR_FOLDER)
    user_receptors = get_files_from_directory(RECEPTOR_FOLDER)
    user_receptors = [f for f in user_receptors if f not in default_receptors]

    st.subheader("Default Receptors")
    default_receptor_selections = [st.checkbox(receptor, key=f"def_rec_{receptor}") for receptor in default_receptors]
    selected_default_receptors = [f"default_{receptor}" for receptor, selected in zip(default_receptors, default_receptor_selections) if selected]

    st.subheader("Your Uploaded Receptors")
    if user_receptors:
        user_receptor_selections = [st.checkbox(receptor, key=f"user_rec_{receptor}") for receptor in user_receptors]
        selected_user_receptors = [receptor for receptor, selected in zip(user_receptors, user_receptor_selections) if selected]
    else:
        st.write("No uploaded receptors")
        selected_user_receptors = []

with col2:
    st.header("Antibody Files")
    uploaded_antibody = st.file_uploader("Upload Antibody File (.pdb)", type=["pdb"], key="antibody_uploader")
    if uploaded_antibody is not None:
        file_path = os.path.join(ANTIBODY_FOLDER, uploaded_antibody.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_antibody.getbuffer())
        st.success(f"Antibody file {uploaded_antibody.name} uploaded successfully!")

    default_antibodies = get_files_from_directory(DEFAULT_ANTIBODY_FOLDER)
    user_antibodies = get_files_from_directory(ANTIBODY_FOLDER)
    user_antibodies = [f for f in user_antibodies if f not in default_antibodies]

    st.subheader("Default Antibodies")
    default_antibody_selections = [st.checkbox(antibody, key=f"def_ab_{antibody}") for antibody in default_antibodies]
    selected_default_antibodies = [f"default_{antibody}" for antibody, selected in zip(default_antibodies, default_antibody_selections) if selected]

    st.subheader("Your Uploaded Antibodies")
    if user_antibodies:
        user_antibody_selections = [st.checkbox(antibody, key=f"user_ab_{antibody}") for antibody in user_antibodies]
        selected_user_antibodies = [antibody for antibody, selected in zip(user_antibodies, user_antibody_selections) if selected]
    else:
        st.write("No uploaded antibodies")
        selected_user_antibodies = []

# Combine selections
selected_receptors = selected_default_receptors + selected_user_receptors
selected_antibodies = selected_default_antibodies + selected_user_antibodies

# Run analysis button
if st.button("Run Analysis", type="primary"):
    if not selected_receptors:
        st.error("Please select at least one receptor")
    elif not selected_antibodies:
        st.error("Please select at least one antibody")
    else:
        run_analysis(selected_receptors, selected_antibodies, st.session_state.auth['user_email'])

# Information section
st.header("About DuoDok Analysis")
st.write("""
DuoDok performs comprehensive analysis of receptor-antibody interactions using multiple computational tools:
""")
st.markdown("""
- **HDOCK** - A protein-protein docking algorithm
- **PRODIGY** - A binding affinity prediction tool
- **PLIP** - A tool for protein-ligand interaction analysis
""")
st.write("This platform facilitates an efficient workflow for antibody research and development.")
