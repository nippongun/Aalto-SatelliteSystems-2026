import pathlib
import subprocess
import sys


REPO_ROOT = pathlib.Path(__file__).parent.parent
TEMPLATE = REPO_ROOT / "templates" / "course_template.docx"


def test_build_produces_docx(tmp_path, tmp_config):
    """build_doc.py assembles content files and produces a .docx in output-dir."""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "01_intro.md").write_text(
        "# Introduction\n\nThis is a test section.\n", encoding="utf-8"
    )
    (content_dir / "02_body.md").write_text(
        "# Body\n\n## Subsection\n\nBody text.\n", encoding="utf-8"
    )

    output_dir = tmp_path / "output"

    result = subprocess.run(
        [
            sys.executable, "scripts/build_doc.py",
            "--config", str(tmp_config),
            "--content-dir", str(content_dir),
            "--template", str(TEMPLATE),
            "--output-dir", str(output_dir),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"build_doc.py failed:\n{result.stderr}"
    docx_files = list(output_dir.glob("mission_feasibility_*.docx"))
    assert len(docx_files) == 1, f"Expected one output file, got: {docx_files}"
    assert docx_files[0].stat().st_size > 0, "Output DOCX is empty"


def test_build_fails_without_pandoc(tmp_path, tmp_config, monkeypatch):
    """build_doc.py exits non-zero with a clear message when pandoc is not found."""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "01_intro.md").write_text("# Intro\n\nText.\n", encoding="utf-8")

    # Hide pandoc from PATH
    monkeypatch.setenv("PATH", str(tmp_path))

    result = subprocess.run(
        [
            sys.executable, "scripts/build_doc.py",
            "--config", str(tmp_config),
            "--content-dir", str(content_dir),
            "--template", str(TEMPLATE),
            "--output-dir", str(tmp_path / "output"),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "pandoc" in result.stderr.lower()


def test_build_fails_without_content(tmp_path, tmp_config):
    """build_doc.py exits non-zero when no 0*.md files exist in content-dir."""
    empty_dir = tmp_path / "content"
    empty_dir.mkdir()

    result = subprocess.run(
        [
            sys.executable, "scripts/build_doc.py",
            "--config", str(tmp_config),
            "--content-dir", str(empty_dir),
            "--template", str(TEMPLATE),
            "--output-dir", str(tmp_path / "output"),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "content" in result.stderr.lower() or "0*.md" in result.stderr
