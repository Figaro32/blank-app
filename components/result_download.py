"""
Download helpers for single files and zip archives.
"""
from typing import Optional

import streamlit as st

from utils.helpers import build_zip


def download_button(
    data: bytes | str,
    label: str = "Download",
    filename: str = "result",
    mime: Optional[str] = None,
    key: Optional[str] = None,
) -> None:
    """
    Render a download button for a single file.

    Args:
        data: File content as bytes or string
        label: Button label
        filename: Suggested filename for download
        mime: MIME type (e.g. 'chemical/x-pdb', 'text/csv', 'image/png')
        key: Unique Streamlit key
    """
    if isinstance(data, str):
        data = data.encode("utf-8")

    if mime is None:
        if filename.endswith(".pdb"):
            mime = "chemical/x-pdb"
        elif filename.endswith(".csv"):
            mime = "text/csv"
        elif filename.endswith(".png") or filename.endswith(".jpg"):
            mime = f"image/{filename.split('.')[-1]}"
        else:
            mime = "application/octet-stream"

    st.download_button(
        label=label,
        data=data,
        file_name=filename,
        mime=mime,
        key=key,
    )


def download_zip(
    entries: list[tuple[str, bytes | str]],
    zip_filename: str = "results.zip",
    label: str = "Download all (ZIP)",
    key: Optional[str] = None,
) -> None:
    """
    Create a zip archive and offer it for download.

    Args:
        entries: List of (filename, content) tuples
        zip_filename: Name of the zip file
        label: Button label
        key: Unique Streamlit key
    """
    zip_bytes = build_zip(entries)
    st.download_button(
        label=label,
        data=zip_bytes,
        file_name=zip_filename,
        mime="application/zip",
        key=key,
    )
