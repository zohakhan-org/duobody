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
st.title("About the Author")
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
st.header("Me, Myself and I")

# Create columns for team members
col1, col2 = st.columns([1, 3])
with col1:
    st.image("aarish.jpg", caption="")
    pass
with col2:
    st.subheader("Mohmmad Aarish Khan")
    st.caption("Highschooler passionate about the world of Computational Biology")
    st.write("""
    Mohammad Aarish Khan, a 16 year old highschool, has found his passional in helping others through his knowledge in the fields of technology and biology. 
    His research for the Terra Science Fair 2026, focuses on developing an automated way for predicting and analyzing molecular interactions between protein receptors and ligands, in a attempt to make the promise of bi-specific antibodies accessible to all.
    """)

st.divider()


# Publications and Citations
st.header("Publications")
st.write("""
my publications
""")

# Get in touch
st.header("Get in Touch")
st.write("""
We value your feedback and are continuously working to improve the platform. If you have suggestions, 
questions, or would like to report issues, please use our Contact page.

For collaboration inquiries or research partnerships, you can reach us at invisiblemr674@gmail.com.
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
