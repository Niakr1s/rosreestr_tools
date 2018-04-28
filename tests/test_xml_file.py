import unittest

from scripts.xml_file import XmlFile


class Test_XmlFile(unittest.TestCase):
    def test_get_rect(self):

        xml = XmlFile('tests\\test\\xml\\KPT CadastralBlock 21 02 010106.xml')
        print(xml.parcels['21:02:010106'])
        etalon = {
            'xmax': 408584.98,
            'xmin': 407769.54,
            'ymax': 1248481.90,
            'ymin': 1246008.09,
        }
        self.assertDictEqual(
            etalon, xml.parcels['21:02:010106']['rect'])  # testing


if __name__ == '__main__':
    unittest.main()
