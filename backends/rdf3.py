"""
RFdiffusion3 backend interface and implementations.

Supports:
- CLI: subprocess calling rfd3 design (foundry)
- API: HTTP POST to custom or Tamarind API
- Stub: mock results for development
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

# Stub PDB for demo (minimal valid PDB)
STUB_PDB = """ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00  0.00           N
ATOM      2  CA  ALA A   1       1.458   0.000   0.000  1.00  0.00           C
ATOM      3  C   ALA A   1       2.009   1.420   0.000  1.00  0.00           C
ATOM      4  O   ALA A   1       1.247   2.394   0.000  1.00  0.00           O
ATOM      5  CB  ALA A   1       1.991  -0.774  -1.229  1.00  0.00           C
END
"""


@dataclass
class RDF3Config:
    """Configuration for a single RDF3 design run."""

    scaffold_pdb: Optional[bytes] = None
    scaffold_path: Optional[Path] = None
    ligand_sdf: Optional[bytes] = None
    ligand_path: Optional[Path] = None
    constraints_json: Optional[str] = None
    num_designs: int = 1
    output_prefix: str = "design"


@dataclass
class RDF3Result:
    """Result from a single RDF3 design run."""

    status: str  # "done" | "failed"
    pdb_content: Optional[str] = None
    error: Optional[str] = None
    output_path: Optional[Path] = None


def run_stub(config: RDF3Config) -> list[RDF3Result]:
    """
    Stub runner that returns mock PDB output.
    Use for UI development when CLI/API are not available.
    """
    results = []
    for i in range(config.num_designs):
        results.append(
            RDF3Result(
                status="done",
                pdb_content=STUB_PDB,
                output_path=Path(f"{config.output_prefix}_{i}.pdb"),
            )
        )
    return results


def run_cli(config: RDF3Config, out_dir: Path) -> list[RDF3Result]:
    """
    Run RDF3 via foundry CLI: rfd3 design ...
    Requires rc-foundry and rfd3 to be installed.
    """
    import subprocess

    # TODO: Implement subprocess call to rfd3
    # rfd3 design out_dir=... inputs=...
    raise NotImplementedError("CLI backend not yet implemented. Use stub for development.")


def run_api(config: RDF3Config, api_url: str, api_key: Optional[str] = None) -> list[RDF3Result]:
    """
    Run RDF3 via HTTP API (e.g. Tamarind, custom).
    """
    import requests

    # TODO: Implement API submission and result polling
    raise NotImplementedError("API backend not yet implemented. Use stub for development.")


def run(config: RDF3Config, backend: str = "stub", **kwargs: Any) -> list[RDF3Result]:
    """
    Run RDF3 with the specified backend.

    Args:
        config: Design configuration
        backend: "stub" | "cli" | "api"
        **kwargs: Backend-specific options (out_dir for CLI, api_url for API)

    Returns:
        List of RDF3Result
    """
    if backend == "stub":
        return run_stub(config)
    if backend == "cli":
        return run_cli(config, out_dir=kwargs.get("out_dir", Path("/tmp/rdf3_out")))
    if backend == "api":
        return run_api(
            config,
            api_url=kwargs.get("api_url", ""),
            api_key=kwargs.get("api_key"),
        )
    raise ValueError(f"Unknown backend: {backend}")
