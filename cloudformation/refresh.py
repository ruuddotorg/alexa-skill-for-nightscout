#!/usr/bin/env python3

import argparse
import os
import re

INDENT_LEVEL = 4


def refresh_includes(template, base):
    output = []
    indent = None
    for line in template.splitlines():
        line = line.replace('\t', ' '*8)
        if indent is not None and (line.startswith(indent) or not line):
            continue
        output.append(line + '\n')
        m = re.search(r'^( *).*\|.*#file (.*)$', line)
        if m:
            spaces, filename = m.groups()
            indent = spaces + ' ' * INDENT_LEVEL
            with open(os.path.join(base, filename)) as include_file:
                for line in include_file:
                    if not line.strip():
                        output.append('\n')
                    else:
                        output.append(indent + line)
        else:
            indent = None
    return ''.join(output)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Update include files in a CloudFormation template.'
    )
    parser.add_argument(
        'filename',
        nargs='+',
        help='Template body file.'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    for filename in args.filename:
        with open(filename) as template_file:
            template = template_file.read()
        new_template = refresh_includes(template, os.path.dirname(filename))
        if new_template != template:
            print(filename)
            with open(filename, 'w') as template_file:
                template_file.write(new_template)
