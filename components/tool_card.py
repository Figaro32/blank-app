"""
Tool card component for home page - Tamarind-style grid.
"""
import streamlit as st
from typing import Optional


def tool_card(
    title: str,
    description: str,
    icon: str,
    page: str,
    category: Optional[str] = None,
) -> None:
    """
    Render a clickable card linking to a tool page.
    """
    with st.container():
        st.markdown(
            f"""
            <div class="tool-card" style="
                background: var(--background-color, white);
                border-radius: 12px;
                padding: 1.25rem 1.5rem;
                margin-bottom: 1rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                border: 1px solid #e2e8f0;
            ">
                <div class="tool-card-title">{icon} {title}</div>
                <div class="tool-card-desc">{description}</div>
                {f'<div class="tool-card-category">{category}</div>' if category else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link(page, label=f"Open {title}", icon="→", use_container_width=True)
