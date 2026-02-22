"""
3D structure viewer using stmol + py3Dmol.
"""
from pathlib import Path
from typing import Literal, Optional, Union

import py3Dmol
import streamlit as st
import stmol

Style = Literal["cartoon", "stick", "sphere", "surface"]


def structure_viewer(
    pdb_data: Union[str, bytes, Path],
    style: Style = "cartoon",
    width: int = 800,
    height: int = 500,
    spin: bool = False,
) -> None:
    """
    Display an interactive 3D molecular structure.

    Args:
        pdb_data: PDB content as string, bytes, or path to file
        style: Visualization style - cartoon (protein), stick, sphere, or surface
        width: Viewer width in pixels
        height: Viewer height in pixels
        spin: Whether to auto-rotate the structure
    """
    if isinstance(pdb_data, Path):
        pdb_str = pdb_data.read_text()
    elif isinstance(pdb_data, bytes):
        pdb_str = pdb_data.decode("utf-8", errors="replace")
    else:
        pdb_str = pdb_data

    view = py3Dmol.view(width=width, height=height)
    view.addModel(pdb_str, "pdb")
    view.setStyle({style: {}})
    view.zoomTo()
    if spin:
        view.spin(True)

    stmol.showmol(view, height=height, width=width)
