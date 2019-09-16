#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 16:31:04 2018

@author: Samuele Garda
"""

from __future__ import division
import logging
import argparse
import glob
from xml.etree import ElementTree
from nltk.tokenize import sent_tokenize


logger = logging.getLogger(__name__)
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(module)s: %(message)s', level = 'INFO')

def parse_args():
  
  parser =  argparse.ArgumentParser(description='Simple stats of plain sentence tokenizer for ADU')
  parser.add_argument('-d','--dir', required=True, help='Folder containing pre-segmented texts in XML format')
  
  return parser.parse_args()
  

if __name__ == "__main__":
  
  args = parse_args()
  folder = args.dir
  
  adu_multi_sent = 0
  adu_clause = 0
  same_sent = 0
  
  tot = 0
  
  for filename in glob.iglob('{}/*.xml'.format(args.dir)):
    
    infile = ElementTree.parse(filename).getroot()
    
    gold = [e.text for e in infile.findall('edu')]
    n_gold = len(gold)
    pred = sent_tokenize(' '.join(gold))
    n_pred = len(pred)
    
    tot += n_gold
    
    if n_gold > n_pred:
      
      are_clause = n_gold - n_pred
      adu_clause += are_clause
      
      same_sent += n_gold - are_clause
   
    
    elif n_gold < n_pred:
      are_multi_sent = n_pred - n_gold
      adu_multi_sent += are_multi_sent
      same_sent += n_gold - are_multi_sent
    
    elif  n_pred == n_gold :
      same_sent += n_gold

  logger.info("ADU - Is Multi Sentence : {}".format(adu_multi_sent/tot))
  logger.info("ADU - Is Clause : {}".format(adu_clause/tot))
  logger.info("ADU - Is Sentence : {}".format(same_sent/tot))
    
    
    
    
    
    
  
  
  
  
  
  
  
  
  