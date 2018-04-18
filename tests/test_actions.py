import filecmp
import os
import unittest

from scripts import settings, actions

settings.BASE_DIR = 'test'  # taking files from 'test' folder


class Test_actions(unittest.TestCase):
    def test_check_mydxfs(self):
        # testing whole result
        test = 'test\\formatted.txt'
        sample = test.replace('test', 'test_sample')
        mydxf_dir = 'test\\mydxf'

        # deleting all results files
        for f in os.listdir(mydxf_dir):
            if f.endswith('.txt'):
                try:
                    os.remove(os.path.join(mydxf_dir, f))
                except Exception:
                    pass
        try:
            os.remove(test)
        except Exception:
            pass

        actions.check_mydxfs()  # creating new check results
        self.assertTrue(filecmp.cmp(test, sample))  # testing


if __name__ == '__main__':
    unittest.main()
