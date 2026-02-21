"""
Main entry point. Run with: streamlit run home.py
"""
import streamlit as st

st.set_page_config(page_title="Protein Design Suite", page_icon="🧬", layout="wide")

st.title("🧬 Protein Design Suite")
st.markdown("""
Welcome! Use the **sidebar** to navigate to each tool:

- **Home** – Overview of all tools
- **RFdiffusion3** – Structure generation
- **AlphaFold-like** – Structure prediction (coming soon)
- **ProteinMPNN** – Sequence design
- **Molecular Docking** – Docking workflows
- **ADMET Prediction** – Drug-likeness properties
""")
