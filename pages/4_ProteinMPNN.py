"""
ProteinMPNN - sequence design for fixed backbones.
"""
import streamlit as st

from components import file_upload, result_download, structure_viewer
from utils.helpers import init_page

st.set_page_config(page_title="ProteinMPNN", page_icon="🧪", layout="wide")
init_page()

st.title("🧪 ProteinMPNN")
st.markdown(
    "Design sequences for fixed backbone structures. Inverse folding. "
    "[Paper](https://www.science.org/doi/10.1126/science.add2187) | "
    "[Code](https://github.com/dauparas/ProteinMPNN)"
)
st.divider()

st.sidebar.subheader("Parameters")
num_seqs = st.sidebar.number_input("Number of sequences", value=8, min_value=1, max_value=64)
temperature = st.sidebar.slider("Sampling temperature", 0.01, 1.0, 0.1)

pdb_file = file_upload.file_upload(
    key="mpnn_pdb",
    label="Backbone PDB",
    types=["pdb", "pdb1", "ent", "cif"],
    help_text="Upload a protein structure. Designed sequences will fit this backbone.",
)

if pdb_file:
    pdb_bytes = pdb_file.read()
    with st.expander("Structure preview"):
        structure_viewer.structure_viewer(pdb_bytes, style="cartoon", width=700, height=400)

    if st.button("Run ProteinMPNN", type="primary", key="mpnn_run"):
        with st.status("Running ProteinMPNN...", expanded=True) as status:
            st.write("Loading model...")
            st.write("Designing sequences...")
            # Placeholder: no backend yet
            status.update(label="Backend not configured", state="complete")

        st.info(
            "ProteinMPNN backend not yet integrated. "
            "Configure the backend in `backends/proteinmpnn.py` to enable."
        )

        # Example output for UI demo
        with st.expander("Example output (placeholder)"):
            st.code(">design_1\nMKVLWAALLVTFLAGCQAKVEQAVETEPEPELRQQTEWQSG", language="text")
            result_download.download_button(
                data=">design_1\nMKVLWAALLVTFLAGCQAKVEQAVETEPEPELRQQTEWQSG\n",
                label="Download FASTA",
                filename="mpnn_designs.fasta",
                key="mpnn_dl",
            )
