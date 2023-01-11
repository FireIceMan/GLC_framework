import numpy as np
import textwrap


def read_file(filename, encode = 'UTF-8'):
    """
    Read the text file with the given filename;
    return a list of the words of text in the file; ignore punctuations.
    also returns the longest word length in the file.
    
    ---Input
        a txt file with 'encode' encoding
    
    ---Parameters
    1. file_name : string
          XXX.txt. We suggest you using the form that set 
          name = 'XXX' 
          and 
          filename = name + '.txt'.

    2. encode : encoding of your txt
    
    ---Return
    1. word_list: array
        a list of words in the txt file
        
    2. longest: int
        max number of syllagrams in a word
        
    """
    punctuation_set = set(u'''_—＄％＃＆:#$&!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
    ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
    々‖•·ˇˉ－―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
    ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
    longest = 0
    word_list = []
    with open(filename, "r", encoding = encode) as file:
        for line in file:
            l = line.split()
            for word in l:
                new_word = ''
                for c in word:
                    if c not in punctuation_set:
                        new_word = new_word + c
                if not len(new_word) == 0: 
                    word_list.append(word)
                    if len(word.split('-')) > longest:
                        longest = len(word.split('-')) #max number of syllagrams in a word
                    
    if '\ufeff' in word_list:
        word_list.remove('\ufeff')
        
    print("read file successfully!")
    return word_list, longest

def read_Ngram_file(filename, N, encode = 'UTF-8'):
    """
    Read the text file with the given filename;    
    return a list of the words of text in the file; ignore punctuations.
    also returns the longest word length in the file.
    
    ---Parameters
    1. file_name : string
      XXX.txt. We suggest you using the form that set 
      name = 'XXX' 
      and 
      filename = name + '.txt'.
        
    2. N: int
      "N"-gram. 
      For example : a string, ABCDEFG (In Chinese, you don't know what's the 'words' of a string)
      in 2-gram = [AB, CD, EF, G];
      in 3-gram = [ABC, DEF, G];
      in 4-gram = [ABCD, EFG]
      
      two words are in a txt 'ABCDE EFGHI' (This case happended in English corpus)
      in 2-gram = [AB, CD, E, EF, GH, I];
      in 3-gram = [ABC, DE, EFG, HI];
      in 4-gram = [ABCD, E, EFGH, I]
    
    3. encode : encoding of your txt
    
    ---Return
    1. word_list: array
        a list of words in the txt file
        
    2. N: int
        N-gram
    """
    punctuation_set = set(u'''_—＄％＃＆:#$&!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
    ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
    々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
    ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')

    word_list = []
    with open(filename, "r", encoding = encode) as file:
        for line in file:
            l = line.split()
            for word in l:
                new_word = ''
                for c in word:
                    if c not in punctuation_set:
                        new_word = new_word + c
                    if c in punctuation_set and len(new_word) != 0:
                        word_list.append(new_word)
                        new_word = ''
                if not len(new_word) == 0: 
                    word_list.append(new_word)
                    new_word = ''
                    
    if '\ufeff' in word_list:
        word_list.remove('\ufeff')
    
    word_list = []
    for word in word_list:
        syllagrams = textwrap.wrap(word, N)
        New_word = ''
        for s in syllagrams:
            New_word = New_word + '-' + s
            word_list.append(New_word)
    
    print("read file successfully!")
    return word_list, N

def produce_wordRank_sylRank_frame(pd_word, pd_syl, longest):
    '''merge pd_word and pd_syl into a large dataframe
    
    ---Input
    1. pd_word: pandas.DataFrame
        return of produce_data_frame(unit = word)
    
    2. pd_syl: pandas.DataFrame
        return of produce_data_frame(unit = syllagram)
    
    3. longest: int
        return of read_file
        
    ---Return
        pd_word: pandas.DataFrame
            a large dataframe contains information of words and its syllagrams
            Ex: for 'ap-ple'
                1th_syl = ap
                2th_syl = ple
    
    '''
    
    
    D = {}
    
    syl_array = pd_syl["syl"]
    syl_rank = {}
    
    for i in range(len(pd_syl)):
        syl_rank[syl_array[i]] = i + 1 
    
    for i in range(longest):
        D[i] = []
    
    word_array = pd_word["word"]
    N_syllagram = [] #count how many syllagram in a word
    
    for word in word_array:
        t = word.split('-') #t is number of syllagram
        N_syllagram.append(len(t))
        
        for i in range(len(t)):
            D[i].append(int(syl_rank[t[i]]))
        
        if len(t) < longest:
            for j in range(len(t),longest):
                D[j].append(np.nan)
    
    pd_word["N_syl"] = np.array(N_syllagram)
    
    for k in range(longest):
        feature = str(k) + "th" + "_syl_rank"
        pd_word[feature] = np.array(D[k])
    
    return pd_word

'''
def transfrom_wordlist_into_Ngram_syllist(word_list, N):
    """Divide each words in the word_list into N-gram syllagrams, order reserved.
    
    -------Input: 
    1. word_list:
      a list containing words
    
    2. N: int
      "N"-gram. 
      For example : a string, ABCDEFG (In Chinese, you don't know what's the 'words' of a string)
      in 2-gram = [AB, CD, EF, G];
      in 3-gram = [ABC, DEF, G];
      in 4-gram = [ABCD, EFG]
      
      two words are in a txt 'ABCDE EFGHI' (This case happended in English corpus)
      in 2-gram = [AB, CD, E, EF, GH, I];
      in 3-gram = [ABC, DE, EFG, HI];
      in 4-gram = [ABCD, E, EFGH, I]
    
    -------Return:
        a list containg syl 
    """
    syl_list = []
    for word in word_list:
        syllagrams = textwrap.wrap(word, N)
        syl_list.extend(syllagrams)
        
    return syl_list
'''


def count_allo(pdframe1, pdframe2, feature1 = "word", feature2 = "syl", feature3 = "sylFreq"):
    '''count the allocations of syllagrams and the chains of words
    
    ---Input
        pdframe1, pdframe2 : class pandas.DataFrame.
            This two args are from module > count.py > info(file_name, encode = "UTF-8")
            They would be word and syl (See Run_case_by_case.ipynb)
    
    ---Output
    1. add a frame "#allocations" (numbers of allocations of syls) in pdframe2
    
    2. add a frame "#chains" (numbers of chains of words) in pdframe1
    '''
    
    word_array = pdframe1[feature1] #ex: word_array=['apple','coffee','elephant']
    syl_array = pdframe2[feature2] #ex: syl_array=['ap', 'ple', 'cof', 'fee', 'e', 'le', 'phant']
    
    #First, we calculate allocations
    
    allocation = {}
    for c in syl_array: 
        allocation[c] = 0
        for w in word_array:
            t = w.split('-')
            if c in set(t): #ex: 'A' in 'AB', but 'A' not in 'BC'
                allocation[c] += 1

    syl_num_allocations_array = np.array([], dtype = 'int16' )
    
    for i in range(len(pdframe2)):
        syl_num_allocations_array = np.append(syl_num_allocations_array, allocation[syl_array[i]])
    
    #add a frame "#allocations" (numbers of allocations of syls) to syl
    pdframe2['#allocations'] = syl_num_allocations_array 
        
    #Second, we use allocation to calculate chains
    
    
    chain = {}
    for w in word_array:
        chain[w] = 0
        t = w.split('-')
        for c in set(t):
            #If we don't use set(w) here, the chains will be overcount. 
            #ex: chain('AA') = allocation('A') but not 2*allocation('A')
            chain[w] += allocation[c]
    
    chain_num_array = np.array([], dtype = 'int16')
    
    for i in range(len(pdframe1)):
        chain_num_array = np.append(chain_num_array , chain[word_array[i]])
    
    #add a frame "#chains" (numbers of chains of words) to word
    pdframe1['#chains'] = chain_num_array