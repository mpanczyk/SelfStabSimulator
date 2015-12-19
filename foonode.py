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

  def rule_1(self):
    return (
      self.k != 1,
      {
        'k': 1,
        'yes': False,
        'yess': False,
      }
    )
