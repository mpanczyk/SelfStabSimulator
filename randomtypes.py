#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

MAX_RAND_INT = 2**31

class RandomInt(int):
  def __new__(T, n=None):
    if n is None:
      n = MAX_RAND_INT
    value = random.randint(0, MAX_RAND_INT)
    return int.__new__(T, value)

class RandomBool(int):
  def __new__(T):
    return int.__new__(T, random.randint(0, 1))
