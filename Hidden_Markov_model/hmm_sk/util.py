def extract_matrix():
    A = list(map(float, input().split()))
    B = list(map(float, input().split()))
    pi = list(map(float, input().split()))
    O  = list(map(int, input().split()))
    for m in [A,B,pi]:
        m[0] = int(m[0])
        m[1] = int(m[1])
    return A, B, pi, O


def mat2str(A):
    l = [str(A[0]), str(A[1])]
    for i in range(2, len(A)):
        l.append(str(round(A[i],6)))
    return " ".join(l)
