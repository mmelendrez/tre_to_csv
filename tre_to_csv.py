#!/user/bin/env python

import argparse

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "treefile",
    help = ".nwk or .tre file path"
  )
  return parser.parse_args()

def main(args):
  fh = open(args.treefile)
  print_first_line(fh)

def print_first_line(fh):
  print fh.readline()

if __name__ == "__main__":
  args = parse_args()
  main(args)
