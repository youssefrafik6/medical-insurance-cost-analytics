"""Refresh report inputs and optionally render with Quarto."""

import argparse
import os
import subprocess

from python.data_loader import ROOT
from python.reporting import build_results


def main() -> None:
    """Generate analytics and render the selected report format."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", choices=["html", "pdf"])
    args = parser.parse_args()
    build_results()
    if args.render:
        subprocess.run(
            [
                os.environ.get("QUARTO_BIN", "quarto"),
                "render",
                "reports/analysis_report.qmd",
                "--to",
                "typst" if args.render == "pdf" else "html",
            ],
            cwd=ROOT,
            check=True,
        )


if __name__ == "__main__":
    main()
