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

1. Put your segmented corpora in "Chinese/data/Text"

2. Run "Chinese/Run_All.ipynb"

3. Now you have all the information
