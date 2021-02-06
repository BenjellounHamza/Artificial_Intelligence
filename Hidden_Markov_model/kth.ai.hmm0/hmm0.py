__author__      =  "Hamza BENJELLOUN & Omar BENCHEKROUN"

from util import *


def main():
    A = list(map(float, input().split()))
    B = list(map(float, input().split()))
    pi = list(map(float, input().split()))
    print(mat2str(product(product(pi,A),B)))


main()
