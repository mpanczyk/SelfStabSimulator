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

def diff_dict(d0, d1):
  '''Return diff between two dictionaries
  in form of a dict with keys only for different values.
  The differences are inspected recursively
  (for values being another dictionaries)
  and respectively returned.
  '''
  diff = {}
  for key, value0 in d0.items():
    value1 = d1[key]
    if isinstance(value0, dict):
      diff_rek = diff_dict(value0, value1)
      if diff_rek:
        diff[key] = diff_rek
    elif value0 != value1:
      diff[key] = (value0, value1)
  return diff

def formated_diff(diff):
  '''Iterates over the diff_dict items
  and yields pairs:
    - array of keys with different value,
    - pair with former and actual value.
  '''
  for key, value in diff.items():
    if isinstance(value, dict):
      for rek_key, rek_value in formated_diff(value):
        yield ((key, rek_key), rek_value)
    else:
      yield key, value
