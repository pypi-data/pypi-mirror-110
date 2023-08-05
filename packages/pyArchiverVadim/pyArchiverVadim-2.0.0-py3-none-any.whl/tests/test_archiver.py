from unittest import TestCase
import shutil
import filecmp
from os import getcwd, remove
from os.path import join
from pyArchiver.pyArchiver import to_zip, unzipping


class TestArchiver(TestCase):

    path_to_test = join(getcwd(), 'tests', 'for_test')

    def test_toZip_1(self):
        to_zip(join(self.path_to_test, 'vbieTest.zip'), [
            join(self.path_to_test, 'test_folder', 'vbie')
        ])

        with open(join(self.path_to_test, 'vbie.zip'), 'rb') as output, open(join(self.path_to_test, 'vbieTest.zip'), 'rb') as input:
            self.assertTrue(output.read() == input.read())


        remove(join(self.path_to_test, 'vbieTest.zip'))

    def test_toZip_2(self):
        to_zip(join(self.path_to_test, 'toZip2.zip'), [
            join(self.path_to_test, 'test_folder'),
            join(self.path_to_test, 'test_folder_2'),
            join(self.path_to_test, 'test_file_1.txt'),
        ])

        with open(join(self.path_to_test, 'toZip2.zip'), 'rb') as output, open(join(self.path_to_test, 'test_folder.zip'), 'rb') as input:
            self.assertTrue(output.read() == input.read())


        remove(join(self.path_to_test, 'toZip2.zip'))

    def test_unzipping_1(self):
        unzipping(join(self.path_to_test, 'vbie.zip'))

        output_dir = join(self.path_to_test, 'vbie')
        compare = filecmp.dircmp(output_dir, join(self.path_to_test, 'test_folder', 'vbie'))

        self.assertTrue(not len(compare.left_only) and not len(compare.right_only))

        shutil.rmtree(output_dir)
