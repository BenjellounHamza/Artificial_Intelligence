__author__      =  "Hamza BENJELLOUN & Omar BENCHEKROUN"

from util import *



def delta(A, B, pi, O, t, i, indices_delta, list_delta):
    assert t >= 0
    assert i >= 0 and i < A[0]
    if t == 0:
        list_delta[t][i] = B[2 + i*B[1] + O[t + 1]]*pi[2 + i]
        indices_delta[t][i] = -555
        return list_delta[t][i]
    else:
        max = 0
        ind_max = 0
        for j in range(A[0]):
            if(list_delta[t-1][j] == -1):
                d = delta(A, B, pi, O, t-1, j, indices_delta, list_delta)
            else:
                d = list_delta[t-1][j]
            tmp = A[2 + j*A[1] + i]*d*B[2 + i*B[1] + O[t+1]]
            if tmp > max:
                max = tmp
                ind_max = j
        indices_delta[t][i] = ind_max
        list_delta[t][i] = max
        return max



def main():
    A, B, pi, O = extract_matrix()
    # initialisation of matrix used in delta function to store the deltas and the path:
    indices_delta = [A[0]*[-1] for _ in range(O[0])]
    list_delta = [A[0]*[-1] for _ in range(O[0])]

    # compute last deltas
    deltas_T = [delta(A, B, pi, O, O[0]-1, j, indices_delta, list_delta) for j in range(A[0])]
    max_delta = max(deltas_T)
    arg_max = deltas_T.index(max_delta)

    # determinate the path fom the T-1 to 0
    chemin = []
    for k in range(O[0] - 1, -1, -1):
        chemin = [arg_max] + chemin
        arg_max = indices_delta[k][arg_max]
    print(mat2str(chemin))

main()
