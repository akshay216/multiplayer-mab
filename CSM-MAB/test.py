from random import randint
import bernoulli_reward
from math import log, sqrt
import time



def beginning_of_SF(t, Tsf):
	if (t % Tsf == 1):
		return True
	else:
		return False


def calculate_flag(epsilon):
	if (randint(0, 10) >= epsilon * 10):
		return 0
	else:
		return 1

def flag_collision(flags):
	if (sum(flags) > 1 or sum(flags) == 0):
		return True
	else:
		False


def find_preferred_channels(assignments, ucb_indices, number_of_users, number_of_channels):
	preferred_channels = [[] for i in range(number_of_users)]
	#print(preferred_channels)
	for i in range(number_of_users):
		print('User:', i)
		print('Ucb indices:', ucb_indices[i])
		for j in range(number_of_channels):
			if (ucb_indices[i][j] > ucb_indices[i][assignments[i]]):
				preferred_channels[i].append(j)
		def ucb_index(channel):
			return ucb_indices[i][channel]
		print('assigned arm:', assignments[i])
		print('before sorting:', preferred_channels[i])
		preferred_channels[i] = sorted(preferred_channels[i], key = ucb_index, reverse = True)
		print('after sorting:', preferred_channels[i])
		#print()
	return preferred_channels


def find_initiator(flags, number_of_users):
	for i in range(len(flags)):
		if (flags[i] == 1):
			return i
	else:
		return 0

def owner(channel, assignments):
	for i in range(len(assignments)):
		if (assignments[i] == channel):
			return i	
	return -1


def propose_swap(responder, ucb_indices, initiator, assignments):
	if (ucb_indices[responder][assignments[initiator]] > ucb_indices[responder][assignments[responder]]):
		return True
	else:
		return False

def swap(preferred_channel, initiator, assignments):
	responder = owner(preferred_channel, assignments)
	if (responder == -1):
		assignments[initiator] = preferred_channel
	else:
		temp = assignments[initiator]
		assignments[initiator] = assignments[responder]
		assignments[responder] = temp

def reset(number_of_users):
	return -1, -1, [0 for i in range(number_of_users)]



def calculate_UCB_indices(observed_mean, sample_count, t, number_of_users, number_of_channels):
	ucb_indices = [[] for i in range(number_of_users)]
	for i in range(number_of_users):
		for j in range(number_of_channels):
			index = observed_mean[i][j] + sqrt((2*log(t))/sample_count[i][j])
			ucb_indices[i].append(index)
	return ucb_indices



def rank_channels(assignments, observed_mean, sample_count, t, number_of_users, number_of_channels):
	ucb_indices = calculate_UCB_indices(observed_mean, sample_count, t, number_of_users, number_of_channels)
	preferred_channels = find_preferred_channels(assignments, ucb_indices, number_of_users, number_of_channels)
	return preferred_channels, ucb_indices



def execute_actions(assignments, reward_distribution, initiator, responder, t, Tsf, number_of_users):
		if (beginning_of_SF(t, Tsf)):
			return []
		rewards = []
		for i in range(number_of_users):
			if (i != initiator and i != responder):
				instantanious_reward = bernoulli_reward.find_reward(reward_distribution[i][assignments[i]])
			else:
				instantanious_reward = -1
			rewards.append(instantanious_reward)
		return rewards
###


def update_stats(rewards, observed_mean, sample_count, number_of_users, assignments, t, Tsf):
	if (beginning_of_SF(t, Tsf)):
		return
	for i in range(number_of_users):
		if (rewards[i] == -1):
			continue
		else:
			assigned_arm = assignments[i]
			sample_count[i][assigned_arm] = sample_count[i][assigned_arm] + 1
			observed_mean[i][assigned_arm] = (observed_mean[i][assigned_arm]*(sample_count[i][assigned_arm]-1) + rewards[i])/sample_count[i][assigned_arm]




########################################################



number_of_users = 5

number_of_channels = 5

epsilon = 1/number_of_channels

Tsf = 1 + (number_of_channels-1)

flags = [0 for i in range(number_of_users)]

initiator = -1
responder = -1
preference = -1

assignments = [0, 1, 2, 3, 4]


'''
ucb_indices =[[0.3,0.1,0.5,0.4,0.2, 0.6],
 [0.4,0.2,0.7,0.4,0.1, 0.9],
 [0.8,0.4,0.2,0.4,0.1, 0.1],
 [0.5,0.6,0.2,0.1,0.4, 0.3],
 [0.1,0.7,0.5,0.3,0.6, 0.5]]
'''




reward_distribution =  [[0.3,0.1,0.5,0.4,0.2],
 [0.4,0.2,0.7,0.4,0.1],
 [0.8,0.4,0.2,0.4,0.1],
 [0.5,0.6,0.2,0.1,0.4],
 [0.1,0.7,0.5,0.3,0.6]] 

observed_mean = [[0.1*randint(0, 8) for i in range(number_of_channels)] for i in range(number_of_users)]
sample_count = [[1 for i in range(number_of_channels)] for j in range(number_of_users)]


'''
for ucb_index in ucb_indices:
	print(ucb_index)
print()
'''

#preferred_channels = find_preferred_channels(assignments, ucb_indices, number_of_users, number_of_channels)

'''
for channel in preferred_channels:
	print(channel)
print()
'''


for t  in range(1, 50, 2):
	_, responder, _ = reset(number_of_users)
	if (beginning_of_SF(t, Tsf)):
		time.sleep(0.5)
		print()
		print()
		print()
		print()
		print()
		print("Miniframe S1 & S2 started at t = ", t)
		print("assignments:", assignments)
		#print('preferred_channels:', preferred_channels)
		initiator, responder, flags = reset(number_of_users)

		preferred_channels, ucb_indices = rank_channels(assignments, observed_mean, sample_count, t, number_of_users, number_of_channels)
		print('preferred_channels:')
		for channel in preferred_channels:
			print(channel)
		#print()
		print('Ucb_indices:')
		for index in ucb_indices:
			print(index)

		#print()



		for i in range(number_of_users):
			if (len(preferred_channels[i])!= 0):
				flags[i] = calculate_flag(epsilon)

		print('flags:', flags)
		#print()

		if (not flag_collision(flags)):
			initiator = find_initiator(flags, number_of_users)
			preference = 0
			print('initiator:', initiator, 'preferred_channel:', preferred_channels[initiator][preference])
			print('Ucb_index of initiator', ucb_indices[initiator])
	else:
		print()
		print("Miniframe S3 & S4 started at t = ", t)
		if (initiator != -1 and preference != -1 and preference < len(preferred_channels[initiator])):
			print('initiator:', initiator, 'preferred_channel:', preferred_channels[initiator][preference], 'preference:', preference)
			responder = owner(preferred_channels[initiator][preference], assignments)
			print('responder:', responder)
			response = propose_swap(responder, ucb_indices, initiator, assignments)
			print('respone:', response)
			if (response == True):
				swap(preferred_channels[initiator][preference], initiator, assignments)
				print('Ucb_index of responder', ucb_indices[responder])
				preference, _, _ = reset(number_of_users)
				#responder, _, _ = reset(number_of_users)
			else:
				print('Ucb_index of responder', ucb_indices[responder])
				preference = preference + 1
				#responder, _, _ = reset(number_of_users)

			print('new_preference:', preference)
			print('new responder:', preference)


		if (initiator == -1):
			print('no initiator')
	print('initiator:', initiator)
	print('responder:', responder)
	rewards = execute_actions(assignments, reward_distribution, initiator, responder, t, Tsf, number_of_users)
	print('reward obtained:', rewards)
	#print()
	update_stats(rewards, observed_mean, sample_count, number_of_users, assignments, t, Tsf)
	print('assignments', assignments)
	#print()
	print('update observed mean: ')
	for mean in observed_mean:
		print(mean)
	#print()
	print('updated sample count')
	for count in sample_count:
		print(count)



for mean in observed_mean:
	print(mean)

print()
print()
for dist in reward_distribution:
	print(dist)







			#
		#
	#






