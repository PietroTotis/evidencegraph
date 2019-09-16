#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 15:30:13 2018

@author: Samuele Garda
"""

import os
import argparse
import logging
from collections import OrderedDict
from evidencegraph.argtree import FULL_RELATION_SET_ADU
from evidencegraph.classifiers import EvidenceGraphClassifier
from evidencegraph.features_text import (feature_function_segmentpairs,
                                         feature_function_segments,
                                         init_language)
from evidencegraph.graph_viz import get_segments_from_dseg,texts_mst2graph
from evidencegraph import utils as eg_utils


def parse_args():
  parser = argparse.ArgumentParser(description='Produce EvidenceGraph MST predictions and ArgGraph visualization for texts')
  parser.add_argument('--dir', default = None, help='Folder where texts are stored. ONLY FOR CUSTOM TEXTS! ')
  parser.add_argument('--suffix', default = 'segmented', help='Suffix of files to be loaded. ONLY FOR CUSTOM TEXTS! ')
  parser.add_argument('--out', required=True, help="Folder where results will be stored")
  parser.add_argument('--text-ids', nargs = '*', default = None, help='Optionally pass COMMA SEPARATED LIST of file names in folder.')
  parser.add_argument('--model', required = True, help= "Path to model to be uused for predictions. MUST BE TRAINED WITH FULL_RELATION_SET_ADU")
  parser.add_argument('--graph-desc', action = 'store_true', help='Write in a text file graph description')
  
  return parser.parse_args()

logger = logging.getLogger(__name__)
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(module)s: %(message)s', level = 'INFO')



if __name__ == "__main__":
  
  
  args = parse_args()
  
  out_folder = args.out
  model_path = args.model
  
  logger.info("Start process...\n")
  
  
  logger.info("1) Loading data...\n")
 
  if not os.path.exists(args.out):
    os.makedirs(out_folder)
    logger.info("Created folder to store outputs : `{}`".format(out_folder))
    
  if not args.dir:
    
    logger.info("Loading original `micro-texts` corpus")
    
    texts,trees = eg_utils.load_corpus('de', 'adu', FULL_RELATION_SET_ADU)
  
  else:
    
    logger.info("Loading customly segmented texts from `{}`".format(args.dir))
    
    suffix = args.suffix
    
    in_dir = args.dir
    
    all_files = sorted([os.path.join(in_dir,file) for file in os.listdir(in_dir) if file.endswith(suffix)])
    
    if not all_files:
      raise ValueError("Folder `{}` seems to be empty! Make sure you are passing the right suffix of files for loading!\n".format(in_dir))
    
    
    id_seg_tuples = [(os.path.basename(file).split('.')[0],get_segments_from_dseg(file)) for file in all_files]
    texts = OrderedDict(id_seg_tuples)
  
  if args.text_ids:

    ids_to_keep = args.text_ids[0].split(',')
    
    logger.info("List of ids passed, keeping only  files with ids {}\n".format(ids_to_keep))
    
    texts = {mid : segs for (mid,segs) in texts.items() if mid in ids_to_keep}
        
    if not texts:
      raise ValueError("No files found with such ids! Make sure you are passing the right names!")
 
  logger.info("2) Start predicting on files...\n")
      
  logger.info("Initializing resources by language. This might take a while...\n")
  init_language('de')
  

  features = [
        'default', 'bow', 'bow_2gram', 'first_three',
        'tags', 'deps_lemma', 'deps_tag',
        'punct', 'verb_main', 'verb_all', 'discourse_marker',
        'context', 'clusters', 'clusters_2gram', 'discourse_relation',
        'vector_left_right', 'vector_source_target',
        'verb_segment', 'same_sentence', 'matrix_clause'
    ]
  
  params = {'feature_set': features,
            'relation_set': FULL_RELATION_SET_ADU,
            'optimize': False,
            'optimize_weighting': False}
  
  
  logger.info("Loading pre-trained model...\n")
  
  clf = EvidenceGraphClassifier(feature_function_segments, feature_function_segmentpairs, **params)
  
  clf.ensemble = eg_utils.load(model_path)
  
  logger.info("Predicting on files")
  
  role_map = {1 : 'opp', 0 : 'pro'}
  
  seg_map ={"support" : "sup", "rebut" : "reb", "undercut" : "und", "example" : "exa"}

  for text_id,segments in texts.items():
            
    file_name = os.path.join(out_folder,text_id)
    
    pred_file = '.'.join([file_name,'pred'])
    
    if not os.path.exists(pred_file):
    
      with open(pred_file, 'w') as outfile:
      
        try:
          mst = clf.predict(segments)
        except AssertionError:
          logger.error("Error when predicting for text : `{}`! Skipping...".format(text_id))
          continue
          
        roles = mst.get_ro_vector()
        
        triples = mst.get_triples()
        
        new_mst = []
        
        for idx,seg in enumerate(triples):
          
          seg[2] = seg_map.get(seg[2],seg[2])
          
          seg.append(role_map[roles[idx]])
          
          new_mst.append(seg)
        
        outfile.write("Predictions : {}".format(new_mst))
 
        texts_mst2graph(segments,new_mst,outpath = '.'.join([file_name,'png']) , write_graph_desc = args.graph_desc )
  
  logger.info("Completed process.")
      