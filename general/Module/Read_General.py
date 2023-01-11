import numpy as np
import textwrap


def read_file(filename, encode = 'UTF-8'):
    """
    Read the text file with the given filename;
    return a list of the blocks of text in the file; ignore punctuations.
    also returns the longest block length in the file.
    
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
    1. block_list: array
        a list of blocks in the txt file
        
    2. longest: int
        max number of components in a block
        
    """
    punctuation_set = set(u'''_—＄％＃＆:#$&!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
    ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
    々‖•·ˇˉ－―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
    ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
    longest = 0
    block_list = []
    with open(filename, "r", encoding = encode) as file:
        for line in file:
            l = line.split()
            for block in l:
                new_block = ''
                for c in block:
                    if c not in punctuation_set:
                        new_block = new_block + c
                if not len(new_block) == 0: 
                    block_list.append(block)
                    if len(block.split('-')) > longest:
                        longest = len(block.split('-')) #max number of components in a block
                    
    if '\ufeff' in block_list:
        block_list.remove('\ufeff')
        
    print("read file successfully!")
    return block_list, longest

def read_Ngram_file(filename, N, encode = 'UTF-8'):
    """
    Read the text file with the given filename;    
    return a list of the blocks of text in the file; ignore punctuations.
    also returns the longest block length in the file.
    
    ---Parameters
    1. file_name : string
      XXX.txt. We suggest you using the form that set 
      name = 'XXX' 
      and 
      filename = name + '.txt'.
        
    2. N: int
      "N"-gram. 
      For example : a string, ABCDEFG (In Chinese, you don't know what's the 'blocks' of a string)
      in 2-gram = [AB, CD, EF, G];
      in 3-gram = [ABC, DEF, G];
      in 4-gram = [ABCD, EFG]
      
      two blocks are in a txt 'ABCDE EFGHI' (This case happended in English corpus)
      in 2-gram = [AB, CD, E, EF, GH, I];
      in 3-gram = [ABC, DE, EFG, HI];
      in 4-gram = [ABCD, E, EFGH, I]
    
    3. encode : encoding of your txt
    
    ---Return
    1. block_list: array
        a list of blocks in the txt file
        
    2. N: int
        N-gram
    """
    punctuation_set = set(u'''_—＄％＃＆:#$&!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
    ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
    々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
    ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')

    block_list = []
    with open(filename, "r", encoding = encode) as file:
        for line in file:
            l = line.split()
            for block in l:
                new_block = ''
                for c in block:
                    if c not in punctuation_set:
                        new_block = new_block + c
                    if c in punctuation_set and len(new_block) != 0:
                        block_list.append(new_block)
                        new_block = ''
                if not len(new_block) == 0: 
                    block_list.append(new_block)
                    new_block = ''
                    
    if '\ufeff' in block_list:
        block_list.remove('\ufeff')
    
    block_list = []
    for block in block_list:
        components = textwrap.wrap(block, N)
        New_block = ''
        for s in components:
            New_block = New_block + '-' + s
            block_list.append(New_block)
    
    print("read file successfully!")
    return block_list, N

def produce_blockRank_compoRank_frame(pd_block, pd_compo, longest):
    '''merge pd_block and pd_compo into a large dataframe
    
    ---Input
    1. pd_block: pandas.DataFrame
        return of produce_data_frame(unit = block)
    
    2. pd_compo: pandas.DataFrame
        return of produce_data_frame(unit = component)
    
    3. longest: int
        return of read_file
        
    ---Return
        pd_block: pandas.DataFrame
            a large dataframe contains information of blocks and its components
            Ex: for 'ap-ple'
                1th_compo = ap
                2th_compo = ple
    
    '''
    
    
    D = {}
    
    compo_array = pd_compo["compo"]
    compo_rank = {}
    
    for i in range(len(pd_compo)):
        compo_rank[compo_array[i]] = i + 1 
    
    for i in range(longest):
        D[i] = []
    
    block_array = pd_block["block"]
    N_component = [] #count how many component in a block
    
    for block in block_array:
        t = block.split('-') #t is number of component
        N_component.append(len(t))
        
        for i in range(len(t)):
            D[i].append(int(compo_rank[t[i]]))
        
        if len(t) < longest:
            for j in range(len(t),longest):
                D[j].append(np.nan)
    
    pd_block["N_compo"] = np.array(N_component)
    
    for k in range(longest):
        feature = str(k) + "th" + "_compo_rank"
        pd_block[feature] = np.array(D[k])
    
    return pd_block

'''
def transfrom_blocklist_into_Ngram_compolist(block_list, N):
    """Divide each blocks in the block_list into N-gram components, order reserved.
    
    -------Input: 
    1. block_list:
      a list containing blocks
    
    2. N: int
      "N"-gram. 
      For example : a string, ABCDEFG (In Chinese, you don't know what's the 'blocks' of a string)
      in 2-gram = [AB, CD, EF, G];
      in 3-gram = [ABC, DEF, G];
      in 4-gram = [ABCD, EFG]
      
      two blocks are in a txt 'ABCDE EFGHI' (This case happended in English corpus)
      in 2-gram = [AB, CD, E, EF, GH, I];
      in 3-gram = [ABC, DE, EFG, HI];
      in 4-gram = [ABCD, E, EFGH, I]
    
    -------Return:
        a list containg compo 
    """
    compo_list = []
    for block in block_list:
        components = textwrap.wrap(block, N)
        compo_list.extend(components)
        
    return compo_list
'''


def count_allo(pdframe1, pdframe2, feature1 = "block", feature2 = "compo", feature3 = "compoFreq"):
    '''count the allocations of components and the chains of blocks
    
    ---Input
        pdframe1, pdframe2 : class pandas.DataFrame.
            This two args are from module > count.py > info(file_name, encode = "UTF-8")
            They would be block and compo (See Run_case_by_case.ipynb)
    
    ---Output
    1. add a frame "#allocations" (numbers of allocations of compos) in pdframe2
    
    2. add a frame "#chains" (numbers of chains of blocks) in pdframe1
    '''
    
    block_array = pdframe1[feature1] #ex: block_array=['apple','coffee','elephant']
    compo_array = pdframe2[feature2] #ex: compo_array=['ap', 'ple', 'cof', 'fee', 'e', 'le', 'phant']
    
    #First, we calculate allocations
    
    allocation = {}
    for c in compo_array: 
        allocation[c] = 0
        for w in block_array:
            t = w.split('-')
            if c in set(t): #ex: 'A' in 'AB', but 'A' not in 'BC'
                allocation[c] += 1

    compo_num_allocations_array = np.array([], dtype = 'int16' )
    
    for i in range(len(pdframe2)):
        compo_num_allocations_array = np.append(compo_num_allocations_array, allocation[compo_array[i]])
    
    #add a frame "#allocations" (numbers of allocations of compos) to compo
    pdframe2['#allocations'] = compo_num_allocations_array 
        
    #Second, we use allocation to calculate chains
    
    
    chain = {}
    for w in block_array:
        chain[w] = 0
        t = w.split('-')
        for c in set(t):
            #If we don't use set(w) here, the chains will be overcount. 
            #ex: chain('AA') = allocation('A') but not 2*allocation('A')
            chain[w] += allocation[c]
    
    chain_num_array = np.array([], dtype = 'int16')
    
    for i in range(len(pdframe1)):
        chain_num_array = np.append(chain_num_array , chain[block_array[i]])
    
    #add a frame "#chains" (numbers of chains of blocks) to block
    pdframe1['#chains'] = chain_num_array