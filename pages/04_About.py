import streamlit as st
import sys
import os

import app

# Add the root directory to the path so we can import from the root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import is_authenticated

# Set page title
st.set_page_config(
    page_title="About - PDB Analysis Platform",
    page_icon="🧬",
    layout="wide"
)

def load_custom_css():
    with open(".streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Call the function at the beginning
load_custom_css()

# Check if user is authenticated
if not is_authenticated():
    st.warning("Please log in to access this page.")
    st.stop()

# Page content
st.title("About the Authors")
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
# Introduction section
st.write("""
Welcome to the team behind the PDB Analysis Platform. Our multidisciplinary team combines expertise 
in structural biology, bioinformatics, and software development to create tools that accelerate research 
and discovery in the field of protein structure analysis.
""")

# Team section
st.header("Our Team")

# Create columns for team members
col1, col2 = st.columns(2)

with col1:
    st.subheader("Dr. Jane Smith")
    st.write("**Lead Structural Biologist**")
    st.write("""
    Dr. Smith is a structural biologist with over 15 years of experience in protein crystallography 
    and NMR spectroscopy. She has published more than 50 peer-reviewed articles in leading journals 
    and has determined the structures of numerous proteins involved in human diseases.

    **Education:**
    - Ph.D. in Structural Biology, Stanford University
    - M.S. in Biochemistry, MIT
    - B.S. in Chemistry, University of California, Berkeley

    **Research Interests:**
    - Protein-ligand interactions
    - Structure-based drug design
    - Membrane protein structures
    """)

with col2:
    st.subheader("Dr. Michael Johnson")
    st.write("**Lead Bioinformatician**")
    st.write("""
    Dr. Johnson specializes in computational approaches to protein structure analysis and prediction. 
    His work on developing algorithms for protein structure comparison has been widely cited and 
    implemented in various bioinformatics tools.

    **Education:**
    - Ph.D. in Bioinformatics, University of Cambridge
    - M.S. in Computer Science, ETH Zurich
    - B.S. in Biophysics, Harvard University

    **Research Interests:**
    - Protein structure prediction
    - Machine learning applications in structural biology
    - Structural bioinformatics
    """)

# Create columns for more team members
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sarah Chen")
    st.write("**Software Developer**")
    st.write("""
    Sarah is a full-stack developer with expertise in scientific applications and data visualization. 
    She leads the technical implementation of the PDB Analysis Platform, ensuring a seamless user 
    experience and robust backend architecture.

    **Education:**
    - M.S. in Computer Science, Georgia Tech
    - B.S. in Software Engineering, University of Washington

    **Technical Skills:**
    - Python, JavaScript, React
    - Scientific computing and visualization
    - Cloud architecture and deployment
    """)

with col2:
    st.subheader("Dr. Robert Patel")
    st.write("**Protein Engineering Specialist**")
    st.write("""
    Dr. Patel brings expertise in protein engineering and directed evolution to the team. His insights 
    help shape the analysis tools to meet the needs of researchers working on protein design and optimization.

    **Education:**
    - Ph.D. in Biochemical Engineering, Caltech
    - B.S. in Bioengineering, UC San Diego

    **Research Interests:**
    - Computational protein design
    - Enzyme engineering
    - Protein stability and dynamics
    """)

# Project history
st.header("Project History")
st.write("""
The PDB Analysis Platform began as an internal tool at our research laboratory to streamline the 
analysis of protein structures. Recognizing its potential to benefit the wider scientific community, 
we developed it into a comprehensive web application with funding from the National Science Foundation.

The platform has evolved significantly since its inception in 2020:

- **2020**: Initial development of core analysis algorithms
- **2021**: Beta release with basic functionality for structure analysis
- **2022**: Added comparative analysis features and improved user interface
- **2023**: Launched enterprise version with enhanced security and collaborative features

Today, our platform is used by researchers at universities, pharmaceutical companies, and biotech 
startups worldwide.
""")

# Publications and Citations
st.header("Publications")
st.write("""
If you use the PDB Analysis Platform in your research, please cite our paper:

Smith, J., Johnson, M., Chen, S., & Patel, R. (2023). PDB Analysis Platform: An integrated tool for 
protein structure analysis and comparison. *Journal of Computational Biology*, 30(4), 342-356.

**Additional publications related to our platform:**

1. Johnson, M., & Smith, J. (2022). Comparative analysis of protein structures using graph-based algorithms. 
   *Bioinformatics*, 38(2), 123-135.

2. Patel, R., Chen, S., & Johnson, M. (2023). Predicting the impact of mutations on protein stability 
   using structural features. *Proteins: Structure, Function, and Bioinformatics*, 91(3), 201-215.

3. Chen, S., Smith, J., & Patel, R. (2022). Optimizing visualization of protein structural data for 
   web applications. *Journal of Cheminformatics*, 14, 42.
""")

# Get in touch
st.header("Get in Touch")
st.write("""
We value your feedback and are continuously working to improve the platform. If you have suggestions, 
questions, or would like to report issues, please use our Contact page.

For collaboration inquiries or research partnerships, you can reach us at research@pdbanalysis.example.com.
""")

# Future developments
st.header("Future Developments")
st.write("""
We're constantly working to enhance the PDB Analysis Platform. Upcoming features include:

- Integration with molecular dynamics simulation tools
- Enhanced machine learning capabilities for structure prediction
- API access for programmatic analysis
- Additional visualization options
- Batch processing for multiple structure analysis

Stay tuned for these exciting updates!
""")
