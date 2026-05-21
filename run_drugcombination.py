"""
HTSplotter - Drug Combination Screen Example (1 time point)
============================================================
MK-1775 combined with Prexasertib and BAY1895344 in MCF7 cells.
Synergy is scored using the Bliss independence model.

Output: PDF report + synergy scores + IC values + HDF5 data file
"""

import os
from HTSplotter.main import Analyser

# --- Paths ---
REPO_DIR   = os.path.expanduser("~/HTSplotter/repo")
INPUT_DIR  = os.path.join(REPO_DIR, "experiment_type/drug_combination/inputfile")

OUTPUT_DIR  = os.path.expanduser("~/HTSplotter/my_results/drugcombination_1timepoint")
RESULTS_DIR = os.path.join(OUTPUT_DIR, "output_results")
INFO_DIR    = os.path.join(OUTPUT_DIR, "information_extracted")

# --- Run ---
analyser = Analyser()

analyser.main_folder           = OUTPUT_DIR + "/"
analyser.input_path            = INPUT_DIR + "/"
analyser.information_extracted = INFO_DIR + "/"
analyser.results_path          = RESULTS_DIR + "/"

analyser.biological_replicate  = 0          # 0 = single experiment
analyser.userinput             = 0          # 0 = no manual confirmation step
analyser.information_readout   = "Confluency"
analyser.readout_units         = "(%)"
analyser.expected_effect       = 0          # 0 = inhibition
analyser.synergy_method        = 0          # 0=Bliss  1=HSA  2=ZIP

analyser.files_list = ["drug_combination_screen_1timepoint"]

print("Starting HTSplotter drug combination analysis...")
analyser.execute()
print(f"\nDone! Results saved to:\n  {RESULTS_DIR}")
