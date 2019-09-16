#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 16:26:37 2018

@author: Samuele Garda
"""

from __future__ import division
import codecs
import logging
import argparse
import re
import glob
import math
from nltk.tree import Tree,ParentedTree
from nltk.tokenize import word_tokenize
from xml.etree import ElementTree
from collections import defaultdict
from segeval.util import SegmentationMetricError
#from dsegmenter.evaluation.segmentation import get_untyped_masses
from dsegmenter.evaluation.align import align_tokenized_tree, AlignmentError
from dsegmenter.evaluation.metrics import metric_pk,metric_windiff,metric_pi_bed,metric_alpha_unit_untyped

BAD_CHAR_RE = re.compile('[_]')
ESCAPE_SLASH_QUOTE = re.compile("\"")
ESCAPE_SLASH_APO = re.compile("\'")
FAKE_ANNO_GOLD = '(HS '
ROOT_NODE = '(ALL '
CLOSE_PAR = ' )'
SEG_TO_KEEP = ["ALL","HS","HSF", "ADV", "APK", "UNS", "FRE", "FRB"]


logger = logging.getLogger(__name__)
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(module)s: %(message)s', level = 'INFO')


def parse_args():
  
  parser = argparse.ArgumentParser(description='Evaluate discourse segmenter with non-typed metrics')
  parser.add_argument('-g','--gold', required=True, help='Directory containing files with gold segmentation. \n Must contain XML files.')
  parser.add_argument('-p','--pred', required=True, help='Directory containing files with predicted segmentation')
  parser.add_argument('-pe','--pred-ext', required=True, help='Extension of files in prediction directory')
  parser.add_argument('-e','--exclude',action = 'store_true', help='Exclude segments that are not: ["ALL","HS","HSF", "ADV", "APK", "UNS", "FRE", "FRB"] ')
  
  return parser.parse_args()
  

def avg_std(values):
  avg = sum(values) / len(values)
  
  std = math.sqrt(sum([(v - avg) ** 2 for v in values]) / (len(values) - 1))
  
  return avg,std

def add_root_node(tree):
  
  tree = ROOT_NODE + tree
  tree = tree + CLOSE_PAR
  
  return tree

def add_fake_annotation_branch(branch):
  
  branch = FAKE_ANNO_GOLD + branch
  branch = branch + CLOSE_PAR
  
  return branch


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

def normalize_pred(pred):
  
  pred = pred.replace("\\","").replace("\'s","'s")
  
  return pred
  
def preprocess_files(gold_file,pred_file):
  
  gold = ElementTree.parse(gold_file).getroot()
  
  pred = normalize_pred(open(pred_file).read())
  
  # preprocess XML : extract edu, add fake type 
  gold = [e.text for e in gold.findall('edu')]
  
  gold = [add_fake_annotation_branch(' '.join(word_tokenize(b))) for b in gold]
  
  gold = '\n'.join(gold).encode('utf-8')
  
  gold = add_root_node(gold)
  
  pred = add_root_node(pred)
  
  gold = BAD_CHAR_RE.sub(' ', gold)
  pred = BAD_CHAR_RE.sub(' ', pred)
  
  gold = gold.split()
  pred = pred.split()
  
  try:
    error, aligned_gold, aligned_pred = align_tokenized_tree(gold, pred,
                                                             tree_pair_name = glob.os.path.basename(gold_file))
  except AlignmentError as err:
    logger.warning("Error in alignment with files : {} - {}".format(gold_file,pred_file))
    print err
    aligned_gold = None
    aligned_pred = None
    
  return aligned_gold,aligned_pred


def preprocess_trees(aligned_gold,aligned_pred,exclude_sub): 
  
  aligned_gold = ' '.join(aligned_gold)
  aligned_pred = ' '.join(aligned_pred)
  
  gold_tree = Tree.fromstring(aligned_gold)
  if exclude_sub:
   pred_tree = get_pred_tree_custom(aligned_pred)
  else:
    pred_tree = Tree.fromstring(aligned_pred)
  
  return gold_tree,pred_tree
  
if __name__ == "__main__":
  
  args = parse_args()
  
  gold_dir = args.gold
  pred_dir = args.pred
  pred_ext = args.pred_ext
  exclude = args.exclude
  
  if exclude:
    logger.info("Excluding {} from predictions by merging in parent node".format(SEG_TO_KEEP))
  
  tot = 0
  processed = 0
  scores = defaultdict(list)
  
  gold_dir = sorted(list(glob.iglob('{}/*.xml'.format(gold_dir))))
  pred_dir = sorted(list(glob.iglob('{}/*.{}'.format(pred_dir,pred_ext))))
  
  for idx,(gold_file,pred_file) in enumerate(zip(gold_dir,pred_dir)):
    
    logger.info("Processing test case {}".format(idx))
    gold,pred = preprocess_files(gold_file,pred_file)
      
    tot += 1
      
    if gold and pred: 
        try:
          gold_tree,pred_tree = preprocess_trees(gold,pred, exclude_sub = exclude)
          
          processed += 1
  
          scores['Pk'].append(metric_pk([gold_tree],[pred_tree]))
          scores['WinDiff'].append(metric_windiff([gold_tree],[pred_tree]))
          scores['Pbed'].append(metric_pi_bed([gold_tree],[pred_tree]))
          scores['AlphaUnit'].append(metric_alpha_unit_untyped([gold_tree],[pred_tree]))
        except SegmentationMetricError:
          logger.warning("Segmentation Error for files : {} - {}".format(gold_file,pred_file))
      

  logger.info("Processed {} trees out of {}".format(processed,tot))
  logger.info("Average Pk : {} (+- {})".format(*avg_std(scores.get('Pk'))))
  logger.info("Average WinDiff : {} (+- {})".format(*avg_std(scores.get('WinDiff'))))
  logger.info("Average Pbed : {} (+- {})".format(*avg_std(scores.get('Pbed'))))
  logger.info("Average AlphaUnit : {} (+- {})".format(*avg_std(scores.get('AlphaUnit'))))


#############
#TESTS
#############


#(HS Ja , (SUB seinen Müll immer ordentlich zu trennen ) ist nervig und mühselig . )
#(HS Drei verschiedene Müllbeutel müffeln in der Küche (HSF und müssen in drei unterschiedliche Tonnen einsortiert werden . ) )
#(HS Aber immer noch wird in Deutschland viel zu viel Müll produziert (HSF und zu viele Ressourcen gehen verloren , (ADV wenn zusammen verbrannt wird , ) (OBJ was getrennt eigentlich verwertet werden könnte . ) ) )
#(HS Wir Berliner sollten die Chance nutzen und Vorreiter im Mülltrennen werden ! )
#  gold_file = './my_data/arg-microtexts/corpus/de/micro_b001.xml'
#  pred_file = './my_data/bitpar_segmented/micro_b001.txt.segmented'
#  
#  
#  gold = "(HS Ja , seinen Müll immer ordentlich zu trennen ist nervig und mühselig . )".split()
#  pred = "(HS Ja , (SUB seinen Müll immer ordentlich zu trennen ) ist nervig und mühselig . )".split()
#  
#  try:
#    error, aligned_gold, aligned_pred = align_tokenized_tree(gold, pred)
#  except AlignmentError as err:
#    print "Error in alignment with files : {} - {}".format(gold_file,pred_file)
#    print "{}".format(err)
#    
#    aligned_gold = None
#    aligned_pred = None
#    
#  print aligned_gold
#  print aligned_pred
#      

#  
#  gold = ElementTree.parse(gold_file).getroot()
#  
#  gold = [e.text for e in gold.findall('edu')]
#  
##  pred = ' '.join(open(pred_file).read().split()) 
#
#  gold = ' '.join([add_fake_annotation_branch(b) for b in gold]).encode('utf-8')
#  
#  gold = add_root_node(gold)
#  
##  pred = add_root_node(pred)
#  
#  gold = BAD_CHAR_RE.sub(' ', gold)
##  pred = BAD_CHAR_RE.sub(' ', pred)
#  
##  print gold
##  print '\n'
##  print pred
##  
#  
#  try:
#    error, aligned_gold, aligned_pred = align_tokenized_tree(gold, gold)
#  except AlignmentError:
#    print "Error in alignment with files : {} - {}".format(gold_file,pred_file)
#    aligned_gold = None
#    aligned_pred = None
#  
#  
#  print aligned_gold,type(gold)
#  print '\n'
#  print aligned_pred,type(pred)

      
      
      
