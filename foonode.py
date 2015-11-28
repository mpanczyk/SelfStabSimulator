#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import basenode
from randomtypes import (
  RandomInt,
  RandomBool,
)

class FooNode(basenode.BaseNode):
  '''Simple example subclass of the Node class'''
  
  variables = {
    'k': RandomInt,
    'yes': RandomBool,
    'yess': RandomBool,
  }

  def guard_1(self):
    return (
      self.k != 1,
      {
        'k': 1,
        'yes': False,
        'yess': False,
      }
    )

  def assignment_1(self, **kwargs):
    print('making a move')
    print('I got this kwargs: ' + str(kwargs))
    for k, v in kwargs.items():
      self.__setattr__(k, v)
