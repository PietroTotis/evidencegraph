#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 15:20:03 2019

@author: Samuele Garda
"""

import numpy as np
from bokeh.palettes import brewer,d3
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.embed import components


def visualize_text_clusters(clf,X_2d,labels,descs):
  
  colors = d3["Category10"][len(np.unique(labels))]

  colormap = {i: colors[i] for i in np.unique(labels)} 
  
  mesh_ = create_mesh(X_2d, step=0.01)
  
  mesh_pred = predict_mesh(clf, mesh_)
  
  xx = X_2d[:,0]
  yy = X_2d[:,1]
  
  source_query = ColumnDataSource(data= dict( xx= [xx[-1]] , 
                                             yy= [yy[-1]], 
                                             labels = [labels[-1]], 
                                             descs = [descs[-1]], 
                                             colors = [colormap.get(labels[-1])]
                                             ))
  
  source_similar = ColumnDataSource(data=dict(xx=xx[:-1], 
                                              yy=yy[:-1],
                                              labels = labels[:-1],
                                              descs=descs[:-1] , 
                                              colors = [colormap.get(x) for x in labels[:-1]]
                                              ))
  
  source_mesh = ColumnDataSource(data=dict(mesh_x=mesh_[0].ravel(),
                                           mesh_y=mesh_[1].ravel(),
                                           colors_mesh= [colormap.get(x) for x in mesh_pred.ravel()]))
  
  
               
  p = figure(plot_width=1000, plot_height=1000, tools=["pan","wheel_zoom","zoom_in","zoom_out","box_zoom"],
             title="Clusters")
  
  p.xaxis.axis_label = 'PC1'
  p.yaxis.axis_label = 'PC2'
    
  p_query = p.triangle('xx', 'yy', size=20, source=source_query, color='colors')
  
  p_data = p.scatter('xx', 'yy', size=20, source=source_similar, color = 'colors', legend="labels")
  
  p.square('mesh_x', 'mesh_y', fill_color='colors_mesh', size = 13, line_alpha=0, fill_alpha=0.05, source=source_mesh)
  
  hover = HoverTool(tooltips="""
    <div style="font-family: Ubuntu;
                width : 500px;
                position: fixed;
                left: 85px;
                top: 370px;
                border: 2px solid black;
                background: #f5f5f5;
                padding: 10px">

    <span style="font-size: 12px;"><br>@descs </span>
    </div>
        """,renderers=[p_data,p_query])
  
  p.add_tools(hover)
  
  script, div = components(p)
  
  return script,div
  
  
def create_mesh(matrix_2D, bound=.1, step=.05):
  """
  create_mesh will generate a mesh grid for a given matrix
  
  matrix_2D: input matrix (numpy)
  bound:     boundary around matrix (absolute value)
  step:      step size between each point in the mesh
  """

  # set bound as % of average of ranges for x and y
  bound = bound*np.average(np.ptp(matrix_2D, axis=0))
  
  # set step size as % of the average of ranges for x and y 
  step = step*np.average(np.ptp(matrix_2D, axis=0))

  # get boundaries
  x_min = matrix_2D[:,0].min() - bound
  x_max = matrix_2D[:,0].max() + bound
  y_min = matrix_2D[:,1].min() - bound 
  y_max = matrix_2D[:,1].max() + bound
  
  # create and return mesh
  mesh = np.meshgrid(np.arange(x_min, x_max, step), np.arange(y_min, y_max, step))
  return mesh

def predict_mesh(trained_clf, mesh):
  """
  predict_mesh will generate predictions for all points in a mesh grid
  
  clf:    sklearn classifier (e.g. knn)
  mesh:   tuple returned by create mesh (xx, yy)
  """
  
  # make predictions based on all values in mesh and return
  predictions = trained_clf.predict(np.c_[mesh[0].ravel(), mesh[1].ravel()])
  predictions = predictions.reshape(mesh[0].shape)    
  return predictions


#def plot_decision_boundaries(X_2D, targets, labels, 
#                             trained_clf, X_test_, colormap_, labelmap_, 
#                             step_=0.02, title_="", xlabel_="", ylabel_=""):
#    """
#    X_2D:        2D numpy array of data (e.g. two features from iris.data or 2D PCA)
#    targets:     array of target data (e.g iris.target)
#    labels:      array of labels for target data
#    trained_clf: previously trained classifier (e.g. KNN)
#    X_test_:     test data taken (e.g. from test_train_split())
#    colormap_:   map of target:color (e.g. {'0': 'red', ...} )
#    labelmap_:   map of target:label (e.g. {'0': 'setosa', ...} )
#    step_:       step size for mesh (e.g lower = higher resolution)
#    title_:      plot title
#    xlabel_:     x-axis label
#    ylabel_:     y-axis label
#    """
#    
#    # Create a mesh
#    mesh_ = create_mesh(X_2D, step=step_)
#
#    # Get predictions for each point in the mesh
#    mesh_pred = predict_mesh(trained_clf, mesh_)
#    
#    # Get predictions for test data, all data
#    test_pred = trained_clf.predict(X_test_)
#    data_pred = trained_clf.predict(X_2D)
#
#    # create color vectors [assume targets are last index]
#    colors = [colormap_[str(t)] for t in targets]
#    colors_test_pred = [colormap_[str(p)] for p in test_pred]
#    colors_pred_data = [labelmap_[str(x)] for x in data_pred]
#    colors_mesh = [colormap_[str(int(m))] for m in mesh_pred.ravel()]
#    
#    """ Create ColumnDataSources  """
#    source_data = ColumnDataSource(data=dict(X=X_2D[:,0], 
#                                             Y=X_2D[:,1],
#                                             colors=colors, 
#                                             colors_legend=labels,
#                                             colors_pred_data=colors_pred_data))
#
#
#    source_test = ColumnDataSource(data=dict(X_test=X_test_[:,0],
#                                                    Y_test=X_test_[:,1],
#                                                    colors_test_pred=colors_test_pred))
#
#    source_mesh = ColumnDataSource(data=dict(mesh_x=mesh_[0].ravel(),
#                                             mesh_y=mesh_[1].ravel(),
#                                             colors_mesh=colors_mesh))    
#    
#    # Initiate Plot
#    tools_ = ['crosshair', 'zoom_in', 'zoom_out', 'save', 'reset', 'tap', 'box_zoom']
#    p = figure(title=title_, tools=tools_)
#    p.xaxis.axis_label = xlabel_
#    p.yaxis.axis_label = ylabel_
#
#    # plot all data
#    p_data = p.circle('X', 'Y', fill_color='colors',
#                  size=10, alpha=0.5, line_alpha=0, 
#                  source=source_data, name='Data')
#    
#    # plot thick outline around predictions on test data
#    p_test = p.circle('X_test', 'Y_test', line_color='colors_test_pred',
#                  size=12, alpha=1, line_width=3, fill_alpha=0,
#                  source=source_test)
#
#    # plot mesh
#    p_mesh = p.square('mesh_x', 'mesh_y', fill_color='colors_mesh',
#               size = 13, line_alpha=0, fill_alpha=0.05, 
#               source=source_mesh)
#    
#    # add hovertool
#    hover_1 = HoverTool(names=['Data'], 
#                        tooltips=[("truth", "@colors_legend"), ("prediction", "@colors_pred_data")], 
#                        renderers=[p_data])
#    p.add_tools(hover_1)
#
#    show(p)
#    
#    return