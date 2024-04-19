'''
Created on Apr 19, 2024

@author: oqb
'''
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys

#To create window, create classes.... could probably be outsourced
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Undulator Analysis HZB')
        
        button = QPushButton('Go on then!')
        
        #self.setFixedSize(QSize(400,300))
        
        self.setMinimumSize(QSize(100, 100))
        self.setMaximumSize(QSize(400,400))
        
        
        
        self.setCentralWidget(button)



#This bit is the running of the app
app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec()

print('I am here')