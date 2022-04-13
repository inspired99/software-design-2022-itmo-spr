import os
from unittest import TestCase

from src.bash.bash import CommandLine
from src.commandInterface.catCommand import Cat
from src.commandInterface.cdCommand import Cd
from src.commandInterface.commandExceptions import FlagError
from src.commandInterface.echoCommand import Echo
from src.commandInterface.exitCommand import Exit
from src.commandInterface.lsCommand import Ls
from src.commandInterface.pwdCommand import Pwd
from src.commandInterface.wcCommand import Wc


class TestCommands(TestCase):
    def setUp(self) -> None:
        self.bash = CommandLine

        self.cat = Cat
        self.pwd = Pwd
        self.exit = Exit
        self.echo = Echo
        self.wc = Wc
        self.cd = Cd
        self.ls = Ls

    def test_main(self) -> None:
        self.assertTrue(self.bash())

    def test_pwd(self) -> None:
        self.assertEqual(self.pwd.invoke(), os.getcwd())

    def test_cat(self) -> None:
        self.assertEqual(self.cat.invoke('test/test_files/cat_test_1.txt'), 'Cat test number 1 passed! Success!\n')
        self.assertEqual(self.cat.invoke('test/test_files/cat_test_2.txt'),
                         """Read from absolute path! \nSuccess!\n""")
        self.assertEqual(self.cat.invoke('-n test/test_files/cat_test_3.txt'),
                         """1 this are real numbers of lines:\n2 2\n3 3\n4 4\n5 5\n6 6\n""")
        self.assertEqual(self.cat.invoke('-s test/test_files/cat_test_4.txt'),
                         'next line should be omitted:\nSuccess!\n')

        with self.assertRaises(FlagError):
            self.cat.invoke('arg1 -n')
            self.cat.invoke('-f arg1')
            self.cat.invoke('-s -n args')

    def test_exit(self) -> None:
        with self.assertRaises(SystemExit):
            self.exit.invoke()

    def test_echo(self) -> None:
        self.assertEqual(self.echo.invoke('a'), 'a')
        self.assertEqual(self.echo.invoke('echo test'), 'echo test')

    def test_wc(self) -> None:
        self.assertEqual(self.wc.invoke('test/test_files/wc_test_1.txt'), '3 6 27  wc_test_1.txt\n')
        self.assertEqual(self.wc.invoke('test/test_files/wc_test_1.txt test/test_files/wc_test_2.txt'),
                         '3 6 27  wc_test_1.txt\n 3 6 27  wc_test_2.txt\n')
        self.assertEqual(self.wc.invoke('-l test/test_files/wc_test_1.txt'), '3 wc_test_1.txt \n')
        self.assertEqual(self.wc.invoke('-w test/test_files/wc_test_1.txt'), '6 wc_test_1.txt \n')
        self.assertEqual(self.wc.invoke('-c test/test_files/wc_test_1.txt'), '27 wc_test_1.txt \n')

        with self.assertRaises(FlagError):
            self.wc.invoke('-f arg')
            self.wc.invoke('arg -l')

    def test_cd(self):
        path = self.pwd.invoke('')

        self.cd.invoke('test/test_files')
        self.assertTrue(self.pwd.invoke('').endswith('test_files'))
        self.cd.invoke('../..')

        self.assertEqual(path, self.pwd.invoke(''))
        self.cd.invoke('')

        self.assertEqual(path, self.pwd.invoke(''))
        self.cd.invoke(self.pwd.invoke(''))

        self.assertEqual(path, self.pwd.invoke(''))

        try:
            self.cd.invoke('bad path')
            self.assertTrue(False)
        except RuntimeError:
            self.assertTrue(True)

    def test_ls(self):
        self.cd.invoke('./test/test_files/test_ls')
        self.assertEqual({'file1', 'file2'}, set(self.ls.invoke('').split('\n')))
        self.cd.invoke('../../..')

        self.assertEqual({"file1", "file2"}, set(self.ls.invoke('test/test_files/test_ls').split('\n')))

        try:
            self.ls.invoke('bad path')
            self.assertTrue(False)
        except RuntimeError:
            self.assertTrue(True)

        self.assertEqual(self.ls.invoke(''), self.ls.invoke(Pwd.invoke('')))

    def test_pipelines(self) -> None:
        test_bash = CommandLine()
        self.assertEqual(test_bash.run('echo a | echo b | echo c'), 'c')
        self.assertEqual(test_bash.run('echo test/test_files/wc_test_1.txt | wc'), '3 6 27  wc_test_1.txt\n')
        self.assertEqual(test_bash.run('echo test/test_files/cat_test_1.txt | cat'),
                         'Cat test number 1 passed! Success!\n')

        with self.assertRaises(SystemExit):
            test_bash.run('wc test/test_files/wc_test_1.txt | exit')
            test_bash.run('pwd | echo')

    def test_subst(self) -> None:
        test_bash = CommandLine()
        test_bash.run('a=6')
        test_bash.run('b=2')
        test_bash.run('let x=test/test_files/wc_test_1.txt')
        self.assertEqual(test_bash.run('echo $a'), '6')
        self.assertEqual(test_bash.run('echo $b'), '2')
        self.assertEqual(test_bash.run('echo $a | echo $b'), '2')
        self.assertEqual(test_bash.run('echo $x | wc'), '3 6 27  wc_test_1.txt\n')
