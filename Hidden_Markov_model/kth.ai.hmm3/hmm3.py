__author__      =  "Hamza BENJELLOUN & Omar BENCHEKROUN"

from util import *
from math import inf, log
class Hmm:
    def __init__(self, A, B, pi):
        assert A[0] == A[1]
        assert A[0] == B[0]
        assert pi[1] == A[0]
        assert pi[0] == 1
        self.A = A
        self.B = B
        self.pi = pi
        self.N = A[0]
        self.M = B[1]
    def forward(self, O):
        alpha_t = [self.pi[i+2]*self.B[i*self.M + O[1] + 2] for i in range(self.N)]
        for t in range(1, O[0]):
            alpha_t_prev = [tmp for tmp in alpha_t]
            for i in range(self.N):
                alpha_t_i = 0
                for j in range(self.N):
                    alpha_t_i += alpha_t_prev[j]*self.A[j*self.N+i+2]
                alpha_t_i *= self.B[i*self.M+O[t+1]+2]
            alpha_t[i] = alpha_t_i
        return alpha_t

    def baum_welch(self, O, maxIters = 30):
        # initialisation
        alphas = [self.N*[0] for _ in range(O[0])]
        betas = [self.N*[0] for _ in range(O[0])]
        di_gammas = [[self.N*[0] for _ in range(self.N)] for i in range(O[0]-1)]
        gammas = [self.N*[0] for _ in range(O[0])]

        cpt=0
        old_log_prob = -inf
        log_prob = -inf
        while(cpt < maxIters):
            #compute alphas
            for i in range(self.N):
                alphas[0][i] = self.pi[i+2]*self.B[i*self.M+O[1]+2]
            c_0 = 1/sum(alphas[0])
            for i in range(self.N):
                alphas[0][i] *= c_0
            cs = [c_0]
            for t in range(1, O[0]):
                for i in range(self.N):
                    alphas[t][i] = sum([alphas[t-1][j]*self.A[j*self.N+i+2] for j in range(self.N)]) * self.B[i*self.M+O[t+1]+2]
                c_t = 1/sum(alphas[t])
                for i in range(self.N):
                    alphas[t][i] *= c_t
                cs.append(c_t)
            #compute Betas
            betas[O[0]-1] = self.N*[cs[O[0]-1]]
            for t in range(O[0]-2, -1, -1):
                for i in range(self.N):
                    betas[t][i] = 0
                    for j in range(self.N):
                        betas[t][i] += betas[t+1][j]*self.B[j*self.M+O[t+2]+2]*self.A[i*self.N+j+2]
                    betas[t][i] *= cs[t]

            #compute digamma and gamma
            for t in range(0, O[0]-1):
                for i in range(self.N):
                    s = 0
                    for j in range(self.N):
                        s1 = (alphas[t][i]*self.A[i*self.N+j+2]*self.B[j*self.M+O[t+2]+2]*betas[t+1][j])
                        di_gammas[t][i][j] = s1
                        s += s1
                    gammas[t][i] = s
            gammas.append(alphas[O[0]-1])
            # reestimation of A, B, pi
            for i in range(self.N):
                self.pi[i+2] = gammas[0][i]
            for i in range(self.N):
                denominator = 0
                for t in range(O[0]-1):
                    denominator += gammas[t][i]
                for j in range(self.N):
                    A_Numerator = 0
                    for t in range(O[0]-1):
                        A_Numerator += di_gammas[t][i][j]
                    self.A[i*self.N+j+2] = A_Numerator /denominator
                for k in range(self.M):
                    B_Numerator = 0
                    for t in range(O[0]-1):
                        if(O[t+1] == k):
                            B_Numerator += gammas[t][i]
                    self.B[i*self.M+k+2] = B_Numerator/denominator
            # test of convergence
            log_prob = -sum(log(c) for c in cs)
            if(log_prob < old_log_prob):
                break
            old_log_prob = log_prob
            cpt += 1






def main():
    A, B, pi, O = extract_matrix()
    hmm = Hmm(A, B, pi)
    hmm.baum_welch(O)
    print(mat2str(hmm.A))
    print(mat2str(hmm.B))

main()
