#!/usr/bin/env python3
# coding: utf-8
"""Provide parsing method for the command line arguments."""
import argparse
import os


def _check_positive(value):
    """Ensure a given value is a positive integer."""
    int_value = int(value)
    if int_value < 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value"
                                         % value)
    return int_value


def _valid_path(value):
    if not (os.path.exists(value) and os.path.isfile(value)):
        raise argparse.ArgumentTypeError("%s doesn't seem to be a valid file."
                                         % value)
    return value


def parseOpts():
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Namespace of the parsed arguments.
    """
    PARSER = argparse.ArgumentParser(
        description="Utility to download zoom videos",
        prog="zoomdl",
        formatter_class=(lambda prog:
                         argparse.HelpFormatter(prog,
                                                max_help_position=10,
                                                width=200)
                         ))

    PARSER.add_argument("-u", "--url",
                        help=("Enter the url of the video to download. "
                              "Looks like 'zoom.us/rec/play/...'"),
                        type=str,
                        required=True,
                        metavar="url")
    PARSER.add_argument("-f", "--filename",
                        help=("The name of the output video file without "
                              "extension. Default to the filename according "
                              "to Zoom. Extension is automatic."),
                        metavar="filename")
    PARSER.add_argument("-d", "--filename-add-date",
                        help=("Add video meeting date if it is specified. "
                              "Default is not to include the date."),
                        default=False,
                        action='store_true')
    PARSER.add_argument("--user-agent",
                        help=("Use custom user agent."
                              "Default is real browser user agent."),
                        type=str)
    PARSER.add_argument("-p", "--password",
                        help="Password of the video (if any)",
                        metavar="password")
    PARSER.add_argument("-c", "--count-clips",
                        help=("If multiple clips, how many to download. "
                              "1 = only current URL (default). "
                              "0 = all of them. "
                              "Other positive integer, count of clips to "
                              "download, starting from the current one"),
                        metavar="Count",
                        type=_check_positive,
                        default=1)
    PARSER.add_argument("-v", "--log-level",
                        help=("Chose the level of verbosity. 0=debug, 1=info "
                              "(default), 2=warning 3=Error, 4=Critical, "
                              "5=Quiet (nothing printed)"),
                        metavar="level",
                        type=int,
                        default=1)

    PARSER.add_argument("--cookies",
                        help="Provide a Netscape-format cookies file",
                        metavar="cookies.txt",
                        type=_valid_path,
                        required=False)
    return PARSER.parse_args()
