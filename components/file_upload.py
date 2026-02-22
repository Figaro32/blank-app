"""
Enhanced drag-and-drop file upload component.
"""
from typing import Optional

import streamlit as st

# Common file types for bioinformatics tools
PDB_TYPES = ["pdb", "pdb1", "ent", "cif"]
FASTA_TYPES = ["fasta", "fa", "faa", "fna"]
SDF_TYPES = ["sdf", "mol", "mol2"]
BATCH_TYPES = ["csv", "xlsx", "xls"]
ALL_STRUCTURE = PDB_TYPES + SDF_TYPES + ["cif"]


def file_upload(
    key: str,
    label: str = "Upload a file",
    types: Optional[list[str]] = None,
    help_text: Optional[str] = None,
    accept_multiple: bool = False,
):
    """
    Enhanced file uploader with validation and clear messaging.

    Args:
        key: Unique key for the uploader
        label: Label shown above the uploader
        types: List of allowed extensions (e.g. ['pdb', 'cif'])
        help_text: Additional help text
        accept_multiple: Allow multiple file uploads (batch mode)

    Returns:
        UploadedFile or list of UploadedFile, or None if no file
    """
    type_str = ", ".join(types) if types else "any"
    default_help = f"Accepted formats: {type_str}. Drag and drop or click to browse."
    help_str = help_text or default_help

    uploaded = st.file_uploader(
        label=label,
        type=types,
        help=help_str,
        accept_multiple_files=accept_multiple,
        key=key,
    )

    if uploaded is None:
        return None

    if accept_multiple and len(uploaded) == 0:
        return None

    return uploaded


def batch_file_upload(
    key: str,
    label: str = "Upload batch file (CSV or Excel)",
    help_text: Optional[str] = None,
):
    """
    Upload CSV or Excel for batch processing.
    Returns the uploaded file or None.
    """
    return file_upload(
        key=key,
        label=label,
        types=BATCH_TYPES,
        help_text=help_text or "CSV or Excel with columns for sequences, IDs, or file references.",
        accept_multiple=False,
    )
