#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
from functools import (
  total_ordering,
)
from PyQt5.QtCore import (
  QPoint,
)
from PyQt5.QtGui import (
  QBrush,
  QColor,
)

from randomtypes import (
  RandomInt,
  RandomBool,
)
import utils

@total_ordering
class BaseNode(object):
  '''Abstract class representing a node in a self-stabilising system.
     
     Its subclasses ought to implement a self-stabilising algorithm
     by implementing methods 'rule_*', for example 'rule_1'.

     A 'rule_x' should return a pair:
      - bool - True if the guard of the rule evaluates to True,
      - dict - dictionary with variable names as keys
               and their new values as the dict values.
  '''

  def __init__(self, **kwargs):

    self.id = uuid.uuid4()
    self.net = None
    self._r = 10

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
    return '{}({})'.format(self.__class__.__name__, self.id)

  def __le__(self, other):
    return self.id <= other.id

  def connect(self, other):
    self.neighbours.add(other)
    other.neighbours.add(self)
    if self.net is None:
      self.net = other.net
    if other.net is None:
      other.net = self.net
    assert self.net is other.net
    if self.net is not None:
      self.net.nodes.add(self)
      self.net.nodes.add(other)

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
      method_name[5:]
      for method_name
      in dir(klass)
      if method_name.startswith('rule_')
    ]
    if not names:
      raise NotImplementedError(
        'You must implement at least one rule in the {} class.'.format(
          klass.__name__,
        )
      )
    return names

  def get_rule(self, name):
    return self.__getattribute__('rule_' + name)

  def get_active_rules(self):
    return [
      name
      for name in self.get_rule_names()
      if self.get_rule(name)()[0]
    ]

  def assign(self, **kwargs):
    '''Assign new values to the node's variables.
       This way a node may change its state.
    '''
    self.__dict__.update(kwargs)

  def move(self):
    '''Pick up a random active rule in the node
       and make a move according to its assignment.
    '''
    active_rule_names = self.get_active_rules()
    assert active_rule_names, 'There is no active rule in the node.'
    rule_name = utils.random_pick(active_rule_names)
    is_active, variables = self.get_rule(rule_name)()
    assert is_active
    self.assign(**variables)
    return rule_name

  def get_state(self):
    return {var: self.__getattribute__(var) for var in self.variables}

  def get_random_neighbour(self):
    return utils.random_pick(list(self.neighbours))

  def centre(self):
    return QPoint(self._x, self._y)

  def get_color(self):
    if self.is_active():
      return QColor(0x1f, 0xff, 0x1f)
    return QColor(0x8f, 0x8f, 0x8f)

  def get_radius(self):
    return self._r

  def set_radius(self, r):
    self._r = r

  radius = property(get_radius, set_radius)

  def draw(self, painter):
    painter.setBrush(QBrush(self.get_color()))
    painter.drawEllipse(
      self.centre(),
      self.radius,
      self.radius,
    )
