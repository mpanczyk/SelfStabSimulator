#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (
  QApplication,
  QWidget,
  QPushButton,
  QVBoxLayout,
  QHBoxLayout,
)
from PyQt5.QtGui import (
  QPainter,
  QBrush,
  QStandardItemModel,
  QStandardItem,
  QFont,
)
from PyQt5.QtCore import (
  Qt,
)
from PyQt5.QtWidgets import (
  QTreeView,
)

from utils import (
  diff_dict,
  formated_diff,
)
from basenode import (
  BaseNode,
)

def typeValueItem(value):
  typeFont = QFont()
  typeFont.setItalic(True)
  textList = [value.__class__.__name__]
  if hasattr(value, '__iter__'):
    if value:
      textList.append('({} items)'.format(str(len(value))))
    else:
      textList.append('(empty)')
  valueItem = QStandardItem(
    ' '.join(textList)
  )
  valueItem.setFont(typeFont)
  return valueItem

def scalarValueItem(value):
  valueFont = QFont()
  valueFont.setBold(True)
  valueItem = QStandardItem(
    '{} (type: {})'.format(
      str(value),
      value.__class__.__name__,
    )
  )
  valueItem.setFont(valueFont)
  return valueItem

def getItems(obj, level=0):
  exclude_keys = ('net', '_r', 'variables')
  retVal = []
  if level > 1 and isinstance(obj, BaseNode):
    return retVal
  if isinstance(obj, dict):
    for key, value in sorted(obj.items()):
      if key not in exclude_keys:
        keyItem = QStandardItem(str(key))
        children = []
        if hasattr(value, '__iter__'):
          valueItem = typeValueItem(value)
          for child in getItems(value, level+1):
            keyItem.appendRow(child)
        else:
          valueItem = scalarValueItem(value)
        retVal.append([keyItem, valueItem])
  elif hasattr(obj, '__dict__'):
    retVal = getItems(obj.__dict__, level+1)
  elif isinstance(obj, (set, list, tuple)):
    for item in sorted(obj):
      keyItem = QStandardItem(str(item))
      children = getItems(item, level+1)
      valueItem = typeValueItem(item)
      for child in children:
        keyItem.appendRow(child)
      retVal.append([keyItem, valueItem])
  return retVal


class VariablesView(QTreeView, object):
  def __init__(self, network, parent=None):
    super(VariablesView, self).__init__(parent)
    self.network = network
    self.redraw()

  def redraw(self):
    self.setModel(QStandardItemModel(self))
    for row in getItems(self.network):
      self.model().appendRow(row)
    self.expandAll()

class DrawArea(QWidget, object):

  def __init__(self, network, parent=None):
    super(DrawArea, self).__init__(parent)
    self.network = network

  def redraw(self):
    self.update()

  def paintEvent(self, event):
    painter = QPainter(self)
    painter.fillRect(
      painter.window(),
      QBrush(Qt.white),
    )
    painter.setRenderHint(QPainter.Antialiasing)
    self.network.draw( painter )


class MainWindow(QWidget, object):

  def __init__(self, network, parent=None):
    
    super(MainWindow, self).__init__(parent)
    
    self.setWindowTitle('Selfstabilising Systems Simulator')
    self.resize(1200, 1000)
    
    self.move_button = QPushButton("Move", self)
    self.move_button.clicked.connect(self.make_move)
    
    self.network = network
    self.drawArea = DrawArea(self.network, self)
    self.drawArea.resize(800, 600)
    self.variablesView = VariablesView(self.network.nodes, self)
    
    self.mainLayout = QHBoxLayout(self)
    self.mainLayout.addWidget(self.drawArea, 3)
    self.rightLayout = QVBoxLayout()
    self.mainLayout.addLayout(self.rightLayout, 3)
    self.rightLayout.addWidget(self.move_button)
    self.rightLayout.addWidget(self.variablesView)

  def make_move(self):
    status = self.network.move()
    for keys, values in formated_diff(
      diff_dict(
        status['prestate'].get_state(),
        status['poststate'].get_state(),
      )
    ):
      print('[{}]\t{}.{}: {}'.format(
        status['rule'],
        status['prestate'],
        '.'.join(str(key) for key in keys),
        ' -> '.join(str(value) for value in values),
      ))
    if self.network.is_stabilised():
      self.move_button.setEnabled( False )
    self.drawArea.redraw()
    self.variablesView.redraw()


def main():
  app = QApplication(sys.argv)
  import centroid
  network = centroid.test_network()
  w = MainWindow(network)
  w.show()
  return app.exec()

if __name__ == '__main__':
  main()
