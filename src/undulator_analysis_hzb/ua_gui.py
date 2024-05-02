'''
Created on Apr 19, 2024

@author: oqb
'''
import sys

import undulator_analysis_hzb.field_analysis as fa

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QMessageBox,
    QFileDialog, 
    QLineEdit,
    QGridLayout,
    QComboBox
)

class MainWindow(QMainWindow):

    def __init__(self):
        #Initialise the upsercalss
        super().__init__()
        
        #set required variables to None
        self.raw_data_folder_path = None
        self.proc_data_file_path = None
        self.component = None
        self.ident = None
        self.meas_state = None
        self.step_number = None
        self.meas_type = None
        
        
        #set the window title
        self.setWindowTitle("HZB: Magnetic Measurement Analysis")
        
        #set a simple vertical layout
        layout = QGridLayout()
        
        #Find folder containing data to be analysed
        self.select_raw_data_folder_button = QPushButton("Select Data Folder For Analysis")
        self.select_raw_data_folder_button.clicked.connect(self.select_raw_data_folder)
        
        #Display folder containing data to be analysed
        self.raw_data_folder_line_edit = QLineEdit()
        self.raw_data_folder_line_edit.setFixedWidth(500)
        self.raw_data_folder_line_edit.textEdited.connect(self.set_raw_data_folder)
        
        #Find file for results to be targeted
        self.select_processed_data_file_button = QPushButton("Select Processed Data File")
        self.select_processed_data_file_button.clicked.connect(self.select_processed_data_file)
        
        #Display filepath for results file
        self.processed_data_file_line_edit = QLineEdit()
        self.processed_data_file_line_edit.setFixedWidth(500)
        self.processed_data_file_line_edit.textEdited.connect(self.set_processed_data_file)
        
        #Label and LineEdit for Component Name
        self.component_name_label = QLabel('Enter Component Name')
        self.component_name_line_edit = QLineEdit()
        self.component_name_line_edit.setFixedWidth(250)
        self.component_name_line_edit.textEdited.connect(self.update_component)
        
        #Label and Line Edit for Ident Name
        self.ident_name_label = QLabel('Enter Ident Name')
        self.ident_name_line_edit = QLineEdit()
        self.ident_name_line_edit.setFixedWidth(250)
        self.ident_name_line_edit.textEdited.connect(self.update_ident)
        
        #Label and Line Edit for State Name
        self.state_name_label = QLabel('Enter State of Component')
        self.state_name_line_edit = QLineEdit()
        self.state_name_line_edit.setFixedWidth(250)
        self.state_name_line_edit.textEdited.connect(self.update_state)
        
        #Label and Line Edit for Step Number
        self.step_number_label = QLabel('Enter Measurement Step (integer)')
        self.step_number_line_edit = QLineEdit()
        self.step_number_line_edit.setFixedWidth(250)
        self.step_number_line_edit.textEdited.connect(self.update_step_number)
        
        #Combo Box to choose measurement type
        self.meas_type_label = QLabel('Choose the Measurement Equipment Used')
        self.meas_type_cbox = QComboBox()
        self.meas_type_cbox.addItems(['Granit Messbank', 'Moved Wire'])
        #TODO - suggest current measurement type
        #self.meas_type_cbox.setCurrentIndex(0)
        self.meas_type_cbox.setFixedWidth(250)
        self.meas_type_cbox.activated.connect(self.update_meas_type)
        
        
        #Button to trigger analysis
        self.button = QPushButton("Analyse Measurement")
        self.button.clicked.connect(self.process_measurement)
        
        

        
        #Message
        self.label = QLabel("Waiting for Processing")

        

        layout.addWidget(self.select_raw_data_folder_button,0,0)
        layout.addWidget(self.raw_data_folder_line_edit,0,1)
        layout.addWidget(self.select_processed_data_file_button,1,0)
        layout.addWidget(self.processed_data_file_line_edit,1,1)
        
        layout.addWidget(self.component_name_label,2,0)
        layout.addWidget(self.component_name_line_edit,2,1)
        
        layout.addWidget(self.ident_name_label,3,0)
        layout.addWidget(self.ident_name_line_edit,3,1)
        
        layout.addWidget(self.state_name_label,4,0)
        layout.addWidget(self.state_name_line_edit,4,1)
        
        layout.addWidget(self.step_number_label,5,0)
        layout.addWidget(self.step_number_line_edit,5,1)
        
        layout.addWidget(self.meas_type_label,6,0)
        layout.addWidget(self.meas_type_cbox,6,1)
        
        layout.addWidget(self.button,7,0,1,2)
        layout.addWidget(self.label,8,0,1,2)
        
        widget = QWidget()
        
        widget.setLayout(layout)
        
        self.setCentralWidget(widget)
        
    def process_measurement(self):
        if self.meas_type == 'Granit Messbank':
            self.status = fa.process_granit_bank(self.raw_data_folder_path,
                                                 self.proc_data_file_path[0], 
                                                 self.component, 
                                                 self.ident,
                                                 self.meas_state,
                                                 self.step_number )
        elif self.meas_type == 'Moved Wire':
            self.status = fa.process_moved_wire(self.raw_data_folder_path,
                                                 self.proc_data_file_path[0], 
                                                 self.component, 
                                                 self.ident,
                                                 self.meas_state,
                                                 self.step_number )
            
        self.label.setText('{} {}'.format(self.raw_data_folder_line_edit.text(),self.status))
        
    def select_raw_data_folder(self):
        self.raw_data_folder_path = QFileDialog.getExistingDirectory(self, 'Select a Measurement Data Folder','D:/UE51/UE51 Measurements')
        self.raw_data_folder_line_edit.setText(self.raw_data_folder_path)
        
    def set_raw_data_folder(self):
        self.raw_data_folder_path = self.raw_data_folder_line_edit.text()
        
    def select_processed_data_file(self):
        self.proc_data_file_path = QFileDialog.getOpenFileName(self,'Select a Processed Data File', 'D:/UE51/UE51 Measurements',"HDF5 Files (*.h5)")
        self.processed_data_file_line_edit.setText(self.proc_data_file_path[0])
        
    def set_processed_data_file(self):
        self.proc_data_file_path = (self.processed_data_file_line_edit.text(),self.proc_data_file_path[1])
        
    def update_component(self):
        self.component = self.component_name_line_edit.text()
        
    def update_ident(self):
        self.ident = self.ident_name_line_edit.text()
        
    def update_state(self):
        self.meas_state = self.state_name_line_edit.text()
    
    def update_step_number(self):
        self.step_number = self.step_number_line_edit.text()
        
    def update_meas_type(self):
        self.meas_type = self.meas_type_cbox.currentText()

#This bit is the running of the app
app = QApplication(sys.argv)

#create the main window
window = MainWindow()

#show the window
window.show()

#begin the action loop
app.exec()

#once closed, you're outta here
print('I am here https://www.pythonguis.com/tutorials/pyqt6-layouts/')