from argparse import ArgumentParser
import json
import sys

from . import print_page


def main():
    parser = ArgumentParser(
        prog='pronounspageviewer',
        description='Read the Pronouns.page file from stdin',
    )
    parser.add_argument('-f', '--file', required=False,
                        help='Pass in the Pronouns.page file name rather than read from stdin')
    args = parser.parse_args()
    if args.file:
        file = open(args.file)
    else:
        file = sys.stdin
    try:
        page_data = json.load(file)
    except json.JSONDecodeError:
        print('File is invalid JSON format')
        return
    finally:
        file.close()
    if not isinstance(page_data, dict):
        print('JSON object must be a dictionary', file=sys.stderr)
        return
    print_page(page_data)


if __name__ == '__main__':
    main()
