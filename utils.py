#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import copy

def random_pick(sequence):
  '''Choose one rule amongst the active ones.
  '''
  return random.choice(sequence)

def updated_dict(d, *args):
  '''Return copy of a nested dictionary d
  with keys args[:-1] updated with value args[-1].
  For example: updated_dict(d, 'key1', 'key2', 'value')
  will return copy of d with d['key1']['key2']=='value'.
  '''
  if len(args) == 1:
    return args[0]
  d = copy.copy(d)
  d[args[0]] = updated_dict(d[args[0]], *args[1:])
  return d
