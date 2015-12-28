#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

MAX_RAND_INT = 2**31
MAX_RAND_FLOAT = 300.0

class RandomType(object):
  pass

def RandomInt(upper_bound=MAX_RAND_INT):
  class ClassRandomInt(int, RandomType):
    def __new__(T):
      value = random.randint(0, upper_bound)
      return int.__new__(T, value)
  ClassRandomInt.__name__ = 'RandomInt'
  return ClassRandomInt

def RandomBool():
  class ClassRandomBool(int, RandomType):
    def __new__(T):
      return int.__new__(T, random.randint(0, 1))
    def __repr__(self):
      return 'True' if self else 'False'
  ClassRandomBool.__name__ = 'RandomBool'
  return ClassRandomBool

def RandomFloat(upper_bound=MAX_RAND_FLOAT):
  class ClassRandomFloat(float, RandomType):
    def __new__(T):
      value = random.random()*upper_bound
      return float.__new__(T, value)
  ClassRandomFloat.__name__ = 'RandomFloat'
  return ClassRandomFloat
