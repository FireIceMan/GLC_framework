# GLC (Genetics-Linguistics Correspondence)
>Based on fundamental physical principle, this research builds a framework to predict the evolution of sequence, such as protein sequence and human text, generating sequence, and examining the statistical hallmarks of life and language, e.g., Zipf's law and power-law degree distribution.

![framework](./img/Evo_Hierarchy.png)

## Table of Contents
* [General Info](#general-information)
* [Features](#features)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)

## General Information
- Main spirt - Life and language shared many similar hallmarks, thus they can be analyzed via a general framework.
- Main Problem - The natural selection of sequence has not been quantified. In the other hands, the generating algorithm and prediction of sequence usually lack the $\text{\textcolor{red}{interpretability}}$. 
- This project provides 

(1) An evolutionary algorithm that can generate text/protein sequence; 

(2) Tools that can be used to analyze text/protein sequence

## Features
List the ready features here:
- Only need $\text{\textcolor{red}{4 parameters}}$ to generate a sequence that satisfies the statistical properties of human text and protein sequence.
- Simulate mutation and predict the direction of evolution.
- The evolution and variation is based on fundamental principle that can be explained, not a $\text{\textcolor{red}{black-box}}$.
- Reveal the hidden information of life and language by rank-rank analysis.

## Setup
### For algorithm of evolution and generating sequence
You can use the demo on google colab [_here_](https://colab.research.google.com/drive/1h8tNyqPPnqfmG9g7BiD-w4jzSz-npnJa#scrollTo=lwZnojnDFM5Y)
or download the `evolution_mechanism.ipynb` to run on your computer.

### For analysis of language, protein sequence, and general sequence
1. Choose the discipline:
  - For language, please go to the folder `linguistics`.
  - For protein sequence, please go to the folder `genetics`.
  - For general sequence, please go to the folder `general`.
2. Segment a sequence with its blocks and components. For details, please go to the corresponding folder.
   If you don't have any segmentation algorithm, please go to the corresponding folder and read the recommend softwares.
3. Use `Run_case_by_case.ipynb` or `Run_All.ipynb` to analyze your segmented sequence.
  - If you only want to analyze one text, use `Run_case_by_case.ipynb` while put the text in the same folder with `Run_case_by_case.ipynb`.
  - If you want to analyze many texts, use `Run_All.ipynb` while put the text in the folder `./data/Text`.

## Usage
How does one go about using it?
Provide various use cases and code examples here.

`write-your-code-here`
![framework](./img/flowchart.png)



## Project Status
Project is: _in progress_ / _complete_ / _no longer being worked on_. If you are no longer working on it, provide reasons why.


## Room for Improvement
Include areas you believe need improvement / could be improved. Also add TODOs for future development.

Room for improvement:
- Improvement to be done 1
- Improvement to be done 2

To do:
- Feature to be added 1
- Feature to be added 2


## Acknowledgements
Give credit here.
- This project was inspired by...
- This project was based on [this tutorial](https://www.example.com).
- Many thanks to...


## Contact
Created by [@FireIceMan](https://www.flynerd.pl/) - feel free to contact me!
