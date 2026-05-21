"""
HTSplotter - Drug Screen Example (1 time point)
================================================
This script runs a single-drug dose-response analysis on the example
dataset included with HTSplotter.

Input data:  3 drugs (MK-1775, BAY1895344, Prexasertib) tested on MCF7 cells
Read-out:    Confluency (%)
Output:      PDF report + IC values + HDF5 data file
"""

import os
from HTSplotter.main import Analyser

# --- Paths ---
REPO_DIR   = os.path.expanduser("~/HTSplotter/repo")
INPUT_DIR  = os.path.join(REPO_DIR, "experiment_type/drug/inputfile")

OUTPUT_DIR = os.path.expanduser("~/HTSplotter/my_results/drugscreen_1timepoint")
RESULTS_DIR     = os.path.join(OUTPUT_DIR, "output_results")
INFO_DIR        = os.path.join(OUTPUT_DIR, "information_extracted")

# --- Run ---
analyser = Analyser()

analyser.main_folder          = OUTPUT_DIR + "/"
analyser.input_path           = INPUT_DIR + "/"
analyser.information_extracted = INFO_DIR + "/"
analyser.results_path         = RESULTS_DIR + "/"

analyser.biological_replicate = 0          # 0 = single experiment (not a biological replicate set)
analyser.userinput            = 0          # 0 = no manual confirmation step
analyser.information_readout  = "Confluency"  # label shown on plots
analyser.readout_units        = "(%)"      # units shown on plots
analyser.expected_effect      = 0          # 0 = inhibition (drug reduces confluency)
analyser.synergy_method       = 0          # 0 = Bliss (not used for single drugs, but required)

# The file name(s) to analyse — no extension, just the base name
analyser.files_list = ["drugscreen_1timepoint"]

print("Starting HTSplotter analysis...")
analyser.execute()
print(f"\nDone! Results saved to:\n  {RESULTS_DIR}")
