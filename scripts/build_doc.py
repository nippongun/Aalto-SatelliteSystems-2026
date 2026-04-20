#!/usr/bin/env python3
"""scripts/build_doc.py — Assemble Markdown sections and build styled DOCX.

Usage:
    python scripts/build_doc.py
    python scripts/build_doc.py --config path/to/mission_config.yaml
    python scripts/build_doc.py --content-dir path/to/content/ --output-dir path/to/output/

Requires: pandoc 3.x, templates/course_template.docx, content/0*.md
Cross-platform: Windows, Linux, macOS
"""
import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile
from datetime import date

import yaml


def main() -> None:
    repo_root = pathlib.Path(__file__).parent.parent

    parser = argparse.ArgumentParser(description="Build styled DOCX from Markdown sections")
    parser.add_argument("--config", default=str(repo_root / "mission_config.yaml"),
                        help="Path to mission_config.yaml")
    parser.add_argument("--content-dir", default=str(repo_root / "content"),
                        help="Directory containing 0*.md section files")
    parser.add_argument("--template", default=str(repo_root / "templates" / "course_template.docx"),
                        help="Pandoc reference DOCX template")
    parser.add_argument("--output-dir", default=str(repo_root / "output"),
                        help="Directory to write the output DOCX into")
    args = parser.parse_args()

    config_path = pathlib.Path(args.config)
    content_dir = pathlib.Path(args.content_dir)
    template = pathlib.Path(args.template)
    output_dir = pathlib.Path(args.output_dir)

    # Verify pandoc
    if shutil.which("pandoc") is None:
        print("ERROR: pandoc not found.", file=sys.stderr)
        print("  Linux:   sudo apt install pandoc  /  sudo pacman -S pandoc", file=sys.stderr)
        print("  macOS:   brew install pandoc", file=sys.stderr)
        print("  Windows: https://pandoc.org/installing.html", file=sys.stderr)
        sys.exit(1)

    # Verify template
    if not template.exists():
        print(f"ERROR: Template not found at {template}", file=sys.stderr)
        sys.exit(1)

    # Verify config
    if not config_path.exists():
        print(f"ERROR: Config not found at {config_path}", file=sys.stderr)
        sys.exit(1)

    # Collect content files in numeric order
    content_files = sorted(content_dir.glob("0*.md"))
    if not content_files:
        print(f"ERROR: No content files matching 0*.md found in {content_dir}", file=sys.stderr)
        sys.exit(1)

    # Read metadata
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    mission_name = config.get("mission_name", "Satellite Mission")
    authors = config.get("authors", "")
    build_date = date.today().isoformat()
    doc_name = config.get("document_name", "mission_feasibility")

    # Assemble sections into a temporary file
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{doc_name}_{date.today().strftime('%Y%m%d')}.docx"

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp:
        for section in content_files:
            tmp.write(section.read_text(encoding="utf-8"))
            tmp.write("\n\n")
        tmp_path = pathlib.Path(tmp.name)

    try:
        subprocess.run(
            [
                "pandoc", str(tmp_path),
                "-o", str(output_file),
                f"--reference-doc={template}",
                "--toc",
                "--toc-depth=3",
                "--from", "markdown+pipe_tables+grid_tables",
                "--metadata", f"title={mission_name}",
                "--metadata", f"author={authors}",
                "--metadata", f"date={build_date}",
            ],
            check=True,
        )
    finally:
        tmp_path.unlink(missing_ok=True)

    _fix_toc_field(output_file)
    print(f"Built: {output_file}")


def _fix_toc_field(docx_path: pathlib.Path) -> None:
    """Replace pandoc's outline-level TOC field with a style-name TOC field.

    pandoc emits  TOC \\o "1-3"  which requires outline levels to be set in
    the template styles.  Switching to  TOC \\t "Heading 1,1,..."  works on
    any template that uses standard heading style names.
    """
    import zipfile, shutil

    import re as _re
    old_pattern = _re.compile(r'TOC\\o\s*&quot;1-3&quot;(\s*\\[hzu])*|TOC\s*\\[to][^\s<]*[^<]*?(?=</w:instrText>)')

    tmp = docx_path.with_suffix(".tmp.docx")
    shutil.copy2(docx_path, tmp)
    with zipfile.ZipFile(tmp, "r") as zin, zipfile.ZipFile(docx_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                text = data.decode("utf-8")
                # Replace the full instrText content between the tags
                text = _re.sub(
                    r'(<w:instrText[^>]*>)[^<]*(</w:instrText>)',
                    lambda m: m.group(1) + r'TOC \t &quot;Heading 1,1,Heading 2,2,Heading 3,3&quot; \h' + m.group(2),
                    text,
                    count=1,
                )
                data = text.encode("utf-8")
            zout.writestr(item, data)
    tmp.unlink()


if __name__ == "__main__":
    main()
