import argparse
import subprocess
import sys

import config

# Colours
FAIL_C = '\033[91m'
END_C = '\033[0m'


def execute(args):
    if config.DRY_RUN:
        print(args)
        return 0, 'Invoked using dry run'
    else:
        output = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            executable='/bin/bash',
        )
        return output.returncode, output.stdout.decode('utf-8')

class KBK:
    def __init__(self, arguments):
        parser = argparse.ArgumentParser(prog='kbk')
        
        # Create base subparser so parsers can consume it as parent and share common arguments
        self.base_subparser = argparse.ArgumentParser(add_help=False)
        self.base_subparser.add_argument(
            '-v',
            '--version',
            action='version',
            version=f'%(prog)s 0.1.0',
        )
        self.base_subparser.add_argument(
            '-d',
            '--dry-run',
            action='store_true',
            help='Inspect what the result of the command will be without any side effects',
        )

        args, _ = self.base_subparser.parse_known_args(arguments)
        if args.dry_run is True:
            config.DRY_RUN = True
        
        self.subparsers = parser.add_subparsers()

        try:
            command = arguments[0]
        except IndexError:
            exit(0)
        
        getattr(self, command)(arguments)
    
    def __create_parser(self, name, description):
        parser = self.subparsers.add_parser(
            name=name,
            parents=[self.base_subparser],
            description=description,
        )
        return parser
    
    # -------- COMMANDS -------- #

    def hello(self, arguments):
        parser = self.__create_parser('hello', 'A friendly Hello World')
        parser.add_argument(
            '-n',
            '--name',
            type=str,
            default='world',
            help='Optional flag to be more friendly',
        )
        args = parser.parse_args(arguments[1:])
        print(f'hello {args.name}')
    
    def cmd(self, arguments):
        parser = self.__create_parser(
            'cmd',
            'Runs shell command',
        )
        parser.add_argument(
            'command',
            nargs='+',
            help='Execute command in a subprocess.',
        )
        args = parser.parse_args(arguments[1:])
        returncode, output = execute(args.command)

        if returncode == 0:
            print(output)
        else:
            print(f'{FAIL_C}{output}{END_C}')


def main():
    config.initialize()
    KBK(sys.argv[1:])


if __name__ == '__main__':
    main()
