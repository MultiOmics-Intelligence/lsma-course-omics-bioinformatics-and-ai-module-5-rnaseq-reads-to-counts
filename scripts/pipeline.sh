#!/usr/bin/env bash
# pipeline.sh: raw reads to a count table for every sample in data/practice_samples.csv
# (Module 5 project, Task 1)
#
# Usage (from the top folder of this repository, with the hts environment active):
#   ./scripts/pipeline.sh
#
# Folders, as in lesson 1: data -> qc -> trimmed -> index -> aligned -> counts.
# Only data/ and results/ are committed; the other folders are rebuilt by every run.

# TODO Task 1 · strict mode
#   Add the line that stops the script at the first failed command, at an
#   unset variable, and when any part of a pipe fails (lesson 6 of Module 3).


mkdir -p qc trimmed index aligned counts results/logs

# TODO Task 1 · build the HISAT2 index, once (lesson 4)


# TODO Task 1 · read the sample names from data/practice_samples.csv
#   Skip the header line and keep the first column, for example with
#   tail -n +2 and cut -d , -f 1, and loop over the names.

for s in ctrl_1; do   # TODO replace this fixed list with the names from the CSV

  # TODO Task 1 · FastQC on both reads (lesson 2)


  # TODO Task 1 · fastp, with the settings from lesson 3; save the summary
  #   it prints to trimmed/${s}_fastp.log with 2>


  # TODO Task 1 · HISAT2 into samtools sort, then samtools index (lesson 4);
  #   save the HISAT2 summary to aligned/${s}.log with 2>

  :   # placeholder, remove it when you add your code
done

# TODO Task 1 · featureCounts on all four BAM files at once (lesson 5), writing
#   counts/practice_counts.txt


# Hand-in copies: this part is given, keep it at the end of the script.
cp trimmed/*_fastp.log aligned/*.log results/logs/
cp counts/practice_counts.txt counts/practice_counts.txt.summary results/
ls aligned > results/aligned_files.txt
