#!/usr/bin/env python3
__author__      =  "Hamza BENJELLOUN & Omar BENCHEKROUN"

from player_controller_hmm import PlayerControllerHMMAbstract
from constants import *




from math import inf, log
import random
class Hmm:
    def __init__(self, N, M):
        self.A, self.B, self.pi = self.initialization(N, M)
        self.N = self.A[0]
        self.M = self.B[1]


    def initialization(self, N, M):
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
        return sum(alpha_t)


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
                    if (self.B[i*self.M+k+2]==0):
                        self.B[i*self.M+k+2] += 0.0001
            # test of convergence
            log_prob = -sum(log(c) for c in cs)
            #if(log_prob < old_log_prob):
            #    break
            old_log_prob = log_prob
            cpt += 1





class PlayerControllerHMM(PlayerControllerHMMAbstract):
    def init_parameters(self):
        """
        In this function you should initialize the parameters you will need,
        such as the initialization of models, or fishes, among others.
        """
        self.allObservations = []
        self.hmms = []
        self.compteur = 0
        self.type = -1
        self.dict = {}
        self.allfishes = [i for i in range(N_FISH)]
        self.listfishes = [i for i in range(20)]
        self.probas = []
    def guess(self, step, observations):
        """
        This method gets called on every iteration, providing observations.
        Here the player should process and store this information,
        and optionally make a guess by returning a tuple containing the fish index and the guess.
        :param step: iteration number
        :param observations: a list of N_FISH observations, encoded as integers
        :return: None or a tuple (fish_id, fish_type)
        """
        self.allObservations.append(observations)
        if(100 < step and len(self.dict.keys()) != N_SPECIES):
            if(len(self.dict.keys()) == 0):
                self.allfishes.pop(0)
                self.listfishes.pop(0)
                return (0, random.randint(0, 6))
            else:
                hmm = Hmm(3, N_EMISSIONS)
                O = [step] + [self.allObservations[k0][fish] for k0 in range(len(self.allObservations)) for fish in self.dict[self.type]]
                hmm.baum_welch(O)
                proba = [hmm.forward([step] + [self.allObservations[k0][fish] for k0 in range(len(self.allObservations))]) for fish in self.listfishes]
                if(len(self.probas) != 0):
                    for i in range(len(proba)):
                        proba[i] = proba[i] + self.probas[i]
                self.probas = proba
                index = self.probas.index(min(self.probas))
                for i in range(N_SPECIES):
                    if(i not in self.dict.keys()):
                        self.allfishes.pop(index)
                        ind = self.listfishes.pop(index)
                        self.probas.pop(index)
                        return (ind, i)
        else:
            if(step == 121):
                for f in range(N_SPECIES):
                    hmm = Hmm(3, N_EMISSIONS)
                    Os = [len(self.dict[f])*step] + [self.allObservations[k0][fish] for k0 in range(len(self.allObservations)) for fish in self.dict[f]]
                    hmm.baum_welch(Os)
                    self.hmms.append(hmm)
            elif(121 < step):
                    if(self.type != -1):
                        Os = [len(self.dict[self.type])*step] + [self.allObservations[k0][fish] for k0 in range(len(self.allObservations)) for fish in self.dict[self.type]]
                        hmm = Hmm(3, N_EMISSIONS)
                        hmm.baum_welch(Os)
                        self.hmms[self.type] = hmm
                        self.type = -1
                        index = self.allfishes.pop()
                    O = [step] + [self.allObservations[k0][index] for k0 in range(len(self.allObservations))]
                    probas = [self.hmms[j].forward(O) for j in range(N_SPECIES)]
                    return(index, probas.index(max(probas)))

    def reveal(self, correct, fish_id, true_type):

        """
        This methods gets called whenever a guess was made.
        It informs the player about the guess result
        and reveals the correct type of that fish.
        :param correct: tells if the guess was correct
        :param fish_id: fish's index
        :param true_type: the correct type of the fish
        :return:
        """
        if(true_type not in self.dict.keys()):
            self.dict[true_type] = [fish_id]
        else:
            self.dict[true_type].append(fish_id)
        self.type = true_type
