#!/usr/bin/env python3

from argparse import ArgumentParser
from silent import generate

def main():
    parser = ArgumentParser()
    parser.add_argument("file_path", help="path to gpx file")
    args = parser.parse_args()
    file_path = args.file_path

    with open(file_path, "r") as f:
        gpx_string = f.read()

    generate(gpx_string)

if __name__ == "__main__":
    main()
