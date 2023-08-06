# importing the required modules
import os
import argparse
from authenticate import UserAuthenticate
from bp_manifest import BPManifest


def main():
    # create parser object
    parser = argparse.ArgumentParser(description="BuildPiper CLI manager!!",
                                     usage='bpctl [options] <command> [-o --optional arguments]')
    parser.add_argument('action', nargs='?', default=os.getcwd())
    parser.add_argument('-f', "--file", nargs='?', default=os.getcwd(), metavar="file", help="bp.yaml file path")
    parser.add_argument('-r', "--recursive", nargs='?', default=None, metavar="recursive",
                        help="recursive search bp.yaml file path")
    parser.add_argument("-o", "--output", type=str, nargs=1, metavar="output", default=None,
                        help="Output will be show in your option format. eg. yaml or json")
    parser.add_argument("-d", "--debug", type=bool, nargs='?', metavar="debug", const=True,
                        help="Shows all the debug logs")

    parse_args = parser.parse_args()
    # # calling functions depending on type of argument
    if parse_args.action == 'login':
        if parse_args.debug:
            print("Login start")
        UserAuthenticate(parse_args).login()
    elif parse_args.action == 'get':
        print("Feature coming soon in next release")
    elif parse_args.action == 'apply':
        BPManifest(parse_args).parse_files(parse_args.file)
    elif parse_args.action == 'delete':
        print("Feature coming soon in next release")
    else:
        print("bpctl [options] <command> [-o --optional arguments]")


if __name__ == "__main__":
    # calling the main function
    main()
