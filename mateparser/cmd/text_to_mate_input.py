#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 16:06:19 2018

@author: Samuele Garda
"""

import sys
import codecs
#from gensim.utils import to_utf8
from nltk.tokenize import sent_tokenize,word_tokenize


if __name__ == "__main__":

  infile = codecs.open(sys.argv[1], encoding='utf-8').read()
  sents = sent_tokenize(infile)
  
  with codecs.open(sys.argv[2], 'w+') as outfile:
    for sent in sents:
      words = word_tokenize(sent)
      
      words = ' '.join(words).encode('utf-8')
      
      
      outfile.write("{}\n".format(words))