from unittest import TestCase
import filecmp
import os.path

class dircmp(filecmp.dircmp):
    """
    Compare the content of dir1 and dir2. In contrast with filecmp.dircmp, this
    subclass compares the content of files with the same path.
    """
    def phase3(self):
        """
        Find out differences between common files.
        Ensure we are using content comparison with shallow=False.
        """
        fcomp = filecmp.cmpfiles(self.left, self.right, self.common_files,
                                 shallow=False)
        self.same_files, self.diff_files, self.funny_files = fcomp

def is_same(dir1, dir2):
    """
    Compare two directory trees content.
    Return False if they differ, True is they are the same.
    """
    compared = dircmp(dir1, dir2)
    if (compared.left_only or compared.right_only or compared.diff_files
        or compared.funny_files):
        return False
    for subdir in compared.common_dirs:
        if not is_same(os.path.join(dir1, subdir), os.path.join(dir2, subdir)):
            return False
    return True

class TestPython(TestCase):
    def test_demo1(self):
        from setup_test_files import setup, setup_keep
        setup("demo1", "demo1_tmp")
        report = filecmp.dircmp("demo1_correct", "demo1_tmp")
        print("Different", report.report())
        self.assertTrue(is_same("demo1_correct", "demo1_tmp"))

    def test_demo2(self):
        from setup_test_files import setup, setup_keep
        setup_keep("demo2/framework.py", "demo2/framework_tmp.txt")
        with open("demo2/framework_tmp.txt") as f:
            tmp = f.read()

        with open("demo2/framework_correct.txt") as f:
            correct = f.read()

        self.assertEqual(tmp, correct)
