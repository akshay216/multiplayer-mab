from math import log2,modf,sqrt
import random
import dbm_with_escaling
import dbm
import time
import numpy as np 

n=1

#number of users
M=5

#number of arms
N=5

#Total time horizon
T=100000

t = 0

#index
g=[[0 for i in range(N)] for j in range(M)] #size M X N

#playingPairCount[j][i] is the number of times user j plays arm i
playingPairCount=[[0 for i in range(N)] for j in range(M)] #size M X N

#k[i] is arm to be played next by user i
k=[i for i in range(M)]

#prevk[i] is last arm played by user i and is currently on it
prevk=[i for i in range(M)]

#playingCount[i] is no. of times user i has played
playingCount = [0 for i in range(M)]

#reward[j][i] is the total sum of rewards obtained uptill now when user j played arm i
reward =[[0 for i in range(N)] for j in range(M)] #size M X N

#distribution[j][i] is the probability that user j gets reward when it plays arm i
#distribution=[[1/((i+1)*(j+1)) for i in range(N)] for j in range(M)] #size M X N
'''
distribution = [[0.3,0.1,0.5,0.4,0.2],
 [0.4,0.2,0.7,0.4,0.1],
 [0.8,0.4,0.2,0.4,0.1],
 [0.5,0.6,0.2,0.1,0.4],
 [0.1,0.7,0.5,0.3,0.6]]
 '''


distribution = [[0.4,0.1,0.5,0.4,0.2],
 [0.9,0.2,0.7,0.4,0.1],
 [0.2,0.4,0.2,0.4,0.1],
 [0.75,0.6,0.2,0.1,0.4],
 [0.1,0.7,0.5,0.3,0.6]] 

#pairReward[a][b][c] is the reward obrained when user a plays arm b at time c
pairReward=[[[0 for i in range(T+1)] for j in range(N)] for k in range(M)] #size M x N x T


def Initialization():
    global t
    for i in range(M): #pick a user from M users sequentially
        for j in range(N): #pick an arm from N arms sequentially for user i
            reward[i][j]=pairReward[i][j][t]
            playingCount[i]+=1 #increment playingCount for user i
            playingPairCount[i][j]+=1 #increment playingPairCount for the pair - user i and arm j
            t = t + 1 #increment t
    g = CalculateIndex() #update indices
    #prevk = [i for i in range(M)] #assume initially user i is on arm i for all M users
    prevk = np.random.permutation(M).tolist()
    print() 
    print()

    '''
    for i in range(M):
        k[i]=BipartiteMatching(g,i,prevk)
        prevk[i]=k[i]
    '''

def Reward():
    for i in range(M): #pick a user from M users sequentially
        for j in range(N): #pick an arm from N arms sequentially for user i
            for t in range(T): 
                randNumber=random.randint(0,100) #Returns a random integer N such that 0 <= N <= 100
                #calculates pairReward[i][j][t] using Montecarlo Simulation
                if randNumber >= int(distribution[i][j]*100): 
                    pairReward[i][j][t]=0
                else:
                    pairReward[i][j][t]=1

                #print('pairReward at i, j, t: ', i, j, t, ' = ', pairReward[i][j][t])

def CalculateIndex():
    for i in range(M): #pick a user from M users sequentially
        #print("Playing count for i = ", i, ' = ', playingCount[i])
        for j in range(N): #pick an arm from N arms sequentially for user i
            g[i][j]=(reward[i][j]/playingPairCount[i][j]) + sqrt( (M+2) * log2(playingCount[i]) / playingPairCount[i][j])
            #print("Playing Pair count for i = ", i, ' and j = ', j, ' = ', playingPairCount[i][j])
            #calculate index g for every pair using ducb4 index formula
    return g


#The Code written below represents the main() function. The execution starts here.
Reward() #calculates pairReward
Initialization() #initialization phase
print('Assignments at t = ', t, 'are', prevk)

while t<T:
#while(1):
    log=log2(n)
    #print('n = ',n) #calculates value of p
    logFrac,_= modf(log)
    #print ("log = ", log, "logfrac = ", logFrac) #returns decimal part of log
    if logFrac==0: #checks if decimal part of log is 0 which is possible only when n is a power of 2
        #Exploration Phase

        g=CalculateIndex() #update indices
        #print("Exploration at ", t)
        #print("g  = ")
        #for index in g:
           #print(index)
        #print()
        #k = dbm_with_escaling.DBM(g, prevk, M, N) #run DBM algorithm
        k = dbm.DBM(g, prevk, M, N)
        if (k != prevk): #checks if newly calculated matching is different from current matching
            #print('Matching has changed!')
            #print("k = ", k, "prevk = ", prevk)
            n = 1 #reset n=1 if matching changes
            #print("n  = ", n)
    else: #Exploitation Phase
        #print("Exploitation at ", t)
        #break
        k = prevk #keep matching as it is

    for i in range(M): #pick a user from M users sequentially
        reward[i][k[i]] = reward[i][k[i]] + pairReward[i][k[i]][t] #sums reward obtained when user i plays arm k[i] uptill time t
        playingCount[i]+=1 #increment playingCount for user i
        playingPairCount[i][k[i]]+=1 #incrment playingPairCount for the pair - user i and arm k[i]
        prevk[i]=k[i] #prevk[i] becomes k[i] since k[i] has been played ny user i 
    n+=1
    t+=1
    print('Assignments at t = ', t, 'are', k)
    #print()
    #print()
    #print()
    
#print("assignments = ", k)
#for index in g:
#    print(index)


    #time.sleep(0.01)
