#!/usr/bin/env bash
# summarise.sh: the QC table and a sorted view of the count table (Module 5 project, Tasks 2 and 3)
#
# Usage (from the top folder of this repository, after pipeline.sh has run):
#   ./scripts/summarise.sh
#
# Writes results/qc_table.tsv and results/counts_sorted.tsv.

set -euo pipefail

# ---------------------------------------------------------------------
# Task 2 · A QC table (lessons 2-4)
# One row per sample, tab-separated, with this header:
#   sample  raw_pairs  trimmed_pairs  adapter_trimmed_reads  alignment_rate
# Every number is in a log the pipeline kept:
#   trimmed/<sample>_fastp.log  "total reads:" under "Read1 before filtering" and
#                               "Read1 after filtering", and "reads with adapter trimmed:"
#   aligned/<sample>.log        the last line, "... overall alignment rate"
# Watch the units: fastp counts reads, and Read1 and Read2 separately; the
# table asks for pairs (and for adapter-trimmed reads as fastp reports them).
# ---------------------------------------------------------------------

echo -e "sample\traw_pairs\ttrimmed_pairs\tadapter_trimmed_reads\talignment_rate" > results/qc_table.tsv

for s in $(tail -n +2 data/practice_samples.csv | cut -d , -f 1); do
  # TODO Task 2 · pull the four numbers for sample $s out of its two logs
  #   (grep for a fixed phrase, then keep the number, for example with awk or cut)
  #   and append one tab-separated row to results/qc_table.tsv with >>

  :   # placeholder, remove it when you add your code
done

# ---------------------------------------------------------------------
# Task 3 · Read the count table (lesson 5)
# Show the gene IDs and the four count columns of counts/practice_counts.txt,
# sorted by one sample, largest first, and save them to results/counts_sorted.tsv.
# Skip the first line (the # comment) and keep the header line on top: sort only
# the gene rows, and compare the values as numbers.
# ---------------------------------------------------------------------

# TODO Task 3
