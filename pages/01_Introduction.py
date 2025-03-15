import streamlit as st
import sys
import os

import app

# Add the root directory to the path so we can import from the root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import is_authenticated

# Set page title
st.set_page_config(
    page_title="Introduction - PDB Analysis Platform",
    page_icon="🧬",
    layout="wide"
)

# Check if user is authenticated
if not is_authenticated():
    st.warning("Please log in to access this page.")
    st.stop()

# Page content
st.title("Introduction to PDB Analysis Platform")

if is_authenticated():
    # Get user information
    user_info = app.get_user_info()

    # Display user information and logout button in the sidebar
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

st.write("""
## What is the PDB Analysis Platform?

The PDB Analysis Platform is a comprehensive tool designed for researchers, scientists, and students 
working with protein structures. Our platform provides an intuitive interface to analyze and compare 
Protein Data Bank (PDB) files, helping you gain insights into protein structures and their properties.

## Key Features

### 1. PDB File Validation
Upload your PDB files and verify their integrity with our validation system. We check for standard 
format compliance and common structural issues.

### 2. Structural Analysis
Analyze key properties of protein structures:
- Residue and atom counts
- Chain identification
- Secondary structure elements
- Bond lengths and angles
- Structural motifs

### 3. Comparative Analysis
Compare two PDB files to identify:
- Structural differences
- Conformational changes
- Ligand binding effects
- Mutation impacts

### 4. Visualization
While we don't provide direct 3D visualization, our analysis results are designed to complement 
popular visualization tools like PyMOL, Chimera, and VMD.

## Getting Started

To begin using the platform:

1. Navigate to the **Tutorial** section to learn how to use the platform effectively
2. Go to the **Analysis** page to upload and analyze your PDB files
3. Use the **Contact** form if you need assistance or have suggestions

## Who Should Use This Platform?

- **Structural Biologists**: Analyze protein structures and compare different models
- **Computational Chemists**: Evaluate structural changes in proteins
- **Students**: Learn about protein structure and bioinformatics
- **Researchers**: Generate insights for publications and research projects
""")

# Display example use cases
with st.expander("Example Use Cases"):
    st.write("""
    ### Use Case 1: Analyzing Protein Mutations
    Compare wild-type and mutant protein structures to understand how mutations affect protein folding and function.

    ### Use Case 2: Drug Discovery
    Analyze protein-ligand interactions by comparing bound and unbound protein structures to identify key binding sites.

    ### Use Case 3: Protein Engineering
    Evaluate structural changes in engineered proteins to optimize stability, activity, or specificity.

    ### Use Case 4: Education
    Use the platform as a teaching tool to help students understand protein structure principles and analysis techniques.
    """)

# Add a note about data privacy
st.info("""
**Note on Data Privacy:** The PDB files you upload are processed on our secure servers and are not stored 
permanently unless you explicitly choose to save your analysis. For more information, please refer to our 
Privacy Policy page.
""")
