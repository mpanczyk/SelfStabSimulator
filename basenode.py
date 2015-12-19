#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import uuid
from randomtypes import (
  RandomInt,
  RandomBool,
)

class BaseNode(object):
  '''Abstract class representing a node in a self-stabilising system.
     
     Its subclasses ought to implement a self-stabilising algorithm
     by implementing methods 'guard_*' and 'assignment_*'
     with corresponding suffixes in their names,
     forming together a rule with the name as the suffix.
     For example 'guard_1' and 'assignment_1'
     form together a rule '1'.
     For every 'guard_x' should exists 'assignment_x' and vice versa.

     A 'guard_x' should return a pair:
      - bool - True if the guard evaluates to True,
      - dict - dictionary with temporary variable names as keys
               and their values as the dict values.
  '''

  def __init__(self, **kwargs):

    self.id = uuid.uuid4()

    self.neighbours = set()
    for neighbour in kwargs.pop('neighbours', ()):
      self.connect(neighbour)

    self.variables = set(('id',))
    for var, val in kwargs.items():
      self.__setattr__(var, val)
      self.variables.add(var)
    for var, type_ in self.__class__.variables.items():
      if var not in self.__dict__:
        self.__setattr__(var, type_())
        self.variables.add(var)

  def __repr__(self):
    return self.__class__.__name__ +\
            '(' +\
              ', '.join('{}={}'.format(var, repr(val)) for var, val in self.get_state().items()) +\
            ')'

  def connect(self, other):
    if other not in self.neighbours:
      self.neighbours.add(other)
    if self not in other.neighbours:
      other.neighbours.add(self)

  def disconnect(self, other):
    if other in self.neighbours:
      self.neighbours.remove(other)
    if self in other.neighbours:
      other.neighbours.remove(self)

  def is_active(self):
    '''Check if there exists any active rule in the node.
    '''
    return bool(self.get_active_rules())

  @classmethod
  def get_rule_names(klass):
    names = [
      method_name[6:]
      for method_name
      in dir(klass)
      if method_name.startswith('guard_')
    ]
    if not names:
      raise NotImplementedError(
        'You must implement at least one rule in the {} class.'.format(
          klass.__name__,
        )
      )
    return names

  def get_guard(self, name):
    return self.__getattribute__('guard_' + name)

  def get_assignment(self, name):
    return self.__getattribute__('assignment_' + name)

  def get_active_rules(self):
    return [
      name
      for name in self.get_rule_names()
      if self.get_guard(name)()[0]
    ]

  @staticmethod
  def pick(items):
    '''Choose one rule amongst the active ones.'''
    return random.choice(items)

  def move(self):
    '''Pick up a random active rule in the node
       and make a move according to its assignment.
    '''
    active_rule_names = self.get_active_rules()
    assert active_rule_names, 'There is no active rule in the node.'
    rule_name = self.pick(active_rule_names)
    is_active, variables = self.get_guard(rule_name)()
    assert is_active
    assignment = self.get_assignment(rule_name)
    assignment(**variables)

  def get_state(self):
    return {var: self.__getattribute__(var) for var in self.variables}

