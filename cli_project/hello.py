import argparse
import sys


def parse_args(args=None):
    parser = argparse.ArgumentParser()

    # Arguments
    parser.add_argument('hello',
                        type=str,
                        help='Friendly command that says hello')
    
    # Optional arguments
    parser.add_argument('--name',
                        type=str,
                        default='world',
                        help='Optional flag to be more personal')
    
    return parser.parse_args(args)


def main():
    args = parse_args()

    if args.hello == 'hello':
        print(f'hello {args.name}')


if __name__ == '__main__':
    main()
