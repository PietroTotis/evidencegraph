#!/usr/bin/env python2
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 14:20:32 2019

@author: Samuele Garda
"""

import logging
from flask import Flask, render_template, request, redirect,url_for,session
from text_sim.load import load_corpus,load_stopwords,load_model,append_to_corpus
from text_sim.sim import ClusteringViz
from text_sim.viz import visualize_text_clusters
from text_sim.arg_graph import init_lang_classifier,get_arggraph
import base64

logger = logging.getLogger(__name__)
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(module)s: %(message)s', level = 'INFO') 

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey"

CORPUS = './data/corpus.txt'
STOP_WORDS = load_stopwords('de')
ARGMIN_MODEL = './data/arg_models/m112de-test-adu-simple-noop__f2aa447__49'
logger.info("Loading language resources, this might take a while")
CLF = init_lang_classifier(ARGMIN_MODEL)
logger.info("Completed loading language resources")
W2V_MODEL = load_model('./data/german.model',limit = 2000)  

@app.route("/text_input",methods=["GET", "POST"])
def text_input():
  """
  Input page
  """
    
  if request.method == 'POST':
    
    return redirect(url_for('options'))

  return render_template("login_form.html")


@app.route("/options", methods=["POST"])
def options():
    
  text = request.form['text_input']
      
  session['text'] = text
  
  append_to_corpus(CORPUS,text)
        
  return render_template("options.html")



@app.route("/visualization", methods=["GET", "POST"])
def visualization():
  
  text = session.get('text')
  
  if request.method == 'POST':
    
    return redirect(url_for('visualize'))
  
  return render_template("visualization.html", text = text)


@app.route("/visualize",methods=["GET","POST"])
def visualize():
  """
  Visualization
  """
      
  text = session.get('text')

  n_clusters = int(request.form.get('clusters'))
    
  cluster_viz = ClusteringViz(n_clusters = n_clusters)

  corpus = load_corpus(CORPUS,STOP_WORDS)
  
  corpus_pp = [t.txt_pp for t in corpus]
  
  corpus_raw = [t.txt for t in corpus]
  
  logger.info("Loaded corpus")
  
  kmeans,X_2d,labels,descs = cluster_viz.create_plot_data(corpus_pp,corpus_raw,W2V_MODEL)
  
  script,div = visualize_text_clusters(kmeans,X_2d,labels,descs)

  return render_template("visualize.html", script=script, div=div,text = text)

  
@app.route("/arggraph", methods=["GET"])
def arggraph():
  """
  Display arg graph
  """
  
  text = session.get('text')
  
  pydot_graph = get_arggraph(clf = CLF, text = text)

  chart_output = pydot_graph.create_png(prog='dot')
  chart_output = base64.b64encode(chart_output).decode('utf-8')
  
  return render_template("arggraph.html", chart_output=chart_output, text = text)
    


if __name__ == "__main__":
  
  app.run(port = 5000, debug = True)

