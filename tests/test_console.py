import unittest
from unittest.mock import patch
from io import StringIO
import os
import sys

# Importing the module to test
from console import HBNBCommand


class TestConsole(unittest.TestCase):

    def setUp(self):
        self.console = HBNBCommand()

    def tearDown(self):
        del self.console

    def test_prompt(self):
        # Test prompt value when stdin is a tty
        with patch('sys.stdin.isatty', return_value=True):
            self.assertEqual(self.console.prompt, '(hbnb) ')

        # Test prompt value when stdin is not a tty
        with patch('sys.stdin.isatty', return_value=False):
            self.assertEqual(self.console.prompt, '')

    def test_precmd(self):
        # Test for correct reformatting of command line
        line = 'update User 1234 name "John Doe"'
        expected_output = 'update User 1234 name John Doe'
        self.assertEqual(self.console.precmd(line), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_quit(self, mock_stdout):
        # Test do_quit method
        with self.assertRaises(SystemExit):
            self.console.do_quit(None)
        self.assertEqual(mock_stdout.getvalue(), '')

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_EOF(self, mock_stdout):
        # Test do_EOF method
        with patch('builtins.print'):
            self.console.do_EOF(None)
        self.assertEqual(mock_stdout.getvalue(), '\n')

    @patch('sys.stdout', new_callable=StringIO)
    def test_emptyline(self, mock_stdout):
        # Test emptyline method
        with patch('builtins.print'):
            self.console.emptyline()
        self.assertEqual(mock_stdout.getvalue(), '')

    def test_do_create(self):
        # Test do_create method
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("create BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertIn("missing **", output)

            self.console.onecmd("create RandomModel")
            output = mock_stdout.getvalue().strip()
            self.assertIn("doesn't exist **", output)

    def test_do_show(self):
        # Test do_show method
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("show")
            output = mock_stdout.getvalue().strip()
            self.assertIn("missing **", output)

            self.console.onecmd("show BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertIn("missing **", output)

            self.console.onecmd("show BaseModel 1234")
            output = mock_stdout.getvalue().strip()
            self.assertIn("no instance found **", output)

            self.console.onecmd("create BaseModel")
            self.console.onecmd("show BaseModel 1234")
            output = mock_stdout.getvalue().strip()
            self.assertIn("no instance found **", output)

    def test_do_destroy(self):
        # Test do_destroy method
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("destroy")
            output = mock_stdout.getvalue().strip()
            self.assertIn("missing **", output)

            self.console.onecmd("destroy BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertIn("missing **", output)

            self.console.onecmd("destroy BaseModel 1234")
            output = mock_stdout.getvalue().strip()
            self.assertIn("no instance found **", output)

            self.console.onecmd("create BaseModel")
            self.console.onecmd("destroy BaseModel 1234")
            self.console.onecmd("show BaseModel 1234")
            output = mock_stdout.getvalue().strip()
            self.assertIn("no instance found **", output)

    def test_do_all(self):
        # Test do_all method
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("all")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '')

            self.console.onecmd("all BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertIn("missing **", output)

            self.console.onecmd("create BaseModel")
            self.console.onecmd("all BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertIn("BaseModel", output)

    def test_do_count(self):
        # Test do_count method
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("count")
            output = mock_stdout.getvalue().strip()
            self.assertIn("missing **", output)

            self.console.onecmd("count BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertIn("0", output)

            self.console.onecmd("create BaseModel")
            self.console.onecmd("count BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertIn("1", output)

    def test_do_update(self):
        # Test do_update method
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("update")
            output = mock_stdout.getvalue().strip()
            self.assertIn("missing **", output)

            self.console.onecmd("update BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertIn("missing **", output)

            self.console.onecmd("update BaseModel 1234")
            output = mock_stdout.getvalue().strip()
            self.assertIn("no instance found **", output)

            self.console.onecmd("create BaseModel")
            self.console.onecmd('update BaseModel 1234 name "John Doe"')
            self.console.onecmd('show BaseModel 1234')
            output = mock_stdout.getvalue().strip()
            self.assertIn("John Doe", output)


if __name__ == '__main__':
    unittest.main()
