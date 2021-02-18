import unittest
import sys
from io import StringIO
import shutil
import os

from klickbrick import shell
from klickbrick import config

TEST_DIRECTORY = 'test_directory'


class TestShell(unittest.TestCase):
    def setUp(self):
        config.initialize()
        self.held, sys.stdout = sys.stdout, StringIO()
        os.makedirs(TEST_DIRECTORY, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(TEST_DIRECTORY)

    def test_execute_happy_path(self):
        return_value_code, return_value_stdout = shell.execute('echo hello')
        self.assertEqual(return_value_code, 0)
        self.assertTrue('hello' in return_value_stdout)

    def test_execute_sad_path(self):
        return_value_code, return_value_stdout = shell.execute('foo')
        self.assertGreater(return_value_code, 0)
        self.assertTrue('command not found' in return_value_stdout)

    def test_execute_sad_path_ls(self):
        return_value_code, return_value_stdout = shell.execute('ls foo')
        self.assertGreater(return_value_code, 0)
        self.assertTrue('No such file or directory' in return_value_stdout)

    def test_execute_happy_path_dry_run(self):
        config.DRY_RUN = True
        return_value_code, return_value_stdout = shell.execute('ls foo')
        stdout_output = sys.stdout.getvalue()
        self.assertTrue('ls foo' in stdout_output)
        self.assertEqual(return_value_code, 0)
        self.assertTrue('Invoked using dry run' in return_value_stdout)

    def test_append_to_file_adds_newlines(self):
        test_file_path = f'{TEST_DIRECTORY}/test_file'
        test_text = 'new text to add'

        with open(test_file_path, 'w') as file:
            file.write('some pre-existing text')
        shell.append_to_file(test_file_path, test_text)
        with open(test_file_path, 'r') as file:
            contents = file.read()
        self.assertTrue(f'\n{test_text}\n' in contents)

    def test_append_to_file_that_does_not_exist(self):
        test_file_path = f'{TEST_DIRECTORY}/test_file'
        test_text = 'new text to add'

        shell.append_to_file(test_file_path, test_text)
        with open(test_file_path, 'r') as file:
            contents = file.read()
        self.assertTrue(f'\n{test_text}\n' in contents)

    def test_create_directory_happy_path(self):
        return_value = shell.create_directory(
            f'{TEST_DIRECTORY}/new_directory'
        )
        self.assertTrue(os.path.isdir(f'{TEST_DIRECTORY}/new_directory'))
        self.assertTrue(return_value)

    def test_create_directory_logs_error_if_already_exists(self):
        return_value = shell.create_directory(TEST_DIRECTORY)
        self.assertFalse(return_value)

    def test_copy_file_happy_path(self):
        test_file_source_path = f'{TEST_DIRECTORY}/source_file'
        test_file_destination_path = f'{TEST_DIRECTORY}/destination_file'
        test_file_contents = 'some pre-existing text'

        with open(test_file_source_path, 'w') as file:
            file.write(test_file_contents)

        return_code = shell.copy_file(
            test_file_source_path, test_file_destination_path
        )
        self.assertTrue((os.path.isfile(test_file_destination_path)))
        with open(test_file_destination_path, 'r') as file:
            contents = file.read()
        self.assertTrue(test_file_contents in contents)
        self.assertTrue(return_code)

    def test_copy_file_source_file_does_not_exist(self):
        test_file_source_path = f'{TEST_DIRECTORY}/source_file'
        test_file_destination_path = f'{TEST_DIRECTORY}/destination_file'

        return_code = shell.copy_file(
            test_file_source_path, test_file_destination_path
        )
        self.assertFalse(return_code)


if __name__ == '__main__':
    unittest.main()
