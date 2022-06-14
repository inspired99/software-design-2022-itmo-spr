from collections import defaultdict
from unittest import TestCase

from src.commandParse.commandParser import CommandParser
from src.commandParse.parseExceptions import AssignmentError, PipelineError, ImbalancedQuotesError
from src.env.env import Environment


class TestParserAndEnv(TestCase):
    def setUp(self) -> None:
        self.parser = CommandParser()
        self.env = Environment()

        self.env.set_var('a', 5)
        self.env.set_var('var', 'a')
        self.env.set_var('b', 'C:/home/Apps')

    def test_parse_binds(self) -> None:
        environment = self.parser.env
        self.assertEqual(self.parser.parse_bind(""), None)
        self.parser.parse_bind("let a=5 x=1")
        self.assertEqual('5', environment.get_var('a')[-1])
        self.assertEqual('1', environment.get_var('x')[-1])
        self.parser.parse_bind("let x=a let a=5")
        self.assertEqual('a', environment.get_var('x')[-1])
        self.assertEqual('5', environment.get_var('a')[-1])
        self.parser.parse_bind("x=4 a=6")
        self.assertEqual('4', environment.get_var('x')[-1])
        self.assertEqual('6', environment.get_var('a')[-1])
        self.parser.parse_bind("a=5 | echo a | echo 'in'")
        self.assertEqual('5', environment.get_var('a')[-1])
        self.parser.parse_bind("x=2 let x=3 x=7")
        self.assertEqual('7', environment.get_var('x')[-1])

        with self.assertRaises(AssignmentError):
            self.parser.parse_bind(" var = 2")
            self.parser.parse_bind(" var= 1")
            self.parser.parse_bind(" let x = 2")

    def test_parse_pipelines_commands(self) -> None:
        self.assertEqual(self.parser.parse_pipelines_and_commands(" echo a | wc 1.txt | wc  2.txt | wc 3.txt"),
                         defaultdict(list, {('echo', 0): ['a'],
                                            ('wc', 1): ['1.txt'],
                                            ('wc', 2): ['2.txt'],
                                            ('wc', 3): ['3.txt']}))
        self.assertEqual(self.parser.parse_pipelines_and_commands("cat 1.txt"),
                         defaultdict(list, {('cat', 0): ['1.txt']}))
        self.assertEqual(self.parser.parse_pipelines_and_commands(""), {})
        self.assertEqual(self.parser.parse_pipelines_and_commands("    "), {})
        self.assertEqual(self.parser.parse_pipelines_and_commands("echo new| cat $file "),
                         defaultdict(list, {('echo', 0): ['new'], ('cat', 1): ['$file']}))
        self.assertEqual(self.parser.parse_pipelines_and_commands(" x=2  |  pwd"), defaultdict(list, {('pwd', 1): []}))
        self.assertEqual(self.parser.parse_pipelines_and_commands('cat "1.txt" | wc'),
                         defaultdict(list, {('cat', 0): ['1.txt'], ('wc', 1): []}))
        self.assertEqual(self.parser.parse_pipelines_and_commands("""cat 1.txt | cat -l 2.txt 3.txt | 
        wc "test file.txt" | cat 'test file2.txt' test_file3.txt"""),
                         defaultdict(list, {('cat', 0): ['1.txt'], ('cat', 1): ['-l', '2.txt', '3.txt'],
                                            ('wc', 2): ['test file.txt'],
                                            ('cat', 3): ['test file2.txt',
                                                         'test_file3.txt']}))

        with self.assertRaises(PipelineError):
            self.parser.parse_pipelines_and_commands(" | ")
            self.parser.parse_pipelines_and_commands(" cate 1.txt | wc | pwd ")
            self.parser.parse_pipelines_and_commands(" pwd | pwd |")
            self.parser.parse_pipelines_and_commands(" | exit | echo a ")
            self.parser.parse_pipelines_and_commands("cat ")
            self.parser.parse_pipelines_and_commands("cwd")

    def test_environment(self) -> None:
        self.assertEqual(self.env.get_var('a'), [5])
        self.assertEqual(self.env.get_var('var'), ['a'])
        self.env.set_var('a', 'new')
        self.assertEqual(self.env.get_var('a'), [5, 'new'])
        self.assertEqual(self.env.get_var('c'), '')
        self.assertEqual(self.env.get_var('ab'), '')

    def test_substitution_vars(self) -> None:
        self.parser.env.set_var('a', 5)
        self.parser.env.set_var('avb', 6)
        self.parser.env.set_var('file', 'C:/home')
        self.parser.env.set_var('p', 'pw')
        self.parser.env.set_var('d', 'd')
        self.assertEqual(self.parser.subst_vars('echo "$a"'), 'echo 5')
        self.parser.env.set_var('a', 'new')
        self.assertEqual(self.parser.subst_vars('echo "$a"'), 'echo new')
        self.assertEqual(self.parser.subst_vars('echo $a | cat $file | cat $file'), 'echo new | cat C:/home | cat '
                                                                                    'C:/home')
        self.assertEqual(self.parser.subst_vars("cat '$file'"), "cat $file")
        self.assertEqual(self.parser.subst_vars('echo $a $avb'), 'echo new 6')
        self.assertEqual(self.parser.subst_vars('echo "$a" $avb'), 'echo new 6')
        self.assertEqual(self.parser.subst_vars("""echo '$a' "$a" """), "echo $a new")
        self.assertEqual(self.parser.subst_vars('$p$d'), 'pwd')
        self.assertEqual(self.parser.subst_vars('echo $b'), 'echo')

    def test_quotes(self) -> None:
        self.assertEqual(self.parser.subst_vars("echo 'a' "), "echo a")
        self.assertEqual(self.parser.subst_vars("""echo "a" """), "echo a")
        self.assertEqual(self.parser.subst_vars("echo '$a'"), 'echo $a')
        self.assertEqual(self.parser.subst_vars('echo " a a a "'), 'echo a a a')

        with self.assertRaises(ImbalancedQuotesError):
            self.parser.subst_vars('echo "a ')
            self.parser.subst_vars('echo a | cat " text ')
            self.parser.subst_vars('wc "ab.txt', )
            self.parser.subst_vars("echo ' a a")
