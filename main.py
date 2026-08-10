import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--directory", required=True)

args = parser.parse_args()

print(args.directory)