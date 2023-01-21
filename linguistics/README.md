# scaling analysis
> Tools to analyze the statistical features for lanuages

## Tutor
### Prerequisit
prepare several segmented corpora (for the same novel, book, ...etc) with different algorithms
Encoding: utf-8

- For human text, please segment its words and syllagrams. 
  
  (1) For phonogram, e.g. English, use the format: "The hunt-er like ap-ple". The space is used to segment words, while the `-` is for syllagrams.
  
  (2) For logogram, such as Chinese, use the format: "獵人 捕捉 獵物". The space is used to segment words, while no symbol is needed to syllabify them.

- If your text is not segmented, here are some suggest algorithms:

1. Chinese:
* CKIP, Sinica. https://pypi.org/project/ckip-segmenter/
* Stanford ctb & pku. http://michelleful.github.io/code-blog/2015/09/10/parsing-chinese-with-stanford/
* LingPipe. http://alias-i.com/lingpipe-3.9.3/demos/tutorial/chineseTokens/read-me.html

2. English:
* https://github.com/henchc/syllabipy

### There are two version program: `Case_by_case.ipynb` and `Run_All.ipynb`

The former is used to run case by case and see details of program, the beginner is suggested to use this program.

### Take Chinese for example:

1. To complete the A-GLMV plot, you need excel table in the form of "**readme of Run_case_by_case.png**"

2. Put your segmented corpora in "Chinese/data/Text"

3. Run "Chinese/Run_All.ipynb"

4. Now you have all the information that can used to fill the excel table
* M, V1, L can get from "Chinese/data/Statistical result"
* SP can get form "Chinese/data/SP"
* G can get form "Chinese/data/fitting"

5. The "Accuracy" need to run "Chinese/Accuracy.ipynb"
* Chose one of your segmented corpora as standard corpora (used to judge other algorithm, i.e., assume it is 100% correct)
* Put the file in "Chinese/data/Statistical result" into "Chinese/Accuracy" folder and rename your standard corpora file as "standard"
* Run "Chinese/Accuracy.ipynb", and you get the Accuracy data for your excel table

6. After your excel table, you can run "A-GLMV plot/Run_case_by_case.ipynb"

7. Now you get the A-GLMV plot !
