
# coding: utf-8

# In[7]:

from random import randint
import bernoulli_reward


def CFL(c,users,time_slots, sample_count, observed_mean, reward_distribution):      #defining CFL . Passing parameters are: c-no of channels , users-no of users , time_slots
    b=0.1
    p = [[1/c for i in range(0,c)] for j in range(0,users)]  #matrix for probability of each user selecting a particular channel .
    selections = [-1 for i in range(0,users)]   # list that will store channels selected by each user in a particular time slot.
                                                #-1 in selection denotes that no channel is selected.
    allocations = [-1 for i in range(0,users)] # it will store the final selections which has no collisions.
    while(time_slots < c):
        print("time slot : ",time_slots)
        for u in range(0,users):    # 'u' is the iterator for users
            channelNumber=0
            while channelNumber < c:
                randNumber1 = randint(0,100)   # generating a random number to check chances of a channel to get selected
                
                if randNumber1 < p[u][channelNumber]*100 :
                    #channel is selected
                    selections[u]=channelNumber
                    break
                    
                channelNumber=channelNumber+1
        
        print("selection of each user : ",selections)
              
              
              
        # To check collisions      
        count = [0 for i in range(0,c)]  # it stores number of users wanting same channel
        colliding_channels=[]           # it stores list of channels colliding
        for u in range(0,users):
            if selections[u] !=-1:
                count[selections[u]]+=1
        
        for i in range(0,c):
            if count[i] >1:     # checks if a count of users wanting a channel is more than 1 than there is collision
                colliding_channels.append(i)
              
                    
        
        print("collinding channels : ",colliding_channels)
        
        for u in range(0,users):
            channelNumber = selections[u]
            if selections[u] in colliding_channels:  # if selection of user belongs to 'colliding_channels' list then failure else success
                #failure
                    
                p[u][channelNumber] = (1-b)*p[u][channelNumber]
                for j in range(0,c):
                    if j!=channelNumber:
                        p[u][j] = ( (1-b)*p[u][j] ) + ( b/(c-1) ) 
                
                
                ### increment no of times user 'u' played on channel 'channelNumber', reward 0 
                '''
                sample_count[u][channelNumber] = sample_count[u][channelNumber] + 1
                print('updating sample count of (u, channelNumber)', u, channelNumber)
                print(sample_count[u])
                observed_mean[u][channelNumber] = (observed_mean[u][channelNumber]  * (sample_count[u][channelNumber] - 1))/sample_count[u][channelNumber]
                print('updating observed_mean of (u, channelNumber)', u, channelNumber)
                print(observed_mean[u])
                '''
            elif selections[u] != -1:  # checks if any channel is selected by user 'u' or not , if a channel is selected then success
                #success
                
                p[u] = [0 for j in range(0,c)]     
                p[u][channelNumber]=1

            time_slots+=1
                


            ### generate reward for user 'u' on channel 'channelNumber' acc to prob distribution
            '''
                instantanious_reward = bernoulli_reward.find_reward(reward_distribution[u][channelNumber])
                print('instantanious_reward:', instantanious_reward)
                ### increment no of times user 'u' played on channel 'channelNumber'
                sample_count[u][channelNumber] = sample_count[u][channelNumber] + 1
                print('updating sample count of (u, channelNumber)', u, channelNumber)
                print(sample_count[u])
                ### add reward to mean reward
                observed_mean[u][channelNumber] = (observed_mean[u][channelNumber]*(sample_count[u][channelNumber]-1) + instantanious_reward)/sample_count[u][channelNumber]
                print('updating observed_mean of (u, channelNumber)', u, channelNumber)
                print(observed_mean[u])
            '''
        
        #time_slots+=1

                
        '''
        for p1 in p:
            print (p1)
        '''
        print()
        print()
        #if -1 not in selections and len(colliding_channels) == 0 :
        

    return selections,time_slots
        
 

 ##MAIN 

   
time_slots=0
c=5
users=4
reward_distribution =  [[0.3,0.1,0.5,0.4,0.2],
 [0.4,0.2,0.7,0.4,0.1],
 [0.8,0.4,0.2,0.4,0.1],
 [0.5,0.6,0.2,0.1,0.4]]
 #[0.1,0.7,0.5,0.3,0.6] 
observed_mean = [[0.1*randint(0, 8) for i in range(c)] for i in range(users)]
sample_count = [[1 for i in range(c)] for j in range(users)]

'''
print('Initial observed_mean:')
for mean in observed_mean:
    print(mean)

print('Initial Sample count')
for sample in sample_count:
    print(sample)
'''


allocations, time_slots = CFL(c ,users,0, sample_count, observed_mean, reward_distribution)


'''

print('Observed mean after CFL')
for mean in observed_mean:
    print(mean)

print()
print('Sample count after CFL')
for sample in sample_count:
    print(sample)
'''

print("final allocations : ",allocations)
print("time slots : ",time_slots)



# In[ ]:






# In[ ]:
