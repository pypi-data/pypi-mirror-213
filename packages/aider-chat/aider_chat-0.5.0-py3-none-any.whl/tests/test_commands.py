import os
import shutil
import tempfile
from unittest import TestCase
from unittest.mock import patch

from aider.commands import Commands
from aider.io import InputOutput


class TestCommands(TestCase):
    def setUp(self):
        self.original_cwd = os.getcwd()
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)

        self.patcher = patch("aider.coder.Coder.check_model_availability")
        self.mock_check = self.patcher.start()
        self.mock_check.return_value = True

    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.tempdir)

        self.patcher.stop()

    def test_cmd_add(self):
        # Initialize the Commands and InputOutput objects
        io = InputOutput(pretty=False, yes=True)
        from aider.coder import Coder

        coder = Coder(io, openai_api_key="deadbeef")
        commands = Commands(io, coder)

        # Call the cmd_add method with 'foo.txt' and 'bar.txt' as a single string
        commands.cmd_add("foo.txt bar.txt")

        # Check if both files have been created in the temporary directory
        self.assertTrue(os.path.exists("foo.txt"))
        self.assertTrue(os.path.exists("bar.txt"))
