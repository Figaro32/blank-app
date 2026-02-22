"""
ADMET Prediction - physicochemical and drug-likeness properties.
"""
import streamlit as st

from components import file_upload, result_download
from utils.helpers import init_page

st.set_page_config(page_title="ADMET Prediction", page_icon="💊", layout="wide")
init_page()

st.title("💊 ADMET Prediction")
st.markdown(
    "Predict absorption, distribution, metabolism, excretion, and toxicity. "
    "Drug-likeness and physicochemical properties."
)
st.divider()

st.sidebar.subheader("Parameters")
properties = st.sidebar.multiselect(
    "Properties to predict",
    ["Lipinski Rule of 5", "Solubility", "Permeability", "Toxicity", "Drug-likeness"],
    default=["Lipinski Rule of 5", "Drug-likeness"],
)

input_mode = st.radio("Input mode", ["SMILES", "File upload"], horizontal=True, key="admet_mode")

if input_mode == "SMILES":
    smiles = st.text_input("SMILES string", placeholder="CC(=O)OC1=CC=CC=C1C(=O)O")
    mol_input = smiles
else:
    mol_file = file_upload.file_upload(
        key="admet_file",
        label="Molecules (SDF, CSV with SMILES column)",
        types=["sdf", "mol", "csv"],
        help_text="Upload a file with molecular structures.",
    )
    mol_input = mol_file

if st.button("Run ADMET prediction", type="primary", key="admet_run"):
    if not mol_input or (input_mode == "SMILES" and not mol_input.strip()):
        st.warning("Please provide a SMILES string or upload a file.")
    else:
        with st.status("Running ADMET prediction...", expanded=True) as status:
            st.write("Parsing input...")
            st.write("Computing descriptors...")
            status.update(label="Backend not configured", state="complete")

        st.info(
            "ADMET backend not yet integrated. "
            "Configure in `backends/admet.py` to enable."
        )

        # Placeholder table for UI demo
        with st.expander("Example output (placeholder)"):
            import pandas as pd

            df = pd.DataFrame(
                {
                    "Property": ["MW", "LogP", "HBD", "HBA", "Lipinski pass"],
                    "Value": [180.2, 1.4, 0, 4, "Yes"],
                }
            )
            st.dataframe(df, use_container_width=True, hide_index=True)
            csv = df.to_csv(index=False)
            result_download.download_button(
                data=csv,
                label="Download CSV",
                filename="admet_results.csv",
                key="admet_dl",
            )
