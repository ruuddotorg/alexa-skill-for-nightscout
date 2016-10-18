#!/usr/bin/env python3

import argparse
import difflib
import os

import botocore.session


client = botocore.session.get_session().create_client('cloudformation')


def stack_exists(stack):
    try:
        client.describe_stacks(StackName=stack)
        return True
    except botocore.exceptions.ClientError:
        return False


def print_diff(stack, template):
    live = client.get_template(StackName=stack)['TemplateBody']
    print(''.join(difflib.unified_diff(
        live.splitlines(keepends=True),
        template.splitlines(keepends=True),
        fromfile='live',
        tofile='proposed'
    )))


def deploy_stack(stack, template, confirm=True):
    exists = stack_exists(stack)
    if confirm:
        if exists:
            print_diff(stack, template)
        else:
            print(template)
        confirm = input('Confirm (y/n)? ')
        if confirm.lower() != 'y':
            return
    kwargs = dict(
        StackName=stack,
        TemplateBody=template,
        Capabilities=['CAPABILITY_IAM'],
    )
    if exists:
        response = client.update_stack(**kwargs)
    else:
        response = client.create_stack(**kwargs)
    print(response)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Deploy a CloudFormation stack.'
    )
    parser.add_argument(
        '-y', '--yes',
        action='store_true',
        default=False,
        help='Skip confirmation.'
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
        stack, _ = os.path.splitext(os.path.basename(filename))
        with open(filename) as template_file:
            template = template_file.read()
        deploy_stack(stack, template, confirm=not args.yes)
