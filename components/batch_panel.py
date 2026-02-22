"""
Batch workflow panel with progress and per-row status.
"""
from typing import Callable, Optional

import pandas as pd
import streamlit as st


def parse_batch_file(uploaded_file) -> tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Parse uploaded CSV or Excel file.
    Returns (DataFrame, error_message). error_message is None on success.
    """
    if uploaded_file is None:
        return None, None

    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            return None, "Unsupported format. Use CSV or Excel."
    except Exception as e:
        return None, str(e)

    if df.empty:
        return None, "File is empty."

    return df, None


def batch_panel(
    df: pd.DataFrame,
    column_mapping: dict[str, str],
    process_row: Callable[[dict], dict],
    key_prefix: str = "batch",
) -> list[dict]:
    """
    Run batch processing with progress bar and per-row status.

    Args:
        df: DataFrame from batch file
        column_mapping: Map batch columns to expected keys, e.g. {'sequence': 'seq', 'id': 'name'}
        process_row: Function that takes a row dict, returns {'status': 'done'|'failed', 'output': ...}
        key_prefix: Unique prefix for session state keys

    Returns:
        List of result dicts, one per row
    """
    results = []
    total = len(df)
    progress_bar = st.progress(0.0, text="Processing...")
    status_container = st.container()

    for i, row in df.iterrows():
        row_dict = {}
        for batch_col, expected_key in column_mapping.items():
            if batch_col in df.columns:
                row_dict[expected_key] = row[batch_col]
            else:
                row_dict[expected_key] = None

        try:
            result = process_row(row_dict)
            results.append(result)
        except Exception as e:
            results.append({"status": "failed", "error": str(e), "row": i})

        progress_bar.progress((i + 1) / total, text=f"Processed {i + 1} / {total}")

    progress_bar.empty()

    # Summary table
    with status_container:
        st.subheader("Batch results")
        summary_data = []
        for i, r in enumerate(results):
            status = r.get("status", "unknown")
            summary_data.append({"Row": i + 1, "Status": status})

        st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

    return results
