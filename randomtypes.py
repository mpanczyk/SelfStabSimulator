#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

MAX_RAND_INT = 2**31
MAX_RAND_FLOAT = 300.0

class RandomInt(int):
  def __new__(T, n=None):
    if n is None:
      n = MAX_RAND_INT
    value = random.randint(0, MAX_RAND_INT)
    return int.__new__(T, value)

class RandomBool(int):
  def __new__(T):
    return int.__new__(T, random.randint(0, 1))

class RandomFloat(float):
  def __new__(T, max=MAX_RAND_FLOAT):
    value = random.random()*max
    return float.__new__(T, value)
