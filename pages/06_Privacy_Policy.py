import streamlit as st
import sys
import os

import Welcome

# Add the root directory to the path so we can import from the root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Welcome import is_authenticated

# Set page title
st.set_page_config(
    page_title="Privacy Policy - PDB Analysis Platform",
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
st.image("duodok.png", width=100)
st.title("🕵️ Privacy Policy")
if is_authenticated():
    # Get user information
    user_info = Welcome.get_user_info()

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
            Welcome.logout()
            st.rerun()
st.write("""
**Last Updated: January 1, 2025**

This Privacy Policy describes how the PDB Analysis Platform ("we," "our," or "us") collects, uses, and 
shares your personal information when you use our platform.

Please read this Privacy Policy carefully. By using the PDB Analysis Platform, you agree to the practices 
described in this policy.
""")

# Data collection section
st.header("Information Collected")


st.write("""
The information you directly provide to us is collected but not stored by our program, including:

- Email address (used for account identification and to send analysis results)
- Uploaded PDB files and analysis results

""")

st.subheader("How Your Information is Used")
st.write("""
Your collected information is used to:

- Provide, maintain, and improve our services
- Send you analysis results
- Respond to comments, questions, and requests
""")

# Data sharing section
st.header("How We Share Your Information")
st.write("""
Your personally identifiable information is not sold, traded, or otherwise transferred to outside parties.
""")

# Data security section
st.header("Data Security")
st.write("""
We are in the process of implementing appropriate technical and organizational measures to protect your personal information from unauthorized access, disclosure, alteration, and destruction. These measures include:

- Secure authentication through OAuth2
- Encryption of data in transit and at rest
- Regular security assessments and audits
- Rate limiting to prevent abuse
- Secure session management

However, no security system is impenetrable, and we cannot guarantee the absolute security of our systems. If you have any concerns about the security of your information, please contact us immediately.
""")

# Data retention section
st.header("Data Retention")
st.write("""
We retain your personal information for as long as necessary to fulfill the purposes outlined in this Privacy Policy, unless a longer retention period is required or permitted by law. 

For uploaded PDB files and analysis results:
- Files you upload for analysis are processed in memory and are not permanently stored unless you explicitly save your analysis.
- Saved analyses are retained for 90 days after your last interaction with them, after which they are automatically deleted.

For account information:
- Your account information is retained as long as you maintain an active account.
- If you request account deletion, we will delete your personal information within 30 days, except as required to comply with legal obligations.
""")

# Changes to policy section
st.header("Changes to This Privacy Policy")
st.write("""
We may update this Privacy Policy from time to time. If we make material changes, we will notify you by email or by posting a notice on our platform prior to the changes becoming effective. We encourage you to review this Privacy Policy periodically to stay informed about our information practices.
""")

# Contact information section
st.header("Contact Us")
st.write("""
If you have any questions, concerns, or requests regarding this Privacy Policy or our privacy practices, please contact us at:

**Email**: invisiblemr674@gmail.com
**Address**: Buffalo, New York, United States

If you have an unresolved privacy concern that we have not addressed satisfactorily, please contact your local data protection authority.
""")
# Consent acknowledgment
st.info("""
By using the PDB Analysis Platform, you acknowledge that you have read and understood this Privacy Policy.
""")
