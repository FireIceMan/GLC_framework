import numpy as np
import textwrap


def read_file(filename, encode = 'UTF-8'):
    """
    Read the text file with the given filename;
    return a list of the proteins of text in the file; ignore punctuations.
    also returns the longest protein length in the file.
    
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
    1. protein_list: array
        a list of proteins in the txt file
        
    2. longest: int
        max number of domains in a protein
        
    """
    punctuation_set = set(u'''_—＄％＃＆:#$&!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
    ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
    々‖•·ˇˉ－―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
    ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
    longest = 0
    protein_list = []
    with open(filename, "r", encoding = encode) as file:
        for line in file:
            l = line.split()
            for protein in l:
                new_protein = ''
                for c in protein:
                    if c not in punctuation_set:
                        new_protein = new_protein + c
                if not len(new_protein) == 0: 
                    protein_list.append(protein)
                    if len(protein.split('-')) > longest:
                        longest = len(protein.split('-')) #max number of domains in a protein
                    
    if '\ufeff' in protein_list:
        protein_list.remove('\ufeff')
        
    print("read file successfully!")
    return protein_list, longest

def read_Ngram_file(filename, N, encode = 'UTF-8'):
    """
    Read the text file with the given filename;    
    return a list of the proteins of text in the file; ignore punctuations.
    also returns the longest protein length in the file.
    
    ---Parameters
    1. file_name : string
      XXX.txt. We suggest you using the form that set 
      name = 'XXX' 
      and 
      filename = name + '.txt'.
        
    2. N: int
      "N"-gram. 
      For example : a string, ABCDEFG (In Chinese, you don't know what's the 'proteins' of a string)
      in 2-gram = [AB, CD, EF, G];
      in 3-gram = [ABC, DEF, G];
      in 4-gram = [ABCD, EFG]
      
      two proteins are in a txt 'ABCDE EFGHI' (This case happended in English corpus)
      in 2-gram = [AB, CD, E, EF, GH, I];
      in 3-gram = [ABC, DE, EFG, HI];
      in 4-gram = [ABCD, E, EFGH, I]
    
    3. encode : encoding of your txt
    
    ---Return
    1. protein_list: array
        a list of proteins in the txt file
        
    2. N: int
        N-gram
    """
    punctuation_set = set(u'''_—＄％＃＆:#$&!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
    ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
    々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
    ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')

    protein_list = []
    with open(filename, "r", encoding = encode) as file:
        for line in file:
            l = line.split()
            for protein in l:
                new_protein = ''
                for c in protein:
                    if c not in punctuation_set:
                        new_protein = new_protein + c
                    if c in punctuation_set and len(new_protein) != 0:
                        protein_list.append(new_protein)
                        new_protein = ''
                if not len(new_protein) == 0: 
                    protein_list.append(new_protein)
                    new_protein = ''
                    
    if '\ufeff' in protein_list:
        protein_list.remove('\ufeff')
    
    protein_list = []
    for protein in protein_list:
        domains = textwrap.wrap(protein, N)
        New_protein = ''
        for s in domains:
            New_protein = New_protein + '-' + s
            protein_list.append(New_protein)
    
    print("read file successfully!")
    return protein_list, N

def produce_proteinRank_domRank_frame(pd_protein, pd_dom, longest):
    '''merge pd_protein and pd_dom into a large dataframe
    
    ---Input
    1. pd_protein: pandas.DataFrame
        return of produce_data_frame(unit = protein)
    
    2. pd_dom: pandas.DataFrame
        return of produce_data_frame(unit = domain)
    
    3. longest: int
        return of read_file
        
    ---Return
        pd_protein: pandas.DataFrame
            a large dataframe contains information of proteins and its domains
            Ex: for 'ap-ple'
                1th_dom = ap
                2th_dom = ple
    
    '''
    
    
    D = {}
    
    dom_array = pd_dom["dom"]
    dom_rank = {}
    
    for i in range(len(pd_dom)):
        dom_rank[dom_array[i]] = i + 1 
    
    for i in range(longest):
        D[i] = []
    
    protein_array = pd_protein["protein"]
    N_domain = [] #count how many domain in a protein
    
    for protein in protein_array:
        t = protein.split('-') #t is number of domain
        N_domain.append(len(t))
        
        for i in range(len(t)):
            D[i].append(int(dom_rank[t[i]]))
        
        if len(t) < longest:
            for j in range(len(t),longest):
                D[j].append(np.nan)
    
    pd_protein["N_dom"] = np.array(N_domain)
    
    for k in range(longest):
        feature = str(k) + "th" + "_dom_rank"
        pd_protein[feature] = np.array(D[k])
    
    return pd_protein

'''
def transfrom_proteinlist_into_Ngram_domlist(protein_list, N):
    """Divide each proteins in the protein_list into N-gram domains, order reserved.
    
    -------Input: 
    1. protein_list:
      a list containing proteins
    
    2. N: int
      "N"-gram. 
      For example : a string, ABCDEFG (In Chinese, you don't know what's the 'proteins' of a string)
      in 2-gram = [AB, CD, EF, G];
      in 3-gram = [ABC, DEF, G];
      in 4-gram = [ABCD, EFG]
      
      two proteins are in a txt 'ABCDE EFGHI' (This case happended in English corpus)
      in 2-gram = [AB, CD, E, EF, GH, I];
      in 3-gram = [ABC, DE, EFG, HI];
      in 4-gram = [ABCD, E, EFGH, I]
    
    -------Return:
        a list containg dom 
    """
    dom_list = []
    for protein in protein_list:
        domains = textwrap.wrap(protein, N)
        dom_list.extend(domains)
        
    return dom_list
'''


def count_allo(pdframe1, pdframe2, feature1 = "protein", feature2 = "dom", feature3 = "domFreq"):
    '''count the allocations of domains and the chains of proteins
    
    ---Input
        pdframe1, pdframe2 : class pandas.DataFrame.
            This two args are from module > count.py > info(file_name, encode = "UTF-8")
            They would be protein and dom (See Run_case_by_case.ipynb)
    
    ---Output
    1. add a frame "#allocations" (numbers of allocations of doms) in pdframe2
    
    2. add a frame "#chains" (numbers of chains of proteins) in pdframe1
    '''
    
    protein_array = pdframe1[feature1] #ex: protein_array=['apple','coffee','elephant']
    dom_array = pdframe2[feature2] #ex: dom_array=['ap', 'ple', 'cof', 'fee', 'e', 'le', 'phant']
    
    #First, we calculate allocations
    
    allocation = {}
    for c in dom_array: 
        allocation[c] = 0
        for w in protein_array:
            t = w.split('-')
            if c in set(t): #ex: 'A' in 'AB', but 'A' not in 'BC'
                allocation[c] += 1

    dom_num_allocations_array = np.array([], dtype = 'int16' )
    
    for i in range(len(pdframe2)):
        dom_num_allocations_array = np.append(dom_num_allocations_array, allocation[dom_array[i]])
    
    #add a frame "#allocations" (numbers of allocations of doms) to dom
    pdframe2['#allocations'] = dom_num_allocations_array 
        
    #Second, we use allocation to calculate chains
    
    
    chain = {}
    for w in protein_array:
        chain[w] = 0
        t = w.split('-')
        for c in set(t):
            #If we don't use set(w) here, the chains will be overcount. 
            #ex: chain('AA') = allocation('A') but not 2*allocation('A')
            chain[w] += allocation[c]
    
    chain_num_array = np.array([], dtype = 'int16')
    
    for i in range(len(pdframe1)):
        chain_num_array = np.append(chain_num_array , chain[protein_array[i]])
    
    #add a frame "#chains" (numbers of chains of proteins) to protein
    pdframe1['#chains'] = chain_num_array