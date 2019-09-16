#!/usr/bin/env python2
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 11:07:55 2019

@author: Samuele Garda
"""

import re
import glob
import pandas as pd
import codecs
from lxml import etree
from collections import namedtuple
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from gensim.models import KeyedVectors



PUNCUTATION_TOKENS = ['.', '..', '...', ',', ';', ':', '(', ')', '"', '\'', '[', ']',
                      '{', '}', '?', '!', '-', '–', '+', '*', '--', '\'\'', '``']
PUNCTUATION = '?.!/;:()&+'.encode('utf-8')

MAP_LANG = {"de" : "german","en" : "english"}


def load_stopwords(lang):
  
  lang = MAP_LANG.get(lang)
  
  stop_words = stopwords.words(lang)
  
  stop_words = [w.encode('utf-8') for w in stop_words]
  
  return stop_words

class MicroTextFile(namedtuple('MicroTextFile', 'id topic stance sents txt txt_pp')):
  pass

class MensaTextFile(namedtuple('MensaTextFile', 'sents txt txt_pp')):
  pass

class CorpusTextFile(namedtuple('CorpusTextFile', 'txt txt_pp')):
  pass


def process_text_string(txt_string,stop_words):
  
  words = word_tokenize(txt_string)
  words = [x for x in words if x not in PUNCUTATION_TOKENS]
  words = [re.sub('[{}]'.format(PUNCTUATION), '', x) for x in words]
  words = [x for x in words if x not in stop_words]
  
  return words


def load_corpus(file,stop_words):
  
  corpus = []
  
  with codecs.open(file, encoding = 'utf-8') as infile:
    for line in infile:
      words = process_text_string(line, stop_words = stop_words)
      corpus.append(CorpusTextFile(line,words))
  
  return corpus


def append_to_corpus(file,text):

  with codecs.open(file, "a", encoding = 'utf-8') as outfile:
    to_write = "{}\n".format(text.encode('utf-8'))
    outfile.write(to_write.decode('utf-8'))

def load_mensa_file(file,stop_words):
  
  sents = []
  with codecs.open(file, encoding = 'iso-8859-1') as infile:
    for line in infile:
      sents.append(line.strip())
  
  words_raw = '\n'.join(sents)
  words = process_text_string(words_raw, stop_words = stop_words)
  
  return MensaTextFile(sents,words_raw,words)
  

def load_argmin_file(file,stop_words):
  
  xml = etree.parse(file)
  
  txt_id = xml.xpath('/arggraph')[0].get('id')
  txt_topic = xml.xpath('/arggraph')[0].get('topic_id')
  txt_stance = xml.xpath('/arggraph')[0].get('stance','unk')
  sents = [elm.text for elm in xml.xpath('/arggraph/edu')]
  words_raw = ' '.join(sents)
  words_raw = '\n'.join(sent_tokenize(words_raw))
  words = process_text_string(words_raw, stop_words = stop_words)
 
  
  return MicroTextFile(txt_id,txt_topic,txt_stance,sents,words_raw,words)

def load_topic_triggers(path,lang,stop_words):
  
  tt = pd.read_csv(path, sep = ',')
  tt["{}_pp".format(lang)] = tt[lang].apply(process_text_string,stop_words = stop_words)
  
  return tt

def load_argmin_corpus(path,stop_words):
  
  corpus = []
  
  for f in glob.iglob(glob.os.path.join(path,"*.xml")):
    
    corpus.append(load_argmin_file(f,stop_words))
  
  return corpus

def load_mensa_corpus(path,stop_words):
  
  corpus = []
  
  for f in glob.iglob(glob.os.path.join(path,"*.txt")):
    
    corpus.append(load_mensa_file(f,stop_words))
    
  return corpus
    

def load_model(model_path,limit):
  
  model = KeyedVectors.load_word2vec_format(model_path, binary=True, limit = limit)
  
  model.init_sims(replace=True)
  
  return model
  
  
if __name__ == "__main__":
  
  x = load_topic_triggers('./data/arg-microtexts/topic_triggers.csv')
  
  print(x.de)