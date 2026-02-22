"""
Common helper functions for file handling, visualization, etc.
"""
import io
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Optional

import pandas as pd
import streamlit as st


def inject_theme() -> None:
    """Inject custom CSS from .streamlit/styles.css."""
    css_path = Path(__file__).resolve().parent.parent / ".streamlit" / "styles.css"
    if css_path.exists():
        st.markdown(
            f'<style>{css_path.read_text()}</style>',
            unsafe_allow_html=True,
        )


def init_page() -> None:
    """Initialize page: theme, optional auth, sidebar logout."""
    inject_theme()
    from utils.auth import render_sidebar_auth, require_auth

    if not require_auth():
        st.stop()
    render_sidebar_auth()


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


def parse_batch_csv(path: str | Path) -> list[dict[str, Any]]:
    """
    Parse batch input CSV or Excel. Returns list of row dicts.
    """
    path = Path(path)
    if path.suffix == ".csv":
        df = pd.read_csv(path)
    elif path.suffix in (".xlsx", ".xls"):
        df = pd.read_excel(path)
    else:
        raise ValueError("Unsupported format. Use CSV or Excel.")
    return df.to_dict(orient="records")


def build_zip(entries: list[tuple[str, bytes | str]]) -> bytes:
    """Create a zip archive from (filename, content) pairs. Returns zip bytes."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, content in entries:
            if isinstance(content, str):
                content = content.encode("utf-8")
            zf.writestr(name, content)
    buffer.seek(0)
    return buffer.getvalue()


def save_session_file(data: bytes | str, name: str) -> Path:
    """Save data to a temp file for use by tools. Returns the path."""
    directory = Path(tempfile.gettempdir())
    path = directory / name
    if isinstance(data, str):
        data = data.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    return path
