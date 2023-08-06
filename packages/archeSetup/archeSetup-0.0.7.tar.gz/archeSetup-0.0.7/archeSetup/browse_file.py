"""
# -----------------------------------------------------------------------------
This python file or module " file_browse" created by
 RAMA KRISHNA REDDY DYAVA
# -----------------------------------------------------------------------------
Copyright (c) by ramadyava. All rights reserved.
Feature: This " browse_file " is used for
# -----------------------------------------------------------------------------
# Enter feature description here

# -----------------------------------------------------------------------------
Scenario: # Enter scenario name here
# Enter steps here
# -----------------------------------------------------------------------------
"""


import sys
import xml.dom.minidom
from PyQt5 import QtCore, QtGui, QtWidgets

class Browse():

    @staticmethod
    def xml_read(path, token):
        doc = xml.dom.minidom.parse(path)
        item = doc.getElementsByTagName(token)
        tag = item[0].getAttribute("name")
        return tag
    
    @staticmethod
    def xml_write(path, token, xml_val):
        doc = xml.dom.minidom.parse(path)
        item = doc.getElementsByTagName(token)
        lic = item[0].getAttribute("name")
        return lic

    @staticmethod
    def browse(file_filter):
        if file_filter == "csv":
            dlg = QtWidgets.QFileDialog()
            dlg.setNameFilters(["CSV Files (*.csv)"])

        elif file_filter == "log":
            dlg = QtWidgets.QFileDialog()
            dlg.setNameFilters(["Log Files (*.log)"])

        elif file_filter == "txt":
            dlg = QtWidgets.QFileDialog()
            dlg.setNameFilters(["Text Files (*.txt)"])

        else:
            dlg = QtWidgets.QFileDialog()
            dlg.setNameFilters(["Log Files (*.log)", "CSV Files (*.csv)", "Text Files (*.txt)"])

        filename = list()

        if dlg.exec_():
            filename = dlg.selectedFiles()

        file_name = ""
        file_name = file_name.join(filename)
        return file_name
    
    
    @staticmethod
    def browse_folder(file_filter):

        if file_filter == "folder":
            dlg_folder = QtWidgets.QFileDialog.getExistingDirectory()
            # filename_f = list()
            file_name = ""
            dlg_folder = str(dlg_folder)
            print("folder is:", dlg_folder)
            filename = dlg_folder + '/'
            file_name = file_name.join(filename)

        else:
            print("Please select the valid format")
            file_name = ""
        return file_name