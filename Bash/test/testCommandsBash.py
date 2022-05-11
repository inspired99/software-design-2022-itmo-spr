import os
from unittest import TestCase

from src.bash.bash import CommandLine
from src.commandInterface.catCommand import Cat
from src.commandInterface.commandExceptions import FlagError
from src.commandInterface.echoCommand import Echo
from src.commandInterface.exitCommand import Exit
from src.commandInterface.externalCommand import ExternalCommand
from src.commandInterface.pwdCommand import Pwd
from src.commandInterface.wcCommand import Wc


class TestCommands(TestCase):
    def setUp(self) -> None:
        self.test_bash = CommandLine()
        self.bash = CommandLine

        self.cat = Cat
        self.pwd = Pwd
        self.exit = Exit
        self.echo = Echo
        self.wc = Wc

    def test_main(self) -> None:
        self.assertTrue(self.bash())

    def test_pwd(self) -> None:
        self.assertEqual(self.pwd.invoke(), os.getcwd())

    def test_cat(self) -> None:
        self.assertEqual(self.cat.invoke([os.path.dirname(__file__) + '/test_files/cat_test_1.txt']),
                         'Cat test number 1 passed! Success!')
        self.assertEqual(
            self.cat.invoke([f'-n', f'{os.path.dirname(__file__)}/test_files/cat_test_3.txt']),
            """1 this are real numbers of lines:\n2 2\n3 3\n4 4\n5 5\n6 6\n""")
        self.assertEqual(self.cat.invoke(['-s', f'{os.path.dirname(__file__)}/test_files/cat_test_4.txt']),
                         'next line should be omitted:\nSuccess!\n')
        self.assertEqual(self.cat.invoke(['-s', '-n', f'{os.path.dirname(__file__)}/test_files/cat_test_4.txt']),
                         '1 next line should be omitted:\n2 Success!\n')

        with self.assertRaises(FlagError):
            self.cat.invoke(['arg1', '-n'])
            self.cat.invoke(['-f', 'arg1'])
            self.cat.invoke(['-s', '-v'])

    def test_exit(self) -> None:
        with self.assertRaises(SystemExit):
            self.exit.invoke()

    def test_echo(self) -> None:
        self.assertEqual(self.echo.invoke(['a']), 'a')
        self.assertEqual(self.echo.invoke(['echo test']), 'echo test')
        self.assertEqual(self.echo.invoke(['']), '')

    def test_wc(self) -> None:
        self.assertEqual(self.wc.invoke([f'{os.path.dirname(__file__)}/test_files/wc_test_1.txt']),
                         '3 6 27  wc_test_1.txt')
        self.assertEqual(self.wc.invoke(
            [f'{os.path.dirname(__file__)}/test_files/wc_test_1.txt',
             f'{os.path.dirname(__file__)}/test_files/wc_test_2.txt']),
            '3 6 27  wc_test_1.txt\n 3 6 27  wc_test_2.txt')
        self.assertEqual(self.wc.invoke(['-l', f'{os.path.dirname(__file__)}/test_files/wc_test_1.txt']),
                         '3 wc_test_1.txt')
        self.assertEqual(self.wc.invoke(['-w', f'{os.path.dirname(__file__)}/test_files/wc_test_1.txt']),
                         '6 wc_test_1.txt')
        self.assertEqual(self.wc.invoke(['-c', f'{os.path.dirname(__file__)}/test_files/wc_test_1.txt']),
                         '27 wc_test_1.txt')

        with self.assertRaises(FlagError):
            self.wc.invoke(['-f', 'arg'])
            self.wc.invoke(['arg', '-l'])

    def test_pipelines(self) -> None:
        self.test_bash.run('a=cat')
        self.test_bash.run("ex=exit")
        self.assertEqual(self.test_bash.run('echo a | echo b | echo c'), 'c')
        self.assertEqual(self.test_bash.run(f'echo /test_files/wc_test_1.txt | wc'),
                         '1 1 26')
        self.assertEqual(self.test_bash.run('echo README.md | cat'), 'README.md')
        self.assertEqual(self.test_bash.run(f'echo /test_files/cat_test_1.txt | cat'),
                         '/test_files/cat_test_1.txt')
        self.assertEqual(self.test_bash.run('x=t | echo x'), 'x')
        self.assertEqual(
            self.test_bash.run(f' pwd | echo | $a /test_files/cat_test_2.txt '),
            """/test_files/cat_test_2.txt""")
        self.assertEqual(self.test_bash.run('echo test | cat | wc'), '1 1 5')
        self.assertEqual(self.test_bash.run('pwd | echo'),
                         '')  # - in reality we get \n and it's ok, this is just for tests
        self.assertEqual(self.test_bash.run('pwd | echo test'), 'test')

        with self.assertRaises(SystemExit):
            self.test_bash.run(f'wc {os.path.dirname(__file__)}/test_files/wc_test_1.txt | exit')
            self.test_bash.run('pwd | echo')
            self.test_bash.run('pwd | echo | $ex')
            self.test_bash.run(' | | ')

    def test_external_command(self) -> None:
        ExternalCommand.external_command_name = 'git'
        self.assertEqual(self.test_bash.run('git status'), ExternalCommand.external_output)

    def test_grep(self) -> None:
        pass

    def test_subst(self) -> None:
        self.test_bash.run('a=6')
        self.test_bash.run('b=2')
        self.test_bash.run(f'let x=test_files/wc_test_1.txt')
        self.assertEqual(self.test_bash.run('echo $a'), '6')
        self.assertEqual(self.test_bash.run('echo $b'), '2')
        self.assertEqual(self.test_bash.run('echo $a | echo $b'), '2')
        self.assertEqual(self.test_bash.run('echo $x | wc'), '1 1 25')
