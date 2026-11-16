#!/usr/bin/env bash
# Exit immediately if any command fails
set -e

echo "=============================================="
echo "Step 1: Running ROOT data plotting script..."
echo "=============================================="
# Replace 'draw_analysis.py' with your actual Python data script name if different
#python3 generate_plots.py

echo ""
echo "=============================================="
echo "Step 2: Generating LaTeX Beamer slides (.tex)..."
echo "=============================================="
python3 generate_slides.py

echo ""
echo "=============================================="
echo "Step 3: Compiling presentation with pdflatex..."
echo "=============================================="
pdflatex -interaction=nonstopmode presentation.tex
pdflatex -interaction=nonstopmode presentation.tex  # Run twice to ensure table of contents and slide counts align

echo ""
echo "=============================================="
echo "Pipeline complete! Output saved to presentation.pdf"
echo "=============================================="
