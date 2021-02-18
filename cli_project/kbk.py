import argparse
import subprocess
import sys
import inspect

from cli_project import __version__
from cli_project import config


# Colours
FAIL_C = '\033[91m'
END_C = '\033[0m'


# TODO make telemetry user configurable
ENABLE_TELEMETRY = False


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
            version=f'%(prog)s {__version__}',
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

        # Handle no arguments
        if len(arguments) == 0:
            self.help(arguments)
        else:
            command = arguments[0]
            if (command == '-h') or (command == '--help'):
                self.help(arguments)
            
            # handle undefined command
            elif not hasattr(self, command):
                self.help(arguments)
            else:
                # use dispatch pattern to invoke method with same name so it's easy to add new subcommands
                getattr(self, command)(arguments)

        if ENABLE_TELEMETRY:
            send_metric(arguments)

    def __create_parser(self, name, description):
        parser = self.subparsers.add_parser(
            name=name,
            parents=[self.base_subparser],
            description=description,
        )
        return parser
    
    # -------- COMMANDS -------- #

    def help(self, arguments):
        parser = self.__create_parser(
            'help', 'Instructions for using the kbk CLI'
        )
        parser.add_argument('help', nargs='?', help=argparse.SUPPRESS)
        parser.add_argument(
            'command',
            nargs='?',
            help='name of command to show usage for',
        )
        
        parser.print_help()
        print_available_commands(self)

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


def print_available_commands(instance):
    print('\nList of available commands are:')
    
    commands = [attr for attr in dir(instance)if inspect.ismethod(getattr(instance, attr))][2:] 
    for _cmd in commands:
        if _cmd == 'help':
            continue
        else:
            print(f'  {_cmd}')    


def send_metric(cli_input):
    """Telemetry - emitting usage events to a backend server."""
    # TODO capture exit reason and duration
    payload = {
        'metrics': [
            {
                'userId': os.getlogin(),
                'osPlatform': platform.system(),
                'osVersion': platform.version(),
                'pythonVersion': sys.version,
                'command': {
                    'input': ' '.join(cli_input),
                    'exitReason': 'Not Implemented',
                    'exitCode': 'Not Implemented',
                    'duration': 'Not Implemented',
                    'timestamp': datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
                },
            }
        ]
    }

    # Buffering the metrics locally and sending at some interval might be a more robust solution
    requests.post(
        'http://localhost:8080/metrics', json=payload, timeout=2000
    )


def main():
    config.initialize()
    KBK(sys.argv[1:])


if __name__ == '__main__':
    main()
