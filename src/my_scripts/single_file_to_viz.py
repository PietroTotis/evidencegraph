#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 15:30:13 2018

@author: Samuele Garda
"""

import logging
import argparse
from evidencegraph.arggraph import ArgGraph
from evidencegraph.argtree import FULL_RELATION_SET_ADU
from evidencegraph.classifiers import EvidenceGraphClassifier
from evidencegraph.features_text import (feature_function_segmentpairs,
                                         feature_function_segments,
                                         init_language)
from evidencegraph.graph_viz import get_segments_from_dseg,texts_mst2graph
from evidencegraph import utils as eg_utils


def parse_args():
  parser = argparse.ArgumentParser(description='Produce EvidenceGraph MST predictions and ArgGraph visualization for texts')
  parser.add_argument('--input', required = True, help='Input file containing text')
  parser.add_argument('--out', required = True, help='File where to save image')
  return parser.parse_args()


logger = logging.getLogger(__name__)
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(module)s: %(message)s', level = 'INFO')

if __name__ == "__main__":
  
  
  args = parse_args()
  
  infile = args.input
  out_png = args.out
  
  segments = get_segments_from_dseg(infile)
    
  logger.info("Initializing resources by language")
  init_language('de')
        
  model_path = './data/models/m112de-test-adu-full-noop__f2aa447__4'

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
  
  
  logger.info("Loading pre-trained model")
  
  clf = EvidenceGraphClassifier(feature_function_segments, feature_function_segmentpairs, **params)
  
  clf.ensemble = eg_utils.load(model_path)
  
  logger.info("Predicting on test case")
  
  mst = clf.predict(segments)
  
  roles = mst.get_ro_vector()
  
  triples = mst.get_triples()
  
  role_map = {1 : 'opp', 0 : 'pro'}
  
  seg_map ={"support" : "sup", "rebut" : "reb", "undercut" : "und", "example" : "exa"}
  
  new_mst = []
  
  for idx,seg in enumerate(triples):
    
    seg[2] = seg_map.get(seg[2],seg[2])
    
    seg.append(role_map[roles[idx]])
    
    new_mst.append(seg)
    
  print(  new_mst )
    
  texts_mst2graph(segments,new_mst,outpath = out_png, write_graph_desc = False )
      