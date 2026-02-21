"""
Common helper functions for file handling, visualization, etc.
"""
import tempfile
from pathlib import Path
from typing import Optional

import streamlit as st


def save_uploaded_file(uploaded_file, directory: Optional[Path] = None) -> Path:
    """Save an uploaded Streamlit file to disk. Returns the path."""
    if directory is None:
        directory = Path(tempfile.gettempdir())
    path = directory / uploaded_file.name
    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return path


def st_file_uploader(
    key: str,
    types: Optional[list[str]] = None,
    help_text: str = "Upload a file",
) -> Optional[bytes]:
    """Upload a file and return its bytes, or None if no file."""
    uploaded = st.file_uploader(help_text, type=types or None, key=key)
    if uploaded is None:
        return None
    return uploaded.read()


def display_pdb(preview_lines: int = 50) -> None:
    """Display a PDB file preview in an expander."""
    uploaded = st.file_uploader("Upload PDB", type=["pdb", "pdb1", "ent"], key="pdb_preview")
    if uploaded:
        lines = uploaded.read().decode("utf-8", errors="replace").splitlines()
        with st.expander("PDB preview"):
            st.code("\n".join(lines[:preview_lines]), language="text")
