from unittest import TestCase

from src.commandInterface.cdCommand import Cd
from src.commandInterface.commandExceptions import CommandExecutionError
from src.commandInterface.lsCommand import Ls
from src.commandInterface.pwdCommand import Pwd


class TestCommands(TestCase):
    def setUp(self) -> None:
        pass

    def test_cd(self):
        path = Pwd('', [])._invoke("")
        Cd('', ['test_dir'])._invoke('')
        Cd('', ['..'])._invoke('')
        self.assertEqual(path, Pwd('', [])._invoke(""))

        try:
            Cd('', ["bad path"])._invoke('')
            self.assertTrue(False)
        except CommandExecutionError as e:
            self.assertTrue(True)

    def test_ls(self):
        Cd('', ['test_dir'])._invoke('./test')
        self.assertEqual({"file1", "file2"}, set(Ls('', [])._invoke("").split('\n')))

        Cd('', ['..'])._invoke('')
        self.assertEqual({"file1", "file2"}, set(Ls('', ['test_dir'])._invoke("").split('\n')))

        try:
            Ls('', ["bad path"])._invoke('')
            self.assertTrue(False)
        except CommandExecutionError as e:
            self.assertTrue(True)

        self.assertEqual(Ls('', [])._invoke(''), Ls('', [Pwd('', [])._invoke('')])._invoke(''))
