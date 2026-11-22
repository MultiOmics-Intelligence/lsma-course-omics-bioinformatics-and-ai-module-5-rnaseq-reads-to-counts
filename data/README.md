# Data

The course files used in Module 5, Sequencing data. **Synthetic, made for teaching**: the reads were
simulated by a computer from a made-up practice genome. No real sample, organism or person is behind
them. They are built so that the numbers in the lessons come out when you run the lesson commands.

| File | What it is |
|---|---|
| `ctrl_1_R1.fastq.gz`, `ctrl_1_R2.fastq.gz` | control sample 1: read 1 and read 2 of 9,000 read pairs |
| `ctrl_2_R1.fastq.gz`, `ctrl_2_R2.fastq.gz` | control sample 2: 11,000 read pairs |
| `treat_1_R1.fastq.gz`, `treat_1_R2.fastq.gz` | treated sample 1: 10,000 read pairs |
| `treat_2_R1.fastq.gz`, `treat_2_R2.fastq.gz` | treated sample 2: 8,500 read pairs |
| `practice_genome.fa` | the practice genome: one sequence, `chrP`, 60,000 bases (FASTA) |
| `practice_genes.gtf` | 12 genes (PRG001 to PRG012) on `chrP`; three of them (PRG003, PRG007, PRG010) have two exons (GTF) |
| `practice_samples.csv` | the sample sheet: `sample` and `condition` (`control` or `treated`) |

All reads are 100 bases, gzip-compressed FASTQ with quality scores +33. The library is unstranded
(featureCounts `-s 0`). Some fragments are shorter than 100 bases, so their reads run on into the
Illumina adapter; quality falls along each read and some reads end in low-quality bases. Four genes
were built to change after treatment. The same count table is the input of the Introduction to R
Module 4 project.

**Source and licence.** Made by MultiOmics Intelligence Ltd for LSMA teaching with a script kept by
LSMA; free to reuse under the MIT licence of this repository.
