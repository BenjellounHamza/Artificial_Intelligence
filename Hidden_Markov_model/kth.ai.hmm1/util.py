__author__      =  "Hamza BENJELLOUN & Omar BENCHEKROUN"

def extract_matrix():
    A = list(map(float, input().split()))
    B = list(map(float, input().split()))
    pi = list(map(float, input().split()))
    O  = list(map(int, input().split()))
    for m in [A,B,pi]:
        m[0] = int(m[0])
        m[1] = int(m[1])
    return A, B, pi, O


def product(A,B):
    #return product AxB, matrixes are formatted as given
    assert A[1]==B[0]
    prod = [A[0],B[1]]
    for i in range(int(A[0])):
        for j in range(int(B[1])):
            r = 0
            for k in range(int(A[1])):
                r += A[i*int(A[1])+k+2] * B[k*int(B[1])+j+2]
            prod.append(r)
    return prod

def mat2str(A):
    l = [str(int(A[0])), str(int(A[1]))]
    for i in range(2, len(A)):
        l.append(str(round(A[i],5)))
    return " ".join(l)
