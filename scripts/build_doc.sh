#!/bin/bash
# scripts/build_doc.sh — Assemble Markdown sections and build styled DOCX
# Usage: bash scripts/build_doc.sh
# Requires: pandoc 3.x, templates/course_template.docx, content/0*.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

CONTENT_GLOB="$REPO_ROOT/content/0*.md"
TEMPLATE="$REPO_ROOT/templates/course_template.docx"
OUTPUT_DIR="$REPO_ROOT/output"
OUTPUT_FILE="$OUTPUT_DIR/mission_feasibility_$(date +%Y%m%d).docx"
TMP_FILE="/tmp/full_document.md"

# Verify dependencies
if ! command -v pandoc &>/dev/null; then
    echo "ERROR: pandoc not found. Install with: sudo pacman -S pandoc" >&2
    exit 1
fi

if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Course template not found at $TEMPLATE" >&2
    exit 1
fi

# Assemble sections in numeric order
# shellcheck disable=SC2086
cat $CONTENT_GLOB > "$TMP_FILE"

# Build DOCX
pandoc "$TMP_FILE" \
    -o "$OUTPUT_FILE" \
    --reference-doc="$TEMPLATE" \
    --toc \
    --toc-depth=3 \
    --from markdown+pipe_tables+grid_tables

echo "Built: $OUTPUT_FILE"
