<a href="https://lsma.co.uk/courses"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/lsma-walk-courses.svg" alt="LSMA, London School of Multiomics and AI: learn by doing, on real data" width="100%"></a>

# Module 5 project: Reads to a count table

LSMA · Omics, Bioinformatics and AI · Module 5 project

<p>
<img src="https://img.shields.io/badge/LSMA-free%20course-D9481F?style=flat-square" alt="LSMA free course">
<img src="https://img.shields.io/badge/course-Omics%2C%20Bioinformatics%20and%20AI-0F1B33?style=flat-square" alt="Course">
<img src="https://img.shields.io/badge/language-Bash%20%7C%20Python-4EAA25?style=flat-square&logo=gnubash&logoColor=white" alt="Language">
<img src="https://img.shields.io/badge/checks-automatic-2F7D5B?style=flat-square&logo=githubactions&logoColor=white" alt="Automatic checks">
</p>

## Research question

Can one script take four samples from raw reads to a clean count table, and do the counts already
hint at the genes that treatment changes?

In lessons 1–5 you ran each tool by hand, often on one sample at a time. This project joins those
commands into a single pipeline script that runs from start to finish without you typing anything in
between. The goal is not new biology. It is a result you can rebuild from scratch at any time.

## What you will build

**In:** paired FASTQ files for four samples (`ctrl_1`, `ctrl_2`, `treat_1`, `treat_2`), the practice
genome, the gene annotation and the sample sheet, all in `data/`. See `data/README.md`.

**Out:** two scripts and, in `results/`, the files the check reads:

| Task | File | What it holds |
|---|---|---|
| 1 | `scripts/pipeline.sh` | FastQC, fastp, HISAT2, samtools and featureCounts for every sample in the sample sheet |
| 1 | `results/aligned_files.txt`, `results/logs/` | written by the last lines of the pipeline: the BAM files made, and every fastp and HISAT2 log |
| 1, 3 | `results/practice_counts.txt`, `results/practice_counts.txt.summary` | the featureCounts table and its summary, copied by the pipeline |
| 2 | `scripts/summarise.sh` → `results/qc_table.tsv` | one row per sample: `sample`, `raw_pairs`, `trimmed_pairs`, `adapter_trimmed_reads`, `alignment_rate` |
| 3 | `scripts/summarise.sh` → `results/counts_sorted.tsv` | the gene IDs and the four count columns, sorted by one sample |
| 4 | `results/methods.md` | a `## Methods` section and a `## Limitations` section |

The big files the pipeline makes (`qc/`, `trimmed/`, `index/`, `aligned/`, `counts/`) stay on your
computer: `.gitignore` keeps them out of your commits.

## Before you start

1. Get your own copy of this repository. Use the GitHub Classroom invitation link in the project
   lesson on lsma.co.uk, or click **Use this template** on GitHub.
2. Clone your copy on the computer where you will run the tools: your own computer, or the LSMA
   Analysis Lab. Open a terminal in its top folder.
3. Make the conda environment from lesson 1, once, and activate it:

   ```
   conda create -n hts -c conda-forge -c bioconda seqkit fastqc fastp hisat2 samtools subread
   conda activate hts
   ```

4. Work in `scripts/`, write what you hand in to `results/`, and never edit `data/`.

Work on one sample first. Get every step working for `ctrl_1`, check its output against the lessons,
and only then loop over all four samples. When the script works, delete the output folders and run
it again: if it only works because of files left over from earlier attempts, it is not finished.
The data were simulated, so the checkpoints tell you exactly what a correct run produces. A mismatch
is a clue to a bug, not a result to explain away.

## Tasks

### 1. One pipeline script

Write `scripts/pipeline.sh` that runs FastQC, fastp, HISAT2, samtools and featureCounts for every
sample listed in `data/practice_samples.csv`. Use `set -euo pipefail`, and keep each tool's log. Build
the HISAT2 index once, not once per sample. Keep the given lines at the end of the script: they copy
the logs and the count table into `results/`. Then run it from empty:

```
rm -rf qc trimmed index aligned counts
./scripts/pipeline.sh
```

Lesson to revisit: lessons 1–5.

**Checkpoint:** one run produces 4 BAM files, their indexes, and `counts/practice_counts.txt` from
scratch.

### 2. A QC table

Collect, per sample: raw pairs, pairs after trimming, reads with adapter trimmed, and overall
alignment rate. Write the code in the Task 2 part of `scripts/summarise.sh`. Every number is already
in a log your pipeline kept. Watch the units: fastp reports reads, and counts Read1 and Read2
separately, while the table asks for pairs.

Lesson to revisit: lessons 2–4.

**Checkpoint:** raw pairs 9,000, 11,000, 10,000 and 8,500; no pairs lost in trimming; alignment rates
between 99.6% and 99.9%.

### 3. Read the count table

On the command line, show the gene IDs and the four count columns of `counts/practice_counts.txt`,
sorted by one sample, and save them with the Task 3 part of `scripts/summarise.sh`. Check in
`practice_counts.txt.summary` that every sample has nearly all its pairs assigned. Then run:

```
./scripts/summarise.sh
```

Lesson to revisit: lesson 5.

**Checkpoint:** 12 genes × 4 samples; PRG005 has the most reads in the control samples, and PRG010,
which treatment induces, in treat_1. Assigned pairs: 8,998, 10,999, 10,000 and 8,500.

### 4. Methods and limitations

Write `results/methods.md` with a `## Methods` heading and a `## Limitations` heading. The methods
give every tool, version and setting, exactly as in your script (the trimming thresholds and the
featureCounts options), and name the genome and annotation files. Record the versions from the
environment you ran (`fastqc --version`, `fastp --version`, `hisat2 --version`, `samtools --version`,
`featureCounts -v`). List two limitations of this experiment.

Lesson to revisit: lessons 1–6.

**Checkpoint:** someone could rerun your pipeline from your methods alone; your limitations mention
two replicates per group and simulated data.

## Hand in

Commit and push `scripts/` and `results/`. The **Checks** tab (GitHub Actions) then runs
automatically. A green tick means every checkpoint passed. You can push as often as you like.

You can run the same check on your own computer first: `python3 tests/check_results.py`. It does not
need any of the tools: it reads the files you saved, and checks the numbers with a small tolerance.

## If a check fails

Open the **Actions** tab, click the latest run and read the log. Each line names a task and says what
to look at, for example:

```
FAIL  Task 2 · A QC table: results/qc_table.tsv: ctrl_1 shows 18000 pairs; that counts read 1 and read 2 together, so take the Read1 total
```

Fix that task, rerun your scripts, commit the new results and push again.

## Getting help

- The project lesson on lsma.co.uk, and the lessons named under each task.
- Helix, the course tutor.
- Email info@lsma.co.uk.

Never post personal data in a public place, including issues and discussions on GitHub.

**Follow LSMA**

<p>
  <a href="https://lsma.co.uk"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-website.svg" alt="LSMA: lsma.co.uk" height="54"></a>
  <a href="https://www.linkedin.com/showcase/113252126/"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-linkedin.svg" alt="LSMA on LinkedIn" height="54"></a>
  <a href="https://www.instagram.com/lsma.uk/"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-instagram.svg" alt="LSMA on Instagram: @lsma.uk" height="54"></a>
  <a href="mailto:info@lsma.co.uk"><img src="https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/btn-lsma-email.svg" alt="Email: info@lsma.co.uk" height="54"></a>
</p>

Good luck, and enjoy the project.

**Dr. Anas Alzaeem**<br>
Academic Director, LSMA

[![Dr. Anas Alzaeem, Academic Director, LSMA](https://raw.githubusercontent.com/MultiOmics-Intelligence/.github/main/assets/signature/LSMA_Banner_Anas_Alzaeem.png)](https://lsma.co.uk)

© 2026 MultiOmics Intelligence Ltd. LSMA is the education arm of MultiOmics Intelligence. Code licensed under MIT.
