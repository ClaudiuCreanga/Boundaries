#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 17:30:42 2017

Computes quasi-bootstrapped distance matrices according to the Jaccard distance ('--' '+0' '-0' '00' ignored)
Assumes alphabet to be +,-,0

@authors: Andrea Ceolin and Luca Bortolussi
"""


import random
import sys


"""
Loads the language table, see the example file for the format. 
Each parameter of each language must be separated from other parameters by a space. 
"""
def loadTable(filename):
    lang_dict = {}
    with open(filename) as f:
        for line in f:
            #splits the line into tokens. Tokens are separated by space
            tokens = line.split()
            #the first token is the language name
            lang = tokens[1:].copy()
            #temporary store into a dictionary
            lang_dict[tokens[0]]=lang
    #returns a list of language names and a table with parameters 
    lang_names = list(lang_dict.keys())    
    lang_table = [ lang_dict[key] for key in lang_dict.keys()]
    return lang_names,lang_table

"""
Computes the distance between two languages
"""           
def compute_distance(lang1,lang2):
    identities = 0
    differences = 0
    #counts identities and differences between the two languages. 
    for (c1,c2) in zip(lang1,lang2):
        if c1=='+' and c2 == '+':
            #ids only for 11
            identities += 1
        elif (c1=='+' and c2 == '-') or (c1=='-' and c2 == '+'):
            #differences only for 10 or 01
            differences += 1
    d = differences / (identities + differences)
    return d

def hamming(P1, P2):
    """Computes the Hamming distance between two strings.

    Args:
        P1: The first string.
        P2: The second string.

    Returns:
        The Hamming distance between the two strings.
    """

    # Check if the strings are the same length
    if len(P1) != len(P2):
        raise ValueError("Strings must be the same length. Hamming extension must be implemented for different string lengths.")

    # Initialize a counter for the number of mismatches
    num_mismatches = 0
    length = 0

    # Iterate over the strings and count the number of mismatches
    # this excludes the 0 items and their index in the other string
    for char1, char2 in zip(P1, P2):
        if char1 != '0' and char2 != '0':
            length += 1
            if char1 != char2:
                num_mismatches += 1

    normalized_hamming_distance = num_mismatches / length

    return normalized_hamming_distance

    
"""
Computes the distance matrix
"""   
def compute_distance_matrix(lang_table):
    n = len(lang_table) #number of languages
    D = [ [0 for i in range(n) ] for j in range(n) ] #init zero distance matrix
    for i in range(n-1):
        for j in range(i+1,n):
            #computes pairwise distances
            D[i][j] = D[j][i] = hamming(lang_table[i],lang_table[j])
    return D    

"""
Print the distance matrix into the correct output format, as in the previous code
"""    
def print_distance_matrix(lang_names,dist_matrix):
    string = '' + str(len(lang_names)) + '\n'
    for (name,dist_row) in zip(lang_names,dist_matrix):
        string += name + '       '
        for d in dist_row:
            string += '{0:10.3f}'.format(d)
        string += '\n' 
    string += '\n\n'    
    return string

"""
Creates a jacknifes version of the language table
"""

def generate_bootstrap(lang_table):
    n = len(lang_table) #n. of langs
    c = len(lang_table[0]) #n. of pars
    #this is the table
    new_table = [[value for value in par] for par in lang_table]
    #this is the old table
    copied_table = [[value for value in par] for par in lang_table]
    #Here we select the columns to replace, and their replacement
    set1 = random.sample(range(c), 6)  # column to replace
    set2 = random.sample(range(c), 6)  # column to repeat
    n1,n2,n3,n4,n5,n6 = set1
    m1,m2,m3,m4,m5,m6 = set2
    for i in range(n):
        new_table[i][n1] = copied_table[i][m1]
        new_table[i][n2] = copied_table[i][m2]
        new_table[i][n3] = copied_table[i][m3]
        new_table[i][n4] = copied_table[i][m4]
        new_table[i][n5] = copied_table[i][m5]
        new_table[i][n6] = copied_table[i][m6]
    return new_table


"""
Main function, loads the table
"""
def main(argv):
    n_samples = int(argv[0])
    input_file = argv[1]
    output_file = argv[2]
    lang_names,lang_table = loadTable(input_file)
    with open(output_file,'w') as f:
        for b in range(n_samples):
            new_table = generate_bootstrap(lang_table)
            D = compute_distance_matrix(new_table)
            f.write(print_distance_matrix(lang_names,D))

if  __name__ =='__main__':
    main(sys.argv[1:])    
      
