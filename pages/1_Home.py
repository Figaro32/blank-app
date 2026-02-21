"""
Home page - welcome and overview of available tools.
"""
import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

st.title("🏠 Welcome")
st.markdown("""
### Overview of Tools

This app provides a suite of computational tools for protein design and analysis:

| Tool | Description |
|------|-------------|
| **RFdiffusion3** | Generate protein structures with diffusion models |
| **AlphaFold-like** | Structure prediction (coming soon) |
| **ProteinMPNN** | Sequence design for given backbones |
| **Molecular Docking** | Protein–ligand or protein–protein docking |
| **ADMET Prediction** | Physicochemical and drug-likeness properties |

Use the sidebar to navigate to each tool.
""")
