#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import copy

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

  def run(self):
    while not self.is_stabilised():
      node = utils.random_pick( self.get_active_nodes() )
      info = {'prestate': copy.copy(node)}
      node.move()
      info['poststate'] = copy.copy(node)
      yield info
