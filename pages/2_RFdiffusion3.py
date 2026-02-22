"""
RFdiffusion3 - all-atom protein design (flagship tool).
"""
import streamlit as st

from backends.rdf3 import RDF3Config, RDF3Result, run
from components import file_upload, result_download, structure_viewer
from components.batch_panel import parse_batch_file
from utils.helpers import init_page

st.set_page_config(page_title="RFdiffusion3", page_icon="🧬", layout="wide")
init_page()

st.title("🧬 RFdiffusion3")
st.markdown(
    "All-atom protein design with diffusion models. Design proteins, enzymes, "
    "and protein–ligand complexes. [Paper](https://www.biorxiv.org/) | "
    "[Code](https://github.com/RosettaCommons/foundry)"
)
st.divider()

tab1, tab2 = st.tabs(["Single Design", "Batch Design"])

with tab1:
    st.subheader("Single design")
    col_upload, col_params = st.columns([1, 1])

    with col_upload:
        scaffold_file = file_upload.file_upload(
            key="rdf3_scaffold",
            label="Scaffold PDB (optional)",
            types=["pdb", "pdb1", "ent", "cif"],
            help_text="Upload a scaffold structure. Leave empty for de novo design.",
        )
        ligand_file = file_upload.file_upload(
            key="rdf3_ligand",
            label="Ligand SDF (optional)",
            types=["sdf", "mol", "mol2"],
            help_text="Upload ligand for protein–ligand design.",
        )

    with col_params:
        num_designs = st.number_input("Number of designs", min_value=1, max_value=20, value=1)
        output_prefix = st.text_input("Output prefix", value="design")

    constraints_json = st.text_area(
        "Constraints JSON (optional)",
        value="{}",
        height=100,
        help="JSON with conditioning (motifs, symmetry, etc.). Leave {} for default.",
    )

    if st.button("Run design", type="primary", key="rdf3_run_single"):
        config = RDF3Config(
            scaffold_pdb=scaffold_file.read() if scaffold_file else None,
            ligand_sdf=ligand_file.read() if ligand_file else None,
            constraints_json=constraints_json or "{}",
            num_designs=num_designs,
            output_prefix=output_prefix,
        )
        with st.status("Running RFdiffusion3...", expanded=True) as status:
            try:
                results = run(config, backend="stub")
                status.update(label="Done!", state="complete")
            except Exception as e:
                st.error(str(e))
                results = []

        if results:
            st.subheader("Results")
            for i, res in enumerate(results):
                if res.status == "done" and res.pdb_content:
                    with st.expander(f"Design {i + 1}"):
                        structure_viewer.structure_viewer(
                            res.pdb_content,
                            style="cartoon",
                            width=700,
                            height=400,
                        )
                        result_download.download_button(
                            data=res.pdb_content,
                            label="Download PDB",
                            filename=f"{output_prefix}_{i}.pdb",
                            key=f"rdf3_dl_{i}",
                        )

with tab2:
    st.subheader("Batch design")
    batch_file = file_upload.batch_file_upload(
        key="rdf3_batch",
        label="Upload CSV or Excel",
        help_text="Columns: scaffold_pdb (path or inline), output_prefix, num_designs. Or use a template.",
    )

    if batch_file:
        df, err = parse_batch_file(batch_file)
        if err:
            st.error(err)
        elif df is not None:
            st.dataframe(df.head(10), use_container_width=True, hide_index=True)
            st.caption(f"Total rows: {len(df)}")

            if st.button("Run batch", type="primary", key="rdf3_run_batch"):
                # Use stub for each row; in real impl, call run() per row
                entries = []
                progress = st.progress(0.0)
                for i, row in df.iterrows():
                    prefix = str(row.get("output_prefix", row.get("id", f"design_{i}")))
                    config = RDF3Config(output_prefix=prefix, num_designs=1)
                    res_list = run(config, backend="stub")
                    if res_list and res_list[0].pdb_content:
                        entries.append((f"{prefix}.pdb", res_list[0].pdb_content))
                    progress.progress((i + 1) / len(df), text=f"Processed {i + 1} / {len(df)}")
                progress.empty()

                if entries:
                    st.success(f"Generated {len(entries)} designs.")
                    result_download.download_zip(
                        entries,
                        zip_filename="rdf3_batch_results.zip",
                        label="Download all (ZIP)",
                        key="rdf3_batch_zip",
                    )
