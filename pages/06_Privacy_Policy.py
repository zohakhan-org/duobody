import streamlit as st
import sys
import os

import app

# Add the root directory to the path so we can import from the root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import is_authenticated

# Set page title
st.set_page_config(
    page_title="Privacy Policy - PDB Analysis Platform",
    page_icon="🧬",
    layout="wide"
)

# Check if user is authenticated
if not is_authenticated():
    st.warning("Please log in to access this page.")
    st.stop()

# Page content
st.title("Privacy Policy")
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
**Last Updated: January 1, 2023**

This Privacy Policy describes how the PDB Analysis Platform ("we," "our," or "us") collects, uses, and 
shares your personal information when you use our platform.

Please read this Privacy Policy carefully. By using the PDB Analysis Platform, you agree to the practices 
described in this policy.
""")

# Data collection section
st.header("Information We Collect")

st.subheader("Information You Provide to Us")
st.write("""
We collect information you provide directly to us when you:

- Create an account
- Upload PDB files for analysis
- Submit contact form inquiries
- Participate in surveys or feedback requests
- Communicate with our support team

This information may include:

- **Account Information**: Your name, email address, and profile information from your Google account when you authenticate through Gmail
- **User Content**: PDB files and related data you upload for analysis
- **Communications**: Information you provide in your communications with us, including through the contact form
""")

st.subheader("Information We Collect Automatically")
st.write("""
When you use our platform, we automatically collect certain information, including:

- **Usage Information**: How you use our platform, including pages visited, features used, and actions taken
- **Device Information**: Information about your device, including IP address, browser type, and operating system
- **Log Data**: Server logs and error reports
""")

# Data use section
st.header("How We Use Your Information")
st.write("""
We use the information we collect to:

- **Provide and maintain our services**, including processing PDB files and delivering analysis results
- **Improve and develop our platform** by analyzing usage patterns and user feedback
- **Personalize your experience** by remembering your preferences and customizing content
- **Communicate with you** about updates, new features, and respond to your inquiries
- **Ensure security and prevent fraud** by monitoring for suspicious activity
- **Comply with legal obligations** as required by applicable laws and regulations
""")

# Data sharing section
st.header("How We Share Your Information")
st.write("""
We may share your information in the following circumstances:

- **With Service Providers**: We share information with third-party vendors who provide services on our behalf, such as hosting, analytics, and customer support. These providers are contractually obligated to use your information only for the purposes of providing services to us.
- **For Legal Reasons**: We may disclose information if we believe it is necessary to comply with applicable laws, regulations, legal processes, or governmental requests.
- **With Your Consent**: We may share information with third parties when you give us explicit consent to do so.
- **Business Transfers**: If we are involved in a merger, acquisition, or sale of assets, your information may be transferred as part of that transaction.

We do not sell your personal information to third parties.
""")

# Data security section
st.header("Data Security")
st.write("""
We implement appropriate technical and organizational measures to protect your personal information from unauthorized access, disclosure, alteration, and destruction. These measures include:

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

# User rights section
st.header("Your Rights and Choices")
st.write("""
Depending on your location, you may have certain rights regarding your personal information, including:

- **Access**: You can request a copy of the personal information we hold about you.
- **Correction**: You can request that we correct inaccurate or incomplete information.
- **Deletion**: You can request that we delete your personal information.
- **Restriction**: You can request that we restrict the processing of your personal information.
- **Data Portability**: You can request that we provide your personal information in a structured, commonly used, and machine-readable format.
- **Objection**: You can object to our processing of your personal information.

To exercise these rights, please contact us using the contact information provided below.
""")

# Children's privacy section
st.header("Children's Privacy")
st.write("""
The PDB Analysis Platform is not directed to individuals under the age of 16. We do not knowingly collect personal information from children under 16. If we become aware that we have collected personal information from a child under 16 without verification of parental consent, we will take steps to delete that information. If you believe we might have any information from or about a child under 16, please contact us.
""")

# International data transfers section
st.header("International Data Transfers")
st.write("""
Your information may be transferred to, stored, and processed in countries other than the country in which you reside. These countries may have data protection laws that are different from the laws of your country.

We take appropriate safeguards to require that your personal information will remain protected in accordance with this Privacy Policy when transferred internationally.
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

**Email**: privacy@pdbanalysis.example.com
**Address**: 123 Research Way, Science City, SC 12345, United States

If you have an unresolved privacy concern that we have not addressed satisfactorily, please contact your local data protection authority.
""")

# Consent acknowledgment
st.info("""
By using the PDB Analysis Platform, you acknowledge that you have read and understood this Privacy Policy.
""")
