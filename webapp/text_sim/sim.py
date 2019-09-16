#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 12:07:37 2019

@author: Samuele Garda
"""

import logging
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from gensim.similarities import WmdSimilarity


logger = logging.getLogger(__name__)
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(module)s: %(message)s', level = 'INFO') 


class WMDQuery:
  
  def __init__(self,corpus,model,num_best):
    
    self.corpus = corpus
    self.num_best = num_best
    self.instance = WmdSimilarity([f.txt_pp for f in self.corpus], model, num_best=self.num_best)
    
  
  def get_doc_word_vec(self,words):
    
    vecs = [self.instance.w2v_model[w] for w in words if w in self.instance.w2v_model]
    
    vec = np.mean(vecs,axis = 0) if vecs else np.zeros(300)
    
    return vec
    

  def query(self,raw_query,pp_query):
    
    sims = self.instance[pp_query]
    
    print("\n")
    print("Query : {}".format(raw_query))
    
    for i in range(self.num_best):
      raw = self.corpus[sims[i][0]].txt
      score = sims[i][1]
      print("\n")
      print("Score : {}".format(score))
      print("{}".format(raw))
      
  
  def tsne_values(self,raw_query,pp_query):
    
    sims = self.instance[pp_query]
    
    sim_score = [0]
    desc = [raw_query]
    vecs = [self.get_doc_word_vec(pp_query)]
    
    for i in range(self.num_best):
      sim_score.append(np.round(sims[i][1],5))
      desc.append(self.corpus[sims[i][0]].txt)
      vecs.append(self.get_doc_word_vec(self.corpus[sims[i][0]].txt_pp))
    
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(vecs)
  
    return new_values[:,0],new_values[:,1],desc,sim_score




class ClusteringViz(object):
  
  def __init__(self,n_clusters):
    
    self.n_clusters = n_clusters
  
  
  def get_word2vec_representation(self,model,words):
    
    vecs = [model[w] for w in words if w in model]
    
    vec = np.mean(vecs,axis = 0) if vecs else np.zeros(300)
    
    return vec
  
  def build_X(self,corpus,model):
    
    vecs = []
    
    for text in corpus:
      
      vecs.append(self.get_word2vec_representation(model,text))
      
    matrix = np.vstack(vecs)
    
    return matrix
     
  def compute_pca(self,X):
    
    pca = PCA(n_components=2).fit(X)
    pca_2d = pca.transform(X)
    
    return pca_2d
  
  def kmeans_clustering(self,X,n_clusters = 2):
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
    
    labels = kmeans.labels_
    
    return kmeans,labels
  
  def create_plot_data(self,corpus_pp,corpus_raw,model):
    
    X = self.build_X(corpus_pp,model)
        
    logger.info("Created embedding matrix")
    
    X_2d = self.compute_pca(X)
        
    logger.info("Created 2d representation of embeddings matrix with PCA")
    
    kmeans,labels = self.kmeans_clustering(X_2d,n_clusters = self.n_clusters)
        
    logger.info("Fitted KMean with {} clusters".format(self.n_clusters))
        
    return kmeans,X_2d,labels,corpus_raw
  
  
  
  