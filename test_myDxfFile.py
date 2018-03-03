from os import path
from unittest import TestCase

from my_dxf_file import MyDxfFile
from settings import Settings
from xml_file import get_list_of_XmlFiles


class TestMyDxfFile(TestCase):
    def test_1(self):
        settings = Settings()
        settings.settings['xml_folder_path'] = path.abspath('tests\\testchecks\\test1')
        my = MyDxfFile('tests\\testchecks\\test1\\test1.dxf', settings)
        XmlFiles = get_list_of_XmlFiles(settings)
        my.geometry_checks(XmlFiles)  # This function updates XmlFiles.check
        etalon = {'21:02:010614'}
        results = my.get_checks(XmlFiles)
        results = {number for numbers in results.values() for number in numbers}
        self.assertEqual(etalon, results)

    def test_2(self):
        settings = Settings()
        settings.settings['xml_folder_path'] = path.abspath('tests\\testchecks\\test2')
        my = MyDxfFile('tests\\testchecks\\test2\\test2.dxf', settings)
        XmlFiles = get_list_of_XmlFiles(settings)
        my.geometry_checks(XmlFiles)  # This function updates XmlFiles.check
        etalon = {'21:02:010614', '21:02:010614:145'}
        results = my.get_checks(XmlFiles)
        results = {number for numbers in results.values() for number in numbers}
        self.assertEqual(etalon, results)

    def test_3(self):
        settings = Settings()
        settings.settings['xml_folder_path'] = path.abspath('tests\\testchecks\\test2')
        my = MyDxfFile('tests\\testchecks\\test3\\test3.dxf', settings)
        XmlFiles = get_list_of_XmlFiles(settings)
        my.geometry_checks(XmlFiles)  # This function updates XmlFiles.check
        etalon = {'21:02:010614', '21:02:010614:211', '21:02:010614:128', '21:02:010614:225', '21:02:010614:129',
                  '21:02:010614:145'}
        results = my.get_checks(XmlFiles)
        results = {number for numbers in results.values() for number in numbers}
        self.assertEqual(etalon, results)

    def test_4(self):
        settings = Settings()
        settings.settings['xml_folder_path'] = path.abspath('tests\\testchecks\\test2')
        my = MyDxfFile('tests\\testchecks\\test4\\test4.dxf', settings)
        XmlFiles = get_list_of_XmlFiles(settings)
        my.geometry_checks(XmlFiles)  # This function updates XmlFiles.check
        etalon = {'21:02:010614', '21:02:010614', '21:02:010614:169', '21:02:010614', '21:02:010614:150',
                  '21:02:010614:338'}
        results = my.get_checks(XmlFiles)
        results = {number for numbers in results.values() for number in numbers}
        self.assertEqual(etalon, results)
