"""
Shared home page content - hero and tool grid.
"""
import streamlit as st

from components import tool_card

TOOLS = [
    {
        "title": "RFdiffusion3",
        "description": "Generate protein structures with all-atom diffusion models. Design proteins, enzymes, and protein–ligand complexes.",
        "icon": "🧬",
        "page": "pages/2_RFdiffusion3.py",
        "category": "Protein Design",
    },
    {
        "title": "AlphaFold-like",
        "description": "Predict protein structures from sequences. Multimer and monomer support.",
        "icon": "📐",
        "page": "pages/3_AlphaFold-like.py",
        "category": "Structure Prediction",
    },
    {
        "title": "ProteinMPNN",
        "description": "Design sequences for fixed backbone structures. Inverse folding.",
        "icon": "🧪",
        "page": "pages/4_ProteinMPNN.py",
        "category": "Sequence Design",
    },
    {
        "title": "Molecular Docking",
        "description": "Protein–ligand or protein–protein docking. AF2BIND-style binding prediction.",
        "icon": "⚗️",
        "page": "pages/5_Molecular_Docking.py",
        "category": "Docking",
    },
    {
        "title": "ADMET Prediction",
        "description": "Physicochemical and drug-likeness properties. Absorption, distribution, metabolism, excretion, toxicity.",
        "icon": "💊",
        "page": "pages/6_ADMET_Prediction.py",
        "category": "Property Prediction",
    },
]


def render_home_content() -> None:
    """Render the home page hero and tool grid."""
    st.markdown("# Bioinformatics Portal")
    st.markdown(
        "A unified suite of computational biology tools. No coding required — drag, drop, and run."
    )
    st.divider()

    cols = st.columns(2)
    for i, tool in enumerate(TOOLS):
        with cols[i % 2]:
            tool_card.tool_card(
                title=tool["title"],
                description=tool["description"],
                icon=tool["icon"],
                page=tool["page"],
                category=tool.get("category"),
            )
