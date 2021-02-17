import unittest
from cli_project import hello


class HelloTest(unittest.TestCase):

    def test_parse_args(self):
        args = hello.parse_args(['hello', '--name', 'dimitri'])
        self.assertEqual('hello', args.hello)
        self.assertEqual('dimitri', args.name)


if __name__ == '__main__':
    unittest.main()
