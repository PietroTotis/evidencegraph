#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 14:20:40 2018

@author: Samuele Garda
"""

import logging
import itertools
from .arggraph import ArgGraph
from nltk.tree import ParentedTree
from nltk.tokenize import word_tokenize

logger = logging.getLogger(__name__)
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(module)s: %(message)s', level = 'INFO')


FAKE_ANNO_GOLD = '(HS '
ROOT_NODE = '(ALL '
CLOSE_PAR = ' )'
SEG_TO_KEEP = ["ALL","HS","HSF", "ADV", "APK", "UNS", "FRE", "FRB"]


def add_root_node(tree):
  
  tree = ROOT_NODE + tree
  tree = tree + CLOSE_PAR
  
  return tree

def normalize_pred(pred):
  
  pred = pred.replace("\\","").replace("\'s","'s")
  
  return pred


def get_pred_tree_custom(tree):
  
  tree = ParentedTree.fromstring(tree)
  
  try:
    for index, sub in enumerate(tree.subtrees()):
      if sub.label() not in SEG_TO_KEEP:
        parent = sub.parent()  
        tree[parent.treeposition()] = ParentedTree.convert(parent.flatten())
  except IndexError:
    pass
      
  return tree

def get_trees_as_segments(tree):
  
  tree_toks = word_tokenize(str(tree))
  
  tree_toks.pop(0)
  
  tree_toks.pop(-1)
  
  tree_toks = [w for w in tree_toks if w not in SEG_TO_KEEP]
  
  tree_toks = [w for w in tree_toks if w != ')']
  
  tree_toks.append('(')
    
  all_segments = []
  
  open_par = 0
  
  for t in tree_toks:
    if t == '(':
      if open_par == 0:
        curr_seg = []
        open_par += 1
      else:
        all_segments.append(curr_seg)
        curr_seg = []
    else:
      curr_seg.append(t)
  
  return all_segments



def get_segments_from_dseg(infile):
  
  pred = open(infile).read().decode('utf-8')
  
  pred = normalize_pred(pred)
  
  pred = add_root_node(pred)
  
  tree = get_pred_tree_custom(pred)
  
  segments = get_trees_as_segments(tree)
  
  segments = [' '.join(seg) for seg in segments]
  
  segments = [seg for seg in segments if seg]
  
  segments = [seg.decode('utf-8') for seg in segments]
      
  return segments


def texts_mst2graph(segments,mst_role,outpath,write_graph_desc = False):
  
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
        logger.warning("Error in graph consturction for : `{}`!".format(outpath))
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
        logger.warning("Error in graph consturction for : `{}`!".format(outpath))
        logger.warning("A `link` edge is defined for a node that does not have a specified role")
        logger.warning("Creating graph anyway without `link` edge")

                                                                  

  if write_graph_desc:
    with open('{}.txt'.format(outpath),'w+') as out_file:
      out_file.write("test edges\n")
      for item in test_graph.edge.items():
        out_file.write("{}\n".format(item))
     
      out_file.write("\n")
      out_file.write("test nodes\n")
      for item in test_graph.node.items():
        out_file.write("{}\n".format(item))
    
  
  try:
    test_graph.render_as_png('{}'.format(outpath))
    logger.info("Saved visualization of argumentative structure at : {}\n".format(outpath))
  except KeyError:
    logger.error("Error in graph consturction for : `{}`! No file will be produced\n".format(outpath))