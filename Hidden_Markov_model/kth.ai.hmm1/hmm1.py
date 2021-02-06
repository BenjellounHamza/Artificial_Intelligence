__author__      =  "Hamza BENJELLOUN & Omar BENCHEKROUN"

from util import *

def forward(A, B, pi, O):
    alpha_t = [pi[i+2]*B[i*B[1]+O[1]+2] for i in range(A[0])]
    for t in range(1, O[0]):
        alpha_t_prev = [tmp for tmp in alpha_t]
        for i in range(A[0]):
            alpha_t_i = 0
            for j in range(A[0]):
                alpha_t_i += alpha_t_prev[j]*A[j*A[1]+i+2]
            alpha_t_i *= B[i*B[1]+O[t+1]+2]
            alpha_t[i] = alpha_t_i
    return alpha_t

def main():
    # extract matrix from the file
    A, B, pi, O = extract_matrix()
    print(sum(forward(A, B, pi, O)))


main()
