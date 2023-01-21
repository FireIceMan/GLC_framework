# Scaling analysis
> A statistical tool to analyze the "scaling property" in protein sequence

## prerequisite
- For protein sequence, please segment its protein and domain in the format: "A1-A2 B1-B2-B3". The space is used to segment proteins, while the `-` is for domain.
- If you don't have suitable algorithm to segment, you can use InterPro which is mention in page 3 of `SI.pdf` (find this in GLC_framework
/SI.pdf)


---------
## Fitting_MLE
A teaching material of maximum likelihood estimation (MLE).

## Run_case_by_case
Apply scaling analysis case by case. View this file for its details.

## Run_All
Apply scaling analysis on the txt files in data/Text

Tutorial for Run_All
------
Before you use Run_All, we suggest you try Run_case_by_case to know the functionalities of each function.

1. Put your segmented txt files in data/Text

2. In main(), there are several settings. You can see Run_case_by_case for their details.
* If you don't want to run certain functions, you can # them. For example, 
```python
  #FRD_plot(...)
```

* Special cases: calculate SP and fitting scaling lines. You need to # three functions.
```python
  #f, flu = Plot_f(...)
  #Rf = rf(...)
  #fit_with_cut(...)
```

3. In jupyter notebook, use Cell > Run all to excute the program.

4. If there is any bug, it will show in the bottom of this program. Please report us if you can not solve the bug.
 
