import numpy as np

A = list(map(float, input().split()))
B = list(map(float, input().split()))
pi = list(map(float, input().split()))

def trabsforme_matrix(A):
    #transform_list_matrix_2D
    matrix_A = []
    for i in range(int(A[0])):
        matrix_A.append(A[(2 + i*int(A[1])):(2 + (i+1)*int(A[1]))])
    matrix_A = np.array(matrix_A)
    return matrix_A


print(np.dot(np.dot(product_numpy(pi), product_numpy(A)), product_numpy(B)))
