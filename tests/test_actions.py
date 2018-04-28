import filecmp
import os
import unittest

from scripts import actions, settings

TEST = 'test'
settings.BASE_DIR = TEST  # taking files from 'test' folder


class Test_actions(unittest.TestCase):
    def test_check_mydxfs(self):
        # testing whole result
        test = os.path.abspath(os.path.join(TEST, 'formatted.txt'))
        sample_dir = test.replace(TEST, 'test_sample')
        mydxf_dir = os.path.abspath(os.path.join(TEST, 'mydxf'))

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
        self.assertTrue(filecmp.cmp(test, sample_dir))  # testing


if __name__ == '__main__':
    unittest.main()
