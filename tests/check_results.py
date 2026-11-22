"""Checks for the Module 5 project: reads to a count table.

Run from the repository folder:  python tests/check_results.py
Python 3 standard library only. It reads the files you commit in scripts/
and results/; it does not run FastQC, fastp, HISAT2, samtools or
featureCounts. Numbers are checked with a small tolerance, so newer tool
versions that differ by a read or two still pass.
"""

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Fingerprints of the untouched starter scripts, so the check can tell
# whether you have started work on them.
STARTER = {
    "scripts/pipeline.sh": "a5f994518d9a036da31b885a9c1bc09500fa12b0b84bd149872d6368f12d4ce8",
    "scripts/summarise.sh": "005965a54a0a8eaad188c6edfd537239e0d7387ceba4d1ca4622f68ab665a9b3",
}

SAMPLES = ["ctrl_1", "ctrl_2", "treat_1", "treat_2"]
PAIRS = {"ctrl_1": 9000, "ctrl_2": 11000, "treat_1": 10000, "treat_2": 8500}
ADAPTER_READS = {"ctrl_1": 1164, "ctrl_2": 1510, "treat_1": 1493, "treat_2": 1116}
ASSIGNED = {"ctrl_1": 8998, "ctrl_2": 10999, "treat_1": 10000, "treat_2": 8500}
GENES = ["PRG%03d" % i for i in range(1, 13)]
COUNTS = {
    "ctrl_1":  [234, 1047, 653, 192, 3161, 295, 344, 47, 384, 2287, 335, 19],
    "ctrl_2":  [366, 1674, 845, 156, 3945, 373, 796, 80, 442, 1995, 300, 27],
    "treat_1": [251, 1193, 1800, 358, 2461, 216, 102, 25, 370, 2984, 218, 22],
    "treat_2": [158, 941, 1393, 277, 2545, 175, 105, 26, 310, 2322, 239, 9],
}


class Fail(Exception):
    pass


def fingerprint(path):
    text = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    text = "\n".join(line.rstrip() for line in text.split("\n")).strip()
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def need_edited(rel):
    path = ROOT / rel
    if not path.is_file():
        raise Fail(f"{rel} is missing; keep the file and write your code in it")
    if fingerprint(path) == STARTER.get(rel):
        raise Fail(f"{rel} is still the untouched starter; write your code under the TODO comments")


def read_text(rel, hint):
    path = ROOT / rel
    if not path.is_file():
        raise Fail(f"{rel} not found; {hint}")
    text = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    if not text.strip():
        raise Fail(f"{rel} is empty; {hint}")
    return text


def sample_of(name):
    """aligned/ctrl_1.bam, ctrl_1.bam or ctrl_1 -> ctrl_1 (or None)"""
    m = re.search(r"(ctrl_[12]|treat_[12])", name)
    return m.group(1) if m else None


def close(value, target, rel_tol, abs_tol):
    return abs(value - target) <= max(abs_tol, rel_tol * target)


def code_only(text):
    return "\n".join(l for l in text.split("\n") if not l.strip().startswith("#"))


def count_table():
    rel = "results/practice_counts.txt"
    text = read_text(rel, "the pipeline should copy counts/practice_counts.txt into results/")
    lines = [l for l in text.split("\n") if l.strip()]
    header = None
    rows = {}
    for line in lines:
        cols = line.split("\t")
        if cols[0] == "Geneid":
            header = cols
        elif cols[0] in GENES:
            rows[cols[0]] = cols
    if header is None:
        raise Fail(f"{rel} has no 'Geneid' header line; commit the featureCounts output itself")
    cols = {}
    for i, name in enumerate(header[1:], 1):
        s = sample_of(name)
        if s:
            cols[s] = i
    if sorted(cols) != sorted(SAMPLES):
        raise Fail(f"{rel} should have one count column per sample (ctrl_1, ctrl_2, treat_1, treat_2); found {', '.join(header[6:]) or 'none'}")
    if len(rows) != 12:
        raise Fail(f"expected 12 genes in {rel}, found {len(rows)}; count with -t exon -g gene_id")
    table = {}
    for s, i in cols.items():
        try:
            table[s] = [int(rows[g][i]) for g in GENES]
        except (ValueError, IndexError):
            raise Fail(f"{rel}: the {s} column should hold whole numbers")
    return rel, table


# ---------------------------------------------------------------- tasks

def task1():
    need_edited("scripts/pipeline.sh")
    text = read_text("scripts/pipeline.sh", "keep the script in scripts/")
    code = code_only(text)
    if not re.search(r"^\s*set\s+-euo\s+pipefail|^\s*set\s+-[a-z]*e[a-z]*u[a-z]*o\s+pipefail", code, re.M):
        raise Fail("scripts/pipeline.sh should use set -euo pipefail")
    low = code.lower()
    for tool, pattern in [("FastQC", r"\bfastqc\b"), ("fastp", r"\bfastp\b"),
                          ("hisat2-build", r"hisat2-build"), ("HISAT2", r"\bhisat2\s"),
                          ("samtools sort", r"samtools\s+sort"), ("samtools index", r"samtools\s+index"),
                          ("featureCounts", r"featurecounts")]:
        if not re.search(pattern, low):
            raise Fail(f"scripts/pipeline.sh does not run {tool} yet")
    if "practice_samples.csv" not in code:
        raise Fail("scripts/pipeline.sh should take the sample names from data/practice_samples.csv")
    rel = "results/aligned_files.txt"
    listing = read_text(rel, "run the whole pipeline; its last lines write this file")
    names = set(listing.split())
    for s in SAMPLES:
        if f"{s}.bam" not in names:
            raise Fail(f"{rel} has no {s}.bam; the pipeline should align every sample in the sample sheet")
        if f"{s}.bam.bai" not in names and f"{s}.bai" not in names:
            raise Fail(f"{rel} has no index for {s}.bam; run samtools index on every BAM file")
    logs = ROOT / "results" / "logs"
    texts = {p.name: p.read_text(encoding="utf-8", errors="replace")
             for p in logs.glob("*") if p.is_file()} if logs.is_dir() else {}
    for s in SAMPLES:
        mine = [t for n, t in texts.items() if sample_of(n) == s]
        if not any("Read1 before filtering" in t for t in mine):
            raise Fail(f"no fastp log for {s} in results/logs/; save fastp's summary with 2> trimmed/{s}_fastp.log")
        if not any("overall alignment rate" in t for t in mine):
            raise Fail(f"no HISAT2 log for {s} in results/logs/; save HISAT2's summary with 2> aligned/{s}.log")
    count_table()


def task2():
    need_edited("scripts/summarise.sh")
    rel = "results/qc_table.tsv"
    text = read_text(rel, "run ./scripts/summarise.sh after the pipeline")
    rows = {}
    for line in text.split("\n"):
        cols = [c.strip() for c in line.split("\t")]
        s = sample_of(cols[0]) if cols and cols[0] else None
        if s and cols[0] == s:
            if len(cols) < 5:
                raise Fail(f"{rel}: the row for {s} needs 5 tab-separated columns: sample, raw_pairs, trimmed_pairs, adapter_trimmed_reads, alignment_rate")
            rows[s] = cols
    missing = [s for s in SAMPLES if s not in rows]
    if missing:
        raise Fail(f"{rel} has no row for {', '.join(missing)}")
    for s in SAMPLES:
        try:
            raw, kept, adapter = (float(rows[s][i].replace(",", "")) for i in (1, 2, 3))
            rate = float(rows[s][4].rstrip("%"))
        except ValueError:
            raise Fail(f"{rel}: the row for {s} should hold numbers after the sample name")
        if raw == 2 * PAIRS[s] or kept == 2 * PAIRS[s]:
            raise Fail(f"{rel}: {s} shows {int(raw)} pairs; that counts read 1 and read 2 together, so take the Read1 total")
        if raw != PAIRS[s]:
            raise Fail(f"{rel}: raw_pairs for {s} does not match the checkpoint; use 'total reads' under 'Read1 before filtering'")
        if kept != PAIRS[s]:
            raise Fail(f"{rel}: trimmed_pairs for {s} should be the Read1 total after filtering; no pairs should be lost")
        if not close(adapter, ADAPTER_READS[s], 0.05, 5):
            if close(adapter * 2, ADAPTER_READS[s], 0.05, 5):
                raise Fail(f"{rel}: adapter_trimmed_reads for {s} looks halved; give the number as fastp reports it")
            raise Fail(f"{rel}: adapter_trimmed_reads for {s} does not match the fastp log; use the line 'reads with adapter trimmed'")
        if rate <= 1:
            raise Fail(f"{rel}: the alignment rate for {s} looks like a fraction; give it as a percentage, as HISAT2 prints it")
        if not 99.5 <= rate <= 100:
            raise Fail(f"{rel}: the alignment rate for {s} is {rate}%, outside 99.6-99.9%; align the trimmed reads, as a pair (-1 and -2)")


def task3():
    rel, table = count_table()
    for s in SAMPLES:
        for g, got, want in zip(GENES, table[s], COUNTS[s]):
            if not close(got, want, 0.02, 3):
                if close(got, 2 * want, 0.05, 5):
                    raise Fail(f"{rel}: {g} in {s} is about twice the expected count; count each pair once with -p --countReadPairs")
                raise Fail(f"{rel}: the count of {g} in {s} is far from the checkpoint; check the trimming, alignment and featureCounts settings")
    for s in ("ctrl_1", "ctrl_2"):
        if GENES[max(range(12), key=lambda i: table[s][i])] != "PRG005":
            raise Fail(f"{rel}: PRG005 should have the most reads in {s}")
    if GENES[max(range(12), key=lambda i: table["treat_1"][i])] != "PRG010":
        raise Fail(f"{rel}: PRG010 should have the most reads in treat_1")
    srel = "results/practice_counts.txt.summary"
    text = read_text(srel, "the pipeline should copy counts/practice_counts.txt.summary into results/")
    lines = [l.split("\t") for l in text.split("\n") if l.strip()]
    head = lines[0]
    assigned = [l for l in lines if l[0] == "Assigned"]
    if not assigned:
        raise Fail(f"{srel} has no 'Assigned' row; commit the featureCounts summary file")
    for i, name in enumerate(head[1:], 1):
        s = sample_of(name)
        if s and not close(int(assigned[0][i]), ASSIGNED[s], 0.005, 2):
            raise Fail(f"{srel}: Assigned pairs for {s} do not match the checkpoint; nearly every pair should be assigned")
    need_edited("scripts/summarise.sh")
    rel = "results/counts_sorted.tsv"
    text = read_text(rel, "save the sorted gene IDs and four count columns from summarise.sh")
    lines = [l for l in text.split("\n") if l.strip()]
    body = []
    for n, line in enumerate(lines):
        cols = line.split("\t")
        if cols[0] in GENES:
            body.append(cols)
        elif cols[0].startswith("#"):
            raise Fail(f"{rel} still has the # comment line; skip the first line of the featureCounts file")
        elif body:
            raise Fail(f"{rel}: the header line ended up among the genes; sort only the gene rows and keep the header on top")
    if len(body) != 12:
        raise Fail(f"expected 12 gene rows in {rel}, found {len(body)}")
    if any(len(c) != 5 for c in body):
        raise Fail(f"{rel} should keep the gene ID and the four count columns only (cut -f 1,7-)")
    try:
        values = [[int(c[i]) for c in body] for i in range(1, 5)]
    except ValueError:
        raise Fail(f"{rel}: the count columns should hold whole numbers")
    if not any(all(v[j] >= v[j + 1] for j in range(11)) for v in values):
        if any(all(v[j] <= v[j + 1] for j in range(11)) for v in values):
            raise Fail(f"{rel} is sorted smallest first; sort largest first (r)")
        raise Fail(f"{rel} is not sorted by any sample as numbers; use sort -k2,2nr (n = numeric, r = largest first)")


def section(text, name):
    m = re.search(rf"^#+\s*{name}\b(.*?)(?=^#+\s|\Z)", text, re.S | re.M | re.I)
    return m.group(1) if m else ""


def task4():
    rel = "results/methods.md"
    text = read_text(rel, "write your methods paragraph and limitations in results/methods.md")
    meth = section(text, "Methods").lower()
    if not meth.strip():
        raise Fail(f"{rel} needs a '## Methods' section")
    tools = [("FastQC", r"fastqc"), ("fastp", r"fastp"), ("HISAT2", r"hisat2?"),
             ("samtools", r"samtools"), ("featureCounts or Subread", r"(featurecounts|subread)")]
    no_version = [name for name, pat in tools if not re.search(pat + r"\D{0,25}\d+\.\d+", meth)]
    if no_version:
        raise Fail("your methods do not yet give " + ", ".join(no_version) + " with a version number")
    needs = [("the fastp quality cut-off (20)", r"cut_mean_quality\D{0,5}20|quality\D{0,30}20"),
             ("the minimum read length (36)", r"\b36\b"),
             ("how pairs were counted (--countReadPairs)", r"countreadpairs|read pairs|fragments"),
             ("what was counted (-t exon -g gene_id)", r"exon"),
             ("the genome file", r"practice_genome"),
             ("the annotation file", r"practice_genes")]
    missing = [name for name, pat in needs if not re.search(pat, meth)]
    if missing:
        raise Fail("your methods do not yet give " + "; ".join(missing))
    lim = section(text, "Limitations").lower()
    if not lim.strip():
        raise Fail(f"{rel} needs a '## Limitations' section with two limitations")
    lim_missing = []
    if not re.search(r"(two|2)\s+(biological\s+)?(replicates?|samples?)|replicate", lim):
        lim_missing.append("how many samples each group has")
    if not re.search(r"simulat|synthetic", lim):
        lim_missing.append("where the data came from")
    if lim_missing:
        raise Fail("your limitations do not yet mention " + " or ".join(lim_missing))


TASKS = [
    ("Task 1 · One pipeline script", task1),
    ("Task 2 · A QC table", task2),
    ("Task 3 · Read the count table", task3),
    ("Task 4 · Methods and limitations", task4),
]


def main():
    failed = 0
    for name, check in TASKS:
        try:
            check()
            print(f"PASS  {name}")
        except Fail as exc:
            failed += 1
            print(f"FAIL  {name}: {exc}")
    print()
    if failed:
        print(f"{failed} of {len(TASKS)} checks failed. Read the message for each failed task, fix it, commit and push again.")
    else:
        print("Every checkpoint passed. Well done.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
