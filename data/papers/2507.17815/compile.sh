#!/bin/bash
cd "$(dirname "$0")/source"
pdflatex -interaction=nonstopmode -output-directory=.. ../personalized_annotated.tex
pdflatex -interaction=nonstopmode -output-directory=.. ../personalized_condensed.tex
