#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 15:06:05 2018

@author: Samuele Garda
"""

import itertools
import argparse
from evidencegraph.arggraph import ArgGraph
from evidencegraph.argtree import ArgTree
from evidencegraph.argtree import FULL_RELATION_SET_ADU


def parse_args():
  parser = argparse.ArgumentParser(description='Test arggraph rendering')
  parser.add_argument('--out', required=True, help='File where to store produced images')
  parser.add_argument('--seg-type', required=True, choices = ('gold','preseg','seg'),
                      help='Which type of text segmentation to use: `preseg` for original, `seg` for post-processed DiscourseSegmeter')
  parser.add_argument('--graph-desc', action = 'store_true', help='Write to a text file graph description')
  
  return parser.parse_args()


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
      
      test_graph.add_edge_with_relation_node('c{}'.format(branch[0]), 'a{}'.format(branch[0]),'c{}'.format(branch[1]),'und' )
 
  # add link
  for branch in mst_role:
    
    if branch[2] == 'link':
      
      linked_to = branch[1]
      edge_to_be_linked = 'c{}'.format(linked_to)
      
      if edge_to_be_linked in set(list(itertools.chain(*test_graph.edges()))):
        test_graph.add_edge('a{}'.format(branch[0]), 'c{}'.format(linked_to), type="src")
      else:
        pass
#      print "Seg : ",branch[0],"(",segments[branch[0]-1],")","is linked to edge",'c{}'.format(linked_to)
#      print "Which should have been created by segment ", segments[linked_to-1
                                                                  

  if write_graph_desc:
    with open('{}.txt'.format(outpath),'w+') as out_file:
      out_file.write("test edges\n")
      for item in test_graph.edge.iteritems():
        out_file.write("{}\n".format(item))
    
        
      
      out_file.write("\n")
      out_file.write("test nodes\n")
      for item in test_graph.node.iteritems():
        out_file.write("{}\n".format(item))
    
  
  try:
    test_graph.render_as_png('{}.png'.format(outpath))
    print("Saved visualization of argumentative structure at : {}".format(outpath))
  except KeyError:
    raise ValueError("There has been an error while trying to create the graph! As of now, I can tell you that probably a link edge is defined for a node that does not have a function")
                    
  
  


if __name__ == "__main__":
  
  args = parse_args()
  
  out = args.out
  seg_type = args.seg_type
  write_graph_desc = args.graph_desc


  gold_graph = ArgGraph()
  gold_graph.load_from_xml('data/corpus/german/arg/micro_b001.xml')
  
  gold_tree_full = ArgTree(relation_set=FULL_RELATION_SET_ADU)
  gold_tree_full.load_from_arggraph(gold_graph)
  
  
  
  segmented = ["Ja, seinen Müll immer ordentlich zu trennen ist nervig und mühselig.", 
               "Drei verschiedene Müllbeutel müffeln in der Küche",
               "und müssen in drei unterschiedliche Tonnen einsortiert werden.",
               "Aber immer noch wird in Deutschland viel zu viel Müll produziert",
               "und zu viele Ressourcen gehen verloren, wenn zusammen verbrannt wird, was getrennt eigentlich verwertet werden könnte.",
               "Wir Berliner sollten die Chance nutzen und Vorreiter im Mülltrennen werden!"]
  
  pre_segmented = ["Ja, seinen Müll immer ordentlich zu trennen ist nervig und mühselig.", 
               "Drei verschiedene Müllbeutel müffeln in der Küche und müssen in drei unterschiedliche Tonnen einsortiert werden.",
               "Aber immer noch wird in Deutschland viel zu viel Müll produziert",
               "und zu viele Ressourcen gehen verloren, wenn zusammen verbrannt wird, was getrennt eigentlich verwertet werden könnte.",
               "Wir Berliner sollten die Chance nutzen und Vorreiter im Mülltrennen werden!"]
  
  segmented = [seg.decode('utf-8') for seg in segmented]
  pre_segmented = [seg.decode('utf-8') for seg in pre_segmented]
  

  
  #################
  # gold full
  #################
  gold_full = [[1, 5, 'reb','opp'], [2, 1, 'sup','opp'], [3, 1, 'und','pro'], [4, 3, 'link','pro']] 
  
  ############################
  # pre-segmented pred full
  ############################
  pre_seg_full = [[1, 5, 'reb', 'opp'], [2, 1, 'sup', 'opp'], [3, 5, 'sup', 'pro'], [4, 5, 'link', 'pro']]

  #############################
  # segmented pred full
  ###########################
  
  seg_full = [[1, 6, 'sup', 'pro'], [2, 1, 'sup', 'pro'], [3, 2, 'link', 'pro'], [4, 6, 'sup', 'pro'], [5, 6, 'link', 'pro']]
  

  
  if seg_type == 'gold':
    
    mst_role,segments = gold_full,pre_segmented
  
  elif seg_type == 'preseg':
  
    mst_role,segments = pre_seg_full,pre_segmented
    
  elif seg_type == 'seg':
    
    mst_role,segments = seg_full,segmented
    
  else:
  
    raise ValueError("Segmentation type not in available choices! Must be either `preseg` or `seg`! Found `{}`".format(seg_type))
    
    
  texts_mst2graph(segments,mst_role,outpath = out, write_graph_desc = write_graph_desc)

 
    
    