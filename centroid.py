#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import copy

import basenode
from randomtypes import (
  RandomBool,
  RandomInt,
  RandomFloat,
)

class CentroidAlgNode(basenode.BaseNode):
  '''Node class implementing centroid finding algorithm in a weighted tree
  
    The algorithm is described in the article
    "A self–stabilizing algorithm for finding weighted centroid in trees"
    by H. Bielak and M. Panczyk
    DOI: 10.2478/v10065-012-0035-x
  '''
  
  variables = {
    'W': lambda: collections.defaultdict(RandomFloat()),
    'w': RandomFloat(),
    'p': RandomInt(upper_bound=10),
  }

  def wCorrect(self):
    for j in self.neighbours:
      weight = self.w + sum(k.W[self.id] for k in self.neighbours-{j})
      if self.W[j.id] != weight:
        return False, j, weight
    return True, None, None

  def rule_1(self):
    correct, j, new_weight = self.wCorrect()
    if not correct:
      return_W = copy.copy(self.W)
      return_W[j.id] = new_weight
      return True, {'W': return_W}
    return False, {}

  def rule_2(self):
    correct, _, _ = self.wCorrect()
    if correct:
      neighbour = self.get_random_neighbour()
      half_tree_weight = (self.W[neighbour.id] + neighbour.W[self.id])/2.0
      if all(j.W[self.id] < half_tree_weight for j in self.neighbours):
        if self.p != self.id:
          return True, {'p': self.id}
    return False, {}
 
  def rule_3(self):
    correct, _, _ = self.wCorrect()
    if correct:
      neighbour = self.get_random_neighbour()
      half_tree_weight = (self.W[neighbour.id] + neighbour.W[self.id])/2.0
      for j in self.neighbours:
        if j.W[self.id] > half_tree_weight:
          if self.p != j.id:
            return True, {'p': j.id}
    return False, {}
    
  def rule_4(self):
    correct, _, _ = self.wCorrect()
    if correct:
      neighbour = self.get_random_neighbour()
      half_tree_weight = (self.W[neighbour.id] + neighbour.W[self.id])/2.0
      for j in self.neighbours:
        if j.W[self.id] == half_tree_weight:
          if self.id > j.id:
            if self.p != self.id:
              return True, {'p': self.id}
    return False, {}

  def rule_5(self):
    correct, _, _ = self.wCorrect()
    if correct:
      neighbour = self.get_random_neighbour()
      half_tree_weight = (self.W[neighbour.id] + neighbour.W[self.id])/2.0
      for j in self.neighbours:
        if j.W[self.id] == half_tree_weight:
          if self.id < j.id:
            if self.p != j.id:
              return True, {'p': j.id}
    return False, {}

def test_network():
  import basenetwork
  net = basenetwork.BaseNetwork()
  w1 = CentroidAlgNode(id=1, w=5)
  net += w1
  w2 = CentroidAlgNode(id=2, w=3, neighbours=[w1])
  w3 = CentroidAlgNode(id=3, w=2, neighbours=[w2])
  w4 = CentroidAlgNode(id=4, w=5, neighbours=[w2])
  w5 = CentroidAlgNode(id=5, w=4, neighbours=[w4])
  w6 = CentroidAlgNode(id=6, w=1, neighbours=[w5])
  w7 = CentroidAlgNode(id=7, w=10, neighbours=[w5])
  return net
