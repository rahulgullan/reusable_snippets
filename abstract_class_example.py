"""
This module exemplify the usage of abstract base class and factory pattern
"""
import csv
import os
import pandas as pd
from abc import abstractmethod


class StudentRecordParser:
    """
    This is the parent class, includes different methods encapsulate student data
    """
    def __init__(self, file_name:str):
        """
        Initialize attributes
        :param file_name: full path to student data file
        """
        self._file_spec = file_name
        self._student_data = []

    def get_students_data(self)->list:
        """
        Display a list of dictionaries contains student information
        :return: list of dictionaries
        """
        return self._student_data

    def get_records_by_student_name(self, name:str)->list:
        """
        This api returns student data by name
        :param name: full name of student
        :return: list of dictionaries
        """
        try:
            student_lists = [student_dict for student_dict in self._student_data if student_dict['name'].lower() == name.lower()]
            return student_lists
        except KeyError as err:
            print(f"Please check the input file has 'name' column")

    @abstractmethod
    def read_file(self):
        """
        This is is the abstract method defined in the child classes, do not call this method using parent class obj
        :return:
        """
        pass


class StudentXLSXRecordParser(StudentRecordParser):
    """
    This child class implements methods that are specific to file type of extension .xlsx
    """
    def read_file(self):
        """
        Read files of extension .xlsx into a list of dictionaries
        :return:
        """
        try:
            data = pd.read_excel(self._file_spec)
            self._student_data = data.to_dict("records")
        except Exception as err:
            print(err)

class StudentCSVRecordParser(StudentRecordParser):
    """
    This child class implements methods that are specific to file type of extension .csv
    """
    def read_file(self):
        """
        Read files of extension .csv into a list of dictionaries
        :return:
        """
        try:
            with open(self._file_spec) as f:
                self._student_data = [{key: value for key, value in row.items()}
                     for row in csv.DictReader(f, skipinitialspace=True)]
        except Exception as err:
            print(err
                  )
def student_record_factory(file_spec:str):
    """
    This method act as a factory method, it will instantiate the proper class based on the extension of input file
    :param file_spec:
    :return: Object of either StudentXLSXRecordParser or StudentCSVRecordParser
    """
    if os.path.basename(file_spec).split('.')[-1] == 'xlsx':
        return StudentXLSXRecordParser(file_spec)
    if os.path.basename(file_spec).split('.')[-1] == 'csv':
        return StudentCSVRecordParser(file_spec)


if __name__ == "__main__":

    # input either csv file or xlsx file
    input_file_name = 'student.csv'
    # input_file_name = 'student.xlsx'

    student_record = student_record_factory(input_file_name)
    student_record.read_file()
    sudent_data = student_record.get_students_data()
    student_list = student_record.get_records_by_student_name('Rahul M')
