"""
AlphaFold-like - structure prediction (coming soon).
"""
import streamlit as st

from components import file_upload
from utils.helpers import init_page

st.set_page_config(page_title="AlphaFold-like", page_icon="📐", layout="wide")
init_page()

st.title("📐 AlphaFold-like Structure Prediction")
st.markdown(
    "Predict protein structures from sequences. Multimer and monomer support. "
    "[Paper](https://www.nature.com/articles/s41586-021-03819-2) | "
    "[Code](https://github.com/deepmind/alphafold)"
)
st.divider()

st.warning("🚧 Coming soon — Structure prediction will be available in a future release.")

with st.expander("Preview: Upload and parameters"):
    seq_file = file_upload.file_upload(
        key="af_seq",
        label="Sequence (FASTA)",
        types=["fasta", "fa", "faa", "fna", "txt"],
        help_text="Upload FASTA or paste sequence.",
    )
    st.sidebar.subheader("Parameters")
    st.sidebar.selectbox("Model", ["monomer", "multimer"], key="af_model")
    st.sidebar.number_input("Number of recycles", value=3, min_value=1, max_value=20)
    st.sidebar.button("Run prediction", disabled=True, help="Coming soon")
