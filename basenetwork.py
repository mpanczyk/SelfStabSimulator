#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import copy
from PyQt5.QtCore import (
  QRect,
)

import utils

class BaseNetwork(object):

  def __init__(self):
    self.nodes = set()

  def get_active_nodes(self):
    return [node for node in self.nodes if node.is_active()]

  def is_stabilised(self):
    return not self.get_active_nodes()

  def __iadd__(self, node):
    self.nodes.add(node)
    node.net = self
    return self

  def connect(self, node1, node2):
    for node in node1, node2:
      self.nodes.add(node)
    node1.connect(node2)

  def move(self):
    node = utils.random_pick( self.get_active_nodes() )
    info = {'prestate': copy.copy(node)}
    rule = node.move()
    info['rule'] = rule
    info['poststate'] = copy.copy(node)
    return info

  def run(self):
    while not self.is_stabilised():
      yield self.move()

  def draw_edge(self, painter, edge):
    node1, node2 = edge
    painter.drawLine(node1.centre(), node2.centre())

  def draw(self, painter):

    painter.setWindow( self.adjustedBoundingBox(painter) )

    # Edges drawing
    edges = {
      frozenset((node, neighbour))
      for node in self.nodes
      for neighbour in node.neighbours
    }
    for edge in edges:
      self.draw_edge(painter, edge)

    # Nodes drawing
    for node in self.nodes:
      node.draw(painter)

  def boundingBox(self):
    margin = 25
    mini_x = min(node._x for node in self.nodes)
    maxi_x = max(node._x for node in self.nodes)
    mini_y = min(node._y for node in self.nodes)
    maxi_y = max(node._y for node in self.nodes)
    width = maxi_x - mini_x
    height = maxi_y - mini_y
    return QRect(mini_x-margin, mini_y-margin, 2*margin+width, 2*margin+height)

  def adjustedBoundingBox(self, painter):
    boundingBox = self.boundingBox()
    bbRatio = boundingBox.height() / boundingBox.width()
    viewPort = painter.viewport()
    vpRatio = viewPort.height() / viewPort.width()
    if vpRatio > bbRatio:
      diff = boundingBox.width() * (vpRatio-bbRatio)
      boundingBox.adjust( 0, -diff/2, 0, diff/2)
    elif vpRatio < bbRatio:
      diff = boundingBox.height() * (1/vpRatio-1/bbRatio)
      boundingBox.adjust( -diff/2, 0, diff/2, 0 )
    return boundingBox
