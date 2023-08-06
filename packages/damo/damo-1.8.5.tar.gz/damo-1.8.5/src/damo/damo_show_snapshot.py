# SPDX-License-Identifier: GPL-2.0

import argparse

import damo_show_raw

import _damo_subcmds

subcmds = [
        _damo_subcmds.DamoSubCmd(name='raw', module=damo_show_accesses_raw,
            msg='human readable raw data'),
        ]

def set_argparser(parser):
    subparsers = parser.add_subparsers(title='format', dest='output_format',
            metavar='<output format>',
            help='the format of the output to show the record')
    subparsers.required = True

    for subcmd in subcmds:
        subcmd.add_parser(subparsers)

def main(args=None):
    if not args:
        parser = argparse.ArgumentParser()
        set_argparser(parser)
        args = parser.parse_args()

    for subcmd in subcmds:
        if subcmd.name == args.output_format:
            subcmd.execute(args)

if __name__ == '__main__':
    main()
