from subprocess import PIPE, Popen
from unittest import TestCase

from dead_code.cli import main


class DeadCodeTests(TestCase):
    def test_main(self):
        self.assertIsNone(main())


class DetectUnimportedDefinitionInRoot(TestCase):
    def test_run_dead_code_finder_with_a_subprocess_in_a_right_directory_main(self):
        main(["tests/test_case1"])

    # def testrun_dead_code_finder_with_a_subprocess_in_a_right_directory(self):
    #     result = Popen(["../venv/bin/dead-code-finder", "tests/test_case1"], stdout=PIPE).communicate()[0].decode()
