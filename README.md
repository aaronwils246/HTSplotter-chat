# HTSplotter + AI Chat Interface

Run [HTSplotter](https://github.com/CBIGR/HTSplotter) drug screen analyses and ask plain-English questions about your results using Claude AI.

## What's included

| Script | Description |
|---|---|
| `run_drugscreen.py` | Run a single-drug dose-response analysis |
| `run_drugcombination.py` | Run a drug combination synergy analysis |
| `chat_results.py` | Chat with Claude about your results |

## Setup

**1. Create a virtual environment and install dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Get the HTSplotter example data (optional)**
```bash
git clone https://github.com/CBIGR/HTSplotter repo
```

## Running an analysis

```bash
source venv/bin/activate

# Single drug dose-response
python run_drugscreen.py

# Drug combination + synergy scoring
python run_drugcombination.py
```

Results are saved to `my_results/`.

## Chatting about your results

Get an API key at [console.anthropic.com](https://console.anthropic.com), then:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python chat_results.py
```

By default it reads the drug screen results. To point it at any other results folder:

```bash
python chat_results.py path/to/output_results/
```

**Example questions:**
- *Which drug was most potent?*
- *What does the IC50 for Prexasertib tell me?*
- *Is there synergy between MK-1775 and BAY1895344?*
- *What do the nan values in the IC table mean?*

## Synergy methods

Edit `run_drugcombination.py` and set `synergy_method` to:
- `0` — Bliss independence (default)
- `1` — HSA
- `2` — ZIP

## Credits

HTSplotter was created by **Carolina de Carvalho Nunes** and collaborators at the
[Center for Biomarkers in Gastroenterology and Inflammatory Diseases (CBIGR)](https://github.com/CBIGR),
Ghent University.

- GitHub: https://github.com/CBIGR/HTSplotter
- Web tool: https://htsplotter.cmgg.be/
- License: [GPL v3](https://github.com/CBIGR/HTSplotter/blob/main/LICENSE.txt)

This repository adds an AI chat interface on top of HTSplotter using the
[Anthropic Claude API](https://console.anthropic.com). It does not modify the
HTSplotter source code. Please cite the original HTSplotter paper if you use
this tool in your research:

> Nunes C, Anckaert J, De Vloed F, De Wyn J, Durinck K, Vandesompele J, Speleman F, Vermeirssen V.
> **HTSplotter: An end-to-end data processing, analysis and visualisation tool for chemical and genetic in vitro perturbation screening.**
> *PLoS One.* 2024 Jan 5;19(1):e0296322.
> DOI: [10.1371/journal.pone.0296322](https://doi.org/10.1371/journal.pone.0296322) | PMID: 38181013
