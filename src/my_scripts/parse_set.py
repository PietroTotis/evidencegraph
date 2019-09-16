#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 10:46:00 2018

@author: Samuele Garda
"""

import sys
import pickle
from collections import defaultdict
from evidencegraph.argtree import SIMPLE_RELATION_SET
from evidencegraph.utils import load_corpus


SE_TYPES = {"GENERIC_SENTENCE" : "SE_GS",
              "GENERALIZING_SENTENCE" : "SE_GIS",
              "QUESTION" : "SE_Q",
              "RESEMBLANCE" : "SE_RES",
              "STATE" : "SE_S",
              "PROPOSITION" : "SE_P",
              "IMPERATIVE" : "SE_I",
              "EVENT" : "SE_E",
              "REPORT" : "SE_REP",
              "FACT" : "SE_F"}

def get_annotation(elems):
  
  anno = "SE_UNK"
  
  annos = [w for w in elems if w in SE_TYPES]
  
  if annos:
    anno = SE_TYPES.get(annos[-1],"SE_UNK")
  
  return anno

def rm_quotes(line):
  
  return line.replace('"','')
    

def parse_SE_annotations(path):
  
  annotations = {}
  
  with open(path) as infile:
    for idx,line in enumerate(infile):
      
      if idx == 0:
        continue
      
      elems = line.split('\t')
      elems = [rm_quotes(el) for el in elems]
      
      if elems[0].isdigit():
        if elems[1].startswith('micro'):
          curr_text = elems[1].strip().replace('.txt','')
          annotations[curr_text] = []
        else:
          if elems[1] != "":
            text = elems[1].strip()
            anno = get_annotation(elems)
            annotations[curr_text].append((text,anno))
      
      else:
        if elems[0] != "":
          text = elems[0].strip()
          anno = get_annotation(elems)
          annotations[curr_text].append((text,anno))
          
  return annotations
        

def pair_se_with_texts(texts,annos):
  
  se_types = defaultdict(list)
  
  for text_id,segs in texts.iteritems():
    segs = [seg.encode('utf-8') for seg in segs]
    partseg_anno = annos.get(text_id)
    for seg in segs:
      annotations = [pa[1] for pa in partseg_anno if pa[0] in seg]
      norm_seg = ''.join(seg.split()).lower()
      se_types[norm_seg] += annotations
    
  return se_types

if __name__ == "__main__":
  
  path_train = '../my_data/german_set/train_german_genre/argumentative_microtexts+genre+modalsverbs.csv'
  path_test = '../my_data/german_set/test_german_genre/argumentative_microtexts+genre+modalsverbs.csv'
  
  annos = parse_SE_annotations(path_train)
    
  anno_test = parse_SE_annotations(path_test)
  
  annos.update(anno_test)
  
  del anno_test
    
  texts,trees = load_corpus('de','adu',SIMPLE_RELATION_SET)
  
  se_types = pair_se_with_texts(texts,annos)
  
  pickle.dump(se_types, open( str(sys.argv[1]), 'wb'))
        