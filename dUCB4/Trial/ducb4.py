from math import log2,modf,sqrt
import random
import dbm


n=1

#number of users
M=5

#number of arms
N=5

#time horizon
T=500


t = 0

#index
g=[[0 for i in range(N)] for j in range(M)]

playingPairCount=[[0 for i in range(N)] for j in range(M)]

#assignments
k=[0 for i in range(M)]
prevk=[0 for i in range(M)]
playingCount=[0 for i in range(M)]
reward=[[0 for i in range(N)] for j in range(M)]
distribution=[[1/((i+1)*(j+1)) for i in range(N)] for j in range(M)]
pairReward=[[0 for i in range(T)] for j in range(M*N)]


def Initialization():
    global t
    for i in range(M):
        for j in range(N):
            reward[i][j]=pairReward[i*j][i*j]
            playingCount[i]+=1
            playingPairCount[i][j]+=1
            t = t + 1
    g = CalculateIndex()
    prevk=[i for i in range(M)]
    '''
    for i in range(M):
        k[i]=BipartiteMatching(g,i,prevk)
        prevk[i]=k[i]
    '''

def Reward():
    for i in range(M):
        for j in range(N):
            for t in range(T):
                randNumber=random.randint(0,100)
                #print(randNumber)
                #print(distribution[i][j])
                if randNumber>= int(distribution[i][j]*100):
                    #print('before in if')
                    pairReward[i*j][t]=0
                    #print('after in if')
                else:
                    #print('before in else')
                    pairReward[i*j][t]=1
                    #print('after in else')


def CalculateIndex():
    for i in range(M):
        for j in range(N):
            g[i][j]=reward[i][j]/playingPairCount[i][j] + sqrt((M+2)*log2(playingCount[i])/playingPairCount[i][j])
    return g


Reward()
Initialization()
while t<T:
    log=log2(n)
    logFrac,_= modf(log)
    if logFrac==0:
        g=CalculateIndex()
        k = dbm.DBM(g, prevk, M, N)
        if (k != prevk):
            n = 1
    else:
        k = prevk

    for i in range(M):
        print(i, k[i], i*k[i], t)
        reward[i][k[i]] = reward[i][k[i]] + pairReward[i*k[i]][t]
        playingCount[i]+=1
        playingPairCount[i][k[i]]+=1
        prevk[i]=k[i]

    n+=1
    t+=1
