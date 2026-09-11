# BioInsight

A multi-agent biological data analysis platform built with Python, Anthropic's Claude API, FastAPI, and Streamlit.

## What it does
BioInsight analyzes biological data files — tabular datasets (CSV) and DNA sequence files (FASTA) — using 10 AI agents organized into 5 sections, producing a written, human-readable analysis report.

## Architecture

| Section | Agents | Job |
|---|---|---|
| 1. Data Intake | File Detective, Data Cleaner | Detect file type, check data quality |
| 2. Sequence Analysis | Sequence Reader, Pattern Finder | Parse DNA sequences, find motifs |
| 3. Statistical Analysis | Stats Analyst, Anomaly Spotter | Compute statistics, flag outliers |
| 4. Research Assistant | Literature Scout, Summarizer | Search and summarize scientific findings |
| 5. Reporting | Chart Maker, Report Writer | Generate charts and final report |

An orchestrator (`orchestrator.py`) routes uploaded files to the correct agents and combines their results into one final report.

## How to run

1. Install dependencies: