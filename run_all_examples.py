"""
HTSplotter - Run All Remaining Example Datasets
================================================
Runs 8 example analyses covering drug screens (multi-timepoint),
drug combinations (multi-timepoint), genetic perturbagen, and
genetic-chemical perturbagen experiment types.
"""

import os
from HTSplotter.main import Analyser

REPO_DIR   = os.path.expanduser("~/HTSplotter/repo")
BASE_OUT   = os.path.expanduser("~/HTSplotter/my_results")

def run(label, input_subdir, filename, output_subdir,
        readout="Confluency", units="(%)", synergy=0):
    print(f"\n{'='*60}")
    print(f"  Running: {label}")
    print(f"{'='*60}")

    out = os.path.join(BASE_OUT, output_subdir)
    a = Analyser()
    a.main_folder           = out + "/"
    a.input_path            = os.path.join(REPO_DIR, "experiment_type", input_subdir) + "/"
    a.information_extracted = os.path.join(out, "information_extracted") + "/"
    a.results_path          = os.path.join(out, "output_results") + "/"
    a.biological_replicate  = 0
    a.userinput             = 0
    a.information_readout   = readout
    a.readout_units         = units
    a.expected_effect       = 0
    a.synergy_method        = synergy
    a.files_list            = [filename]
    a.execute()
    print(f"  Done → {a.results_path}")


# ── Drug screen (multi-timepoint) ───────────────────────────────────────────
run("Drug screen — several time points, 1 control",
    "drug/inputfile",
    "drugscreen_severaltimepoint_1control",
    "drugscreen_multitime_1ctrl")

run("Drug screen — several time points, several controls",
    "drug/inputfile",
    "drugscreen_severaltimepoint_severalcontrol",
    "drugscreen_multitime_multictl")

# ── Drug combination (multi-timepoint) ──────────────────────────────────────
run("Drug combination — several time points",
    "drug_combination/inputfile",
    "drug_combination_several_time_points",
    "drugcombination_multitime")

run("Drug combination — several time points, repetitive conditions",
    "drug_combination/inputfile",
    "drug_combination_several_time_points_repetitive_conditions",
    "drugcombination_multitime_repetitive")

# ── Genetic perturbagen ──────────────────────────────────────────────────────
run("Genetic perturbagen — 1 time point",
    "genetic_pertubagen/inputfile",
    "gene_perturbagen_1timepoint_1control",
    "genetic_1timepoint")

run("Genetic perturbagen — several time points",
    "genetic_pertubagen/inputfile",
    "gene_perturbagen_severaltimepoints",
    "genetic_multitime")

# ── Genetic-chemical perturbagen ────────────────────────────────────────────
run("Genetic-chemical perturbagen — 1 time point",
    "genetic-chemical_perturbagens/inputfile",
    "genetic-chemical_perturbagen_1time_point",
    "genetic_chemical_1timepoint")

run("Genetic-chemical perturbagen — several time points",
    "genetic-chemical_perturbagens/inputfile",
    "genetic-chemical_perturbagen_several-time_points",
    "genetic_chemical_multitime")

print("\n\nAll analyses complete!")
