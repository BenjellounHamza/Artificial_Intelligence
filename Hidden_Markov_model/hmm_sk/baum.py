import random
def print_matrice(A):
    for i in range(A[0]):
        s = ""
        for j in range(A[1]):
            s = s + str(A[i*A[1] + j+2]) + " ,"
        print(s)
def init(N, M):
    A = N*N*[1/N]
    B = N*M*[1/M]
    pi = N*[1/N]

    for i in range(N):
        for j in range(N-1):
            A[i*N+j]+=random.uniform(-1/(N*N),1/(N*N))
        A[i*N+N-1] = 1-sum([A[i*N+j] for j in range(N-1)])
        for k in range(M-1):
            B[i*M+k]+=random.uniform(-1/(M*M),1/(M*M))
        B[i*M+M-1] = 1-sum([B[i*M+k] for k in range(M-1)])

    for i in range(N-1):
        pi[i]+=random.uniform(-1/(N*N),1/(N*N))
    pi[N-1] = 1-sum([pi[i] for i in range(N-1)])
    A = [N, N] +A
    B = [N, M] +B
    pi = [1, N] +pi

    return [A, B, pi]

#print(init(4,3)[0])

def baum(A, B, pi, O, maxIters=30):
    #baum welch algorithm

    alphas = [A[0]*[0] for _ in range(O[0])]
    betas = [A[0]*[0] for _ in range(O[0])]
    di_gammas = [[A[0]*[0] for _ in range(A[0])] for i in range(O[0]-1)]
    gammas = [A[0]*[0] for _ in range(O[0])]
    maxIters = 30
    cpt=0
    #old_log_prob = -inf
    #log_prob = -inf
    #and log_prob>old_log_prob
    while(cpt<maxIters):
        #old_log_prob = log_prob
        cpt+=1
        for i in range(A[0]):
            alphas[0][i] = pi[i+2]*B[i*B[1]+O[1]+2]
        c_0 = 1/sum(alphas[0])
        for i in range(A[0]):
            alphas[0][i] *= c_0
        cs = [c_0]
        for t in range(1, O[0]):
            for i in range(A[0]):
                s3 = 0
                for j in range(A[0]):
                    s3 += alphas[t-1][j]*A[j*A[1]+i+2]
                alphas[t][i] = s3* B[i*B[1]+O[t+1]+2]
            c_t = 1/sum(alphas[t])
            for i in range(A[0]):
                alphas[t][i] *= c_t
            cs.append(c_t)
        betas[O[0]-1] = A[0]*[cs[O[0]-1]]
        for t in range(O[0]-2, -1, -1):
            for i in range(A[0]):
                betas[t][i] = 0
                for j in range(A[0]):
                    betas[t][i] += betas[t+1][j]*B[j*B[1]+O[t+2]+2]*A[i*A[1]+j+2]
                betas[t][i] *= cs[t]

        #digamma, descaled
        for t in range(0, O[0]-1):
            for i in range(A[0]):
                s = 0
                for j in range(A[0]):
                    s1 = (alphas[t][i]*A[i*A[1]+j+2]*B[j*B[1]+O[t+2]+2]*betas[t+1][j])
                    di_gammas[t][i][j] = s1
                    s += s1
                gammas[t][i] = s
        gammas.append(alphas[O[0]-1])

        for i in range(A[0]):
            pi[i+2] = gammas[0][i]
        for i in range(A[0]):
            s = 0
            for t in range(O[0]-1):
                s += gammas[t][i]
            for j in range(A[0]):
                s33 = 0
                for t in range(O[0]-1):
                    s33 += di_gammas[t][i][j]
                A[i*A[0]+j+2] = s33 /s
            for k in range(B[1]):
                s1 = 0
                for t in range(O[0]-1):
                    if(O[t+1]==k):
                        s1 += gammas[t][i]
                B[i*B[1]+k+2] = s1/s
                if (B[i*B[1]+k+2]==0):
                    B[i*B[1]+k+2] += 0.00001
    return [A,B,pi]


#
#
#
# A, B, pi = init(4,3)
# O = [8, 0,1,2,1,0,2,0,1]
# print(baum(A, B, pi, O))
