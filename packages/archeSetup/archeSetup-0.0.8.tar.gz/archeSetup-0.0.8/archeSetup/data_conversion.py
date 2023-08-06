"""
# -----------------------------------------------------------------------------
This python file or module " example" created by
 RAMA KRISHNA REDDY DYAVA on 07-01-2023 and 11:43
# -----------------------------------------------------------------------------
Copyright (c) by Rama Krishna. All rights reserved.
Feature: This " data_conversion " is used for
# -----------------------------------------------------------------------------
# Enter feature description here

# -----------------------------------------------------------------------------
Scenario: # Enter scenario name here
# Enter steps here
# -----------------------------------------------------------------------------
"""

import os
import pandas as pd
from datetime import date, datetime, timedelta

from . browse_file import *
from os import mkdir,path,getcwd


class DataConversion(Browse):

    def __int__(self):
        self.value = "conversion"

    @staticmethod
    def convert_to_csv(log_path, frame_extract, prefix_txt, suffix_txt, store_path_main, file_type):

        """
        The convert_to_csv method is willing to convert to csv files from log/txt files
        This emthods needs total 6 agruments are follows:
        1) log/txt file path
        2) String frame to extract and should separator by colon (:)
        3) prefix_txt = data file to be saved with this prefix
        4) suffix_txt = data file to be saved with this sufix,
        5) store_path = storage path of the final csv/txt file
        6) type = which type of conversion is needed example "CSV"

        """

        conversion_type = file_type
        testing_data = []
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("_%d_%m_%H_%M")
        # print("time is:  ",dt_string)

        file_name = str(prefix_txt + dt_string)
        file_path = log_path
        if file_path == "":
            print("Please select the suitable format or file")
        else:
            print("ok")
            datastore1 = open(file_path, 'r')
            print("reading")

            data_out = []
            data_extract1 = frame_extract

            ##########################
            if data_extract1 == "":
                print("Please enter the valid data extract line ")

            else:
                for line in datastore1:
                    if line.split(':')[0] == data_extract1:
                        data_out.append(line.split(':')[1])

                print(data_out[10])
            ##########################



        store_path = store_path_main
        print(store_path)
        file_pos = open(store_path + file_name + suffix_txt + ".txt", 'w')
        file_pos.writelines(data_out)
        file_pos.close()
        value = 1
        if value == 1:
            if conversion_type == "CSV File" and suffix_txt == "_g":
                print("the type is:: ", conversion_type)
                file_pos2 = pd.read_csv(store_path + file_name + suffix_txt + ".txt", delimiter=' ')
                file_pos2.to_csv(store_path + file_name + suffix_txt + ".csv")

            if conversion_type == "CSV File" and ((suffix_txt == "_p") or (suffix_txt == "_t")):
                print("the type is:: ", conversion_type)
                file_pos2 = pd.read_csv(store_path + file_name + suffix_txt + ".txt", delimiter=',')
                file_pos2.to_csv(store_path + file_name + suffix_txt + ".csv")
        else:
            print("the type is:: ", conversion_type)
            file_pos2 = pd.read_csv(store_path + file_name + suffix_txt + ".txt", delimiter=',')
            file_pos2.to_csv(store_path + file_name + suffix_txt + ".csv")


        return data_out
    
    @staticmethod
    def create_folder(store_path_main,prefix_txt):

        testing_data = []
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("_%d_%m_%H_%M")
        # print("time is:  ",dt_string)

        file_name = str(prefix_txt + dt_string)
        print("working")
        path =os.path.join(store_path_main,file_name)
        os.mkdir(path)
        store_path_test = path+'/'
        print("the path final ", store_path_test)

        return store_path_test
        # store_path =store_path_test
