#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (
  QApplication,
  QWidget,
  QMainWindow,
  QPushButton,
  QLabel,
  QVBoxLayout,
)
from PyQt5.QtGui import (
  QIcon,
  QPainter,
  QBrush,
  QColor,
)
from PyQt5.QtCore import (
  QStateMachine,
  QState,
)

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
      QBrush(QColor(0xff, 0xff, 0xff))
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
    
    self.layout = QVBoxLayout(self)
    self.layout.addWidget(self.move_button)
    self.layout.addWidget(self.drawArea)

  def make_move(self):
    self.network.move()
    if self.network.is_stabilised():
      self.move_button.setEnabled( False )
    self.drawArea.redraw()


def main():
  app = QApplication(sys.argv)
  import centroid
  network = centroid.test_network()
  w = MainWindow(network)
  w.show()
  return app.exec()

if __name__ == '__main__':
  main()
