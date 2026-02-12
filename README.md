# GLC Framework — Genetics-Linguistics Correspondence

[![arXiv](https://img.shields.io/badge/arXiv-2012.14309-b31b1b.svg)](https://arxiv.org/abs/2012.14309)

> A unified framework based on fundamental physical principles for predicting and analyzing the evolution of sequences — including protein sequences and human language. The framework reveals statistical characteristics common to both biological and linguistic systems, such as Zipf's law and power-law degree distributions.

![GLC Hierarchy](./img/Evo_Hierarchy.png)

## Table of Contents

- [Key Idea](#key-idea)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Data Format](#data-format)
- [Usage](#usage)
  - [Evolution Algorithm](#1-evolution-algorithm)
  - [Analysis Tool](#2-analysis-tool)
  - [Fake Generators](#3-fake-generators)
- [Possible Future Updates](#possible-future-updates)
- [Citation](#citation)
- [Contact](#contact)

## Key Idea

Life and language share many common characteristics, making it possible to analyze them using a generalized framework.

The GLC hierarchy defines a universal structure for both biological and linguistic sequences:

| GLC Hierarchy | Life (Genetics) | Language (Linguistics) |
|:---:|:---:|:---:|
| **Element** | Amino acid | Phoneme |
| **Component** | Domain | Syllagram |
| **Block** | Protein | Word |
| **Book** | Sequence of blocks | Sequence of blocks |

**Problem addressed:** The quantitative measurement of natural selection for sequences is an unresolved issue. Furthermore, existing algorithms for generating and forecasting sequences often lack transparency and **interpretability**.

**This project provides:**

1. **Evolution Algorithm** — Generates text or protein sequences by simulating the process of natural selection
2. **Analysis Tools** — Analyzes human text and protein sequences using scaling analysis, network analysis, and distribution fitting
3. **Fake Generators** — Produces artificial text with specified statistical distributions for comparative studies

Technical details can be found in `SI.pdf`.

## Features

- Requires only **4 key parameters** (`lam`, `z`, `P_mu`, `T`) to generate sequences that conform to the statistical properties of human text and protein sequences
- Capable of simulating mutation and forecasting evolutionary changes
- Evolution and variation are based on explainable fundamental principles — **not a black-box** mechanism
- Rank-rank analysis uncovers previously hidden information about life and language

## Project Structure

```
GLC_framework/
│
├── evolution_mechanism.ipynb       # Core evolution algorithm (runnable on Colab)
├── SI.pdf                          # Supplementary information (technical details)
│
├── general/                        # General sequence analysis
│   ├── Module/                     #   Core analysis modules
│   ├── Run_case_by_case.ipynb      #   Analyze a single file
│   └── Run_All.ipynb               #   Batch analysis
│
├── genetics/                       # Protein sequence analysis
│   ├── Module/                     #   Genetics-specific modules
│   ├── seq2txt/                    #   Sequence format conversion
│   ├── Run_case_by_case.ipynb      #   Analyze a single file
│   ├── Run_All.ipynb               #   Batch analysis
│   ├── Network.ipynb               #   Network visualization & analysis
│   └── Fitting_MLE.ipynb           #   MLE fitting tutorial
│
├── linguistics/
│   ├── English/                    # English text analysis
│   │   ├── Module/                 #   English-specific modules
│   │   ├── Run_case_by_case.ipynb  #   Analyze a single file
│   │   ├── Run_All.ipynb           #   Batch analysis
│   │   └── Z_ZM_comparsion.ipynb   #   Zipf vs Zipf-Mandelbrot comparison
│   └── Mandarin Chinese/           # Mandarin Chinese text analysis
│       ├── Module/                 #   Chinese-specific modules
│       ├── Ngram/                  #   N-gram analysis data
│       ├── Run_All.ipynb           #   Batch analysis
│       └── Run_All_Ngram.ipynb     #   N-gram batch analysis
│
├── fake generator/                 # Synthetic data generators
│   ├── Zipf.ipynb                  #   Zipf distribution
│   ├── Gaussian.ipynb              #   Gaussian distribution
│   ├── LogNormal.ipynb             #   Log-normal distribution
│   ├── Exponential.ipynb           #   Exponential distribution
│   ├── DoubleZipf.ipynb            #   Double power-law distribution
│   ├── David_Wang_fake.ipynb       #   N-gram shuffling
│   └── Constraint.ipynb            #   Constrained generation
│
└── img/                            # Figures for documentation
```

## Installation

### Prerequisites

- Python 3
- [Anaconda](https://www.anaconda.com/) (recommended) or pip

### Dependencies

```bash
pip install numpy pandas matplotlib scipy networkx numba
```

| Package | Usage |
|---|---|
| `numpy` | Numerical computation |
| `pandas` | Data manipulation |
| `matplotlib` | Visualization |
| `scipy` | Curve fitting, MLE, optimization |
| `networkx` | Network analysis |
| `numba` | JIT acceleration (evolution algorithm) |

### Running Notebooks

All analysis and generation programs are provided as Jupyter notebooks (`.ipynb`). You can run them with:

```bash
jupyter notebook
```

The evolution algorithm can also be run directly on Google Colab:
[Open in Colab](https://colab.research.google.com/drive/1h8tNyqPPnqfmG9g7BiD-w4jzSz-npnJa#scrollTo=lwZnojnDFM5Y)

## Data Format

Before running the analysis tools, your text must be **segmented** into blocks and components. The format depends on your data type:

### Phonographic language (e.g., English)

Use **spaces** to separate words (blocks) and **hyphens** to separate syllables (components):

```
The hunt-er like ap-ple
```

Recommended segmentation tool: [syllabipy](https://github.com/henchc/syllabipy)

### Logographic language (e.g., Mandarin Chinese)

Use **spaces** to separate words (blocks). Characters within a word are naturally the components:

```
獵人 捕捉 獵物
```

Recommended segmentation tools:
- [CKIP](https://pypi.org/project/ckip-segmenter/) (Sinica)
- [Stanford CTB/PKU parser](http://michelleful.github.io/code-blog/2015/09/10/parsing-chinese-with-stanford/)
- [LingPipe](http://alias-i.com/lingpipe-3.9.3/demos/tutorial/chineseTokens/read-me.html)

### Protein sequences

Use **spaces** to separate proteins (blocks) and **hyphens** to separate domains (components):

```
A1-A2 B1-B2-B3
```

Recommended tool: [InterPro](https://www.ebi.ac.uk/interpro/) for domain identification (see page 3 of `SI.pdf`)

### File requirements

- Encoding: **UTF-8**
- Place your `.txt` files in the corresponding `data/Text/` folder of each discipline

## Usage

### 1. Evolution Algorithm

![Flowchart of the evolution algorithm](./img/flowchart.png)

The evolution algorithm simulates natural selection to generate sequences. It uses the **principle of least effort** to decide between two modes at each step: **(I) co-option** (reuse an existing block) or **(II) de novo** (create a new block).

**Steps:**

1. Configure the parameters:

   | Parameter | Description | Example |
   |---|---|---|
   | `L` | Sequence length (total number of blocks in Book) | 10000 |
   | `N_max` | Maximum number of components per block | 5 |
   | `P_N` | Probability distribution for component count | [0.15, 0.40, 0.25, 0.15, 0.05] |
   | **`lam`** | System parameter lambda (crucial) | 0.47 |
   | **`z`** | Effective connection strength (crucial) | 0.004 * L |
   | **`P_mu`** | Mutation probability (crucial) | 0.0005 |
   | **`T`** | Number of mutation rounds per iteration (crucial) | 1 |

2. Run `evolution_mechanism.ipynb` (locally or on [Google Colab](https://colab.research.google.com/drive/1h8tNyqPPnqfmG9g7BiD-w4jzSz-npnJa#scrollTo=lwZnojnDFM5Y)). It will output a `.txt` file.

3. Move the output `.txt` file to the `general/data/Text/` folder and run `general/Run_case_by_case.ipynb` to analyze the generated sequence.

### 2. Analysis Tool

Each discipline folder (`general/`, `genetics/`, `linguistics/English/`, `linguistics/Mandarin Chinese/`) provides two modes:

| Notebook | Purpose | How to use |
|---|---|---|
| `Run_case_by_case.ipynb` | Analyze a **single** text file | Place the `.txt` file in the same directory as the notebook |
| `Run_All.ipynb` | **Batch** analyze multiple files | Place all `.txt` files in `./data/Text/` |

**Recommended:** Start with `Run_case_by_case.ipynb` to understand each function before running batch analysis.

The analysis pipeline produces:

- **Frequency-Rank Distribution (FRD)** — Zipf's law fitting via MLE (Zipf vs Zipf-Mandelbrot, selected by AICc)
- **Rank-Rank Distribution (RRD)** — Block-component rank relationships
- **Scaling Analysis** — Hierarchical scaling structure with de-noising, SC-value
- **Network Analysis** — Degree distribution and clustering coefficients
- **Allocation & Chain Analysis** — Distribution fitting for block-component relationships

### 3. Fake Generators

Generate synthetic corpora with controlled statistical properties for comparison with real data. See page 4 of `SI.pdf` for details.

| Generator | Distribution |
|---|---|
| `Zipf.ipynb` | Zipf (power-law) |
| `Gaussian.ipynb` | Gaussian (normal) |
| `LogNormal.ipynb` | Log-normal |
| `Exponential.ipynb` | Exponential |
| `DoubleZipf.ipynb` | Double power-law |
| `David_Wang_fake.ipynb` | N-gram shuffling |
| `Constraint.ipynb` | Constrained generation (with upper bound on link) |

## Possible Future Updates

**Evolution algorithm:**
- Allow user-defined function connection networks (current version: random FC)

**Analysis tool:**
- Develop segmentation algorithms for unknown languages or non-coding DNA
- Automatically determine corresponding evolution parameters when analyzing real-world data

## Citation

If you use this framework in your research, please cite:

```bibtex
@article{GLC2020,
  title={Genetics-Linguistics Correspondence framework},
  author={FireIceMan},
  journal={arXiv preprint arXiv:2012.14309},
  year={2020},
  url={https://arxiv.org/abs/2012.14309}
}
```

## Contact

Created by [@FireIceMan](https://github.com/FireIceMan) — feel free to contact me!
