"""
Molecular Docking - protein–ligand or AF2BIND-style docking.
"""
import streamlit as st

from components import file_upload, result_download, structure_viewer
from utils.helpers import init_page

st.set_page_config(page_title="Molecular Docking", page_icon="⚗️", layout="wide")
init_page()

st.title("⚗️ Molecular Docking")
st.markdown(
    "Protein–ligand docking or AF2BIND-style binding prediction. "
    "[DiffDock](https://github.com/gcorso/DiffDock) | "
    "[Autodock Vina](https://vina.scripps.edu/)"
)
st.divider()

st.sidebar.subheader("Parameters")
docking_mode = st.sidebar.selectbox(
    "Mode",
    ["Protein–ligand", "Protein–protein (AF2BIND)"],
    key="dock_mode",
)
exhaustiveness = st.sidebar.number_input("Search exhaustiveness", value=8, min_value=1, max_value=64)

protein_file = file_upload.file_upload(
    key="dock_protein",
    label="Protein structure (PDB)",
    types=["pdb", "pdb1", "ent", "cif"],
    help_text="Target protein structure.",
)
ligand_file = file_upload.file_upload(
    key="dock_ligand",
    label="Ligand (SDF/MOL)",
    types=["sdf", "mol", "mol2", "pdb"],
    help_text="Small molecule to dock.",
)

if protein_file:
    with st.expander("Protein structure preview"):
        structure_viewer.structure_viewer(protein_file.read(), style="cartoon", width=700, height=400)
    protein_file.seek(0)

if st.button("Run docking", type="primary", key="dock_run"):
    if not protein_file or not ligand_file:
        st.warning("Please upload both protein and ligand files.")
    else:
        with st.status("Running docking...", expanded=True) as status:
            st.write("Preparing structures...")
            st.write("Searching binding poses...")
            status.update(label="Backend not configured", state="complete")

        st.info(
            "Docking backend not yet integrated. "
            "Configure in `backends/docking.py` to enable."
        )
