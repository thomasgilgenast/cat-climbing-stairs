import sys

from node import build_tree

if __name__ == '__main__':
    total = int(sys.argv[1])
    limit = int(sys.argv[2])
    build_tree({1: total}, limit=limit)
