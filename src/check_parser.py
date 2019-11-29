from argparse import ArgumentParser, RawTextHelpFormatter
import sys
import string


def chk_parser(parser):
    args = parser.parse_args()

    if args.file == "":
        raise NameError("Parser Error: Invalid FileName")

    if args.cut == "":
        raise NameError("Parser Error: Invalid Cut FileName")

    if args.cross_level == False:
        if (args.file.count(",")+1) > 1:
            raise NameError("Parser Error: Too many FileName")

    if args.cross_level == True:
        if (args.file.count(",")+1) <=2:
            raise NameError("Parser Error: Invalid CrossPolar definition. Tree files should be expected [Copola], [45 plane CX], [-45 plane CX]")

    print(args)
