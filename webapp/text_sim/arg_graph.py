#!/usr/bin/env python2
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 12:15:08 2019

@author: Samuele Garda
"""

import logging
import itertools
from nltk.tokenize import sent_tokenize
from pydot import graph_from_dot_data
from evidencegraph.arggraph import ArgGraph
from evidencegraph.argtree import FULL_RELATION_SET_ADU
from evidencegraph.features_text import (feature_function_segmentpairs,
                                         feature_function_segments,
                                         init_language)
from evidencegraph.classifiers import EvidenceGraphClassifier
from evidencegraph import utils as eg_utils

logger = logging.getLogger(__name__)
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(module)s: %(message)s', level = 'INFO')

ROLE_MAP = {1 : 'opp', 0 : 'pro'}
SEG_MAP  = {"support" : "sup",
            "rebut" : "reb",
            "undercut" : "reb",
            "example" : "sup", 
            "link" : "sup",
            "att" : "reb"}


def init_lang_classifier(model_path):
  
  init_language('de')

  features = [
        'default', 'bow', 'bow_2gram', 'first_three',
        'tags', 'deps_lemma', 'deps_tag',
        'punct', 'verb_main', 'verb_all', 'discourse_marker',
        'context', 'clusters', 'clusters_2gram', 'discourse_relation',
        'vector_left_right', 'vector_source_target',
        'verb_segment', 'same_sentence', 'matrix_clause'
    ]
  
  PARAMS = {'feature_set': features,
            'relation_set': FULL_RELATION_SET_ADU,
            'optimize': False,
            'optimize_weighting': False}
  
  clf = EvidenceGraphClassifier(feature_function_segments, feature_function_segmentpairs, **PARAMS)
  clf.ensemble = eg_utils.load(model_path)
  
  return clf


def create_arggraph_from_triples(segments,mst_role):
  
  test_graph = ArgGraph()
  
  #ADD NODES
  all_segs = [i for i in range(1,len(segments)+1)]  
  
  # add premises
  for branch in mst_role:
    index = branch[0]
    test_graph.add_edu_adu('e{}'.format(index), segments[index-1] , 'a{}'.format(index), branch[-1])
    all_segs.remove(index)
    
  # add CC  
  for s in all_segs:
    test_graph.add_edu_adu('e{}'.format(s), segments[s-1] , 'a{}'.format(s), 'pro')
    
  #add edges
  # create straightforward edges first
  for branch in mst_role:
    if branch[2] not in ['link','und']:
      test_graph.add_edge_with_relation_node('c{}'.format(branch[0]), 'a{}'.format(branch[0]), 'a{}'.format(branch[1]), branch[2])
  
  # add undercut
  for branch in mst_role:
    
    if branch[2] == 'und':
      
      linked_to = branch[1]
      edge_to_be_linked = 'c{}'.format(linked_to)
      
      if edge_to_be_linked in set(list(itertools.chain(*test_graph.edges()))):
        test_graph.add_edge_with_relation_node('c{}'.format(branch[0]), 'a{}'.format(branch[0]),'c{}'.format(branch[1]),'und' )
      else:
        logger.warning("Error in graph consturction for text : {}...".format(' '.join(segments)[:10]))
        logger.warning("An `undercut` edge is defined for a node that does not have a specified role")
        logger.warning("Creating graph anyway without `undercut` edge")
 
  # add link
  for branch in mst_role:
    
    if branch[2] == 'link':
      
      linked_to = branch[1]
      edge_to_be_linked = 'c{}'.format(linked_to)
      
      if edge_to_be_linked in set(list(itertools.chain(*test_graph.edges()))):
        test_graph.add_edge('a{}'.format(branch[0]), 'c{}'.format(linked_to), type="src")
      else:
        logger.warning("Error in graph consturction for text : {}...".format(' '.join(segments)[:10]))
        logger.warning("A `link` edge is defined for a node that does not have a specified role")
        logger.warning("Creating graph anyway without `link` edge")
        
  
  return test_graph


def get_arggraph(clf,text):
  
  segments = sent_tokenize(text)
  
  print("Segments : {}".format(segments))
  
  mst = clf.predict(segments)
  
  print("MST : {}".format(mst))
  
  roles = mst.get_ro_vector()
  triples = mst.get_triples()
  
  print("MST : {}".format(triples))
  
  new_mst = []
        
  for idx,seg in enumerate(triples):
    
    seg[2] = SEG_MAP.get(seg[2],seg[2])
    
    seg.append(ROLE_MAP[roles[idx]])
    
    new_mst.append(seg)
    
  
  print("New MST : {}".format(new_mst))
    
  graph = create_arggraph_from_triples(segments,new_mst)
  
  
  dot_graph = graph.render_as_dot()
    
  pydot_graph = graph_from_dot_data(dot_graph)
  
  return pydot_graph
  
  
  
  

    
  
  
  
  
  