from math import log, sqrt
from random import randint
import bernoulli_reward
import cfl
import initiation

number_of_users = 5

number_of_channels = 5

Tsf = 2 + 2*(number_of_channels-1)

T = 1000000

time_slots_so_far = 0

sample_count = [[0 for j in range(number_of_channels)] for i in range(number_of_users)]

observed_mean = [[0 for j in range(number_of_channels)] for i in range(number_of_users)]

assignments = [i for i in range(number_of_users)]

flags = [0 for i in range(number_of_users)]

reward_distribution =  [[0.4,0.1,0.5,0.4,0.2],
 [0.9,0.2,0.7,0.4,0.1],
 [0.2,0.4,0.2,0.4,0.1],
 [0.75,0.6,0.2,0.1,0.4],
 [0.1,0.7,0.5,0.3,0.6]] 

epsilon = 1/number_of_channels

initiator = -1
responder = -1
preference = -1

def beginning_of_SF(t, Tsf):
	if (t % Tsf == 1):
		return True
	else:
		return False


def calculate_UCB_indices(observed_mean, sample_count, t, number_of_users, number_of_channels):
	ucb_indices = [[] for i in range(number_of_users)]
	for i in range(number_of_users):
		for j in range(number_of_channels):
			index = observed_mean[i][j] + sqrt((2*log(t))/sample_count[i][j])
			ucb_indices[i].append(index)
	return ucb_indices

def find_preferred_channels(assignments, ucb_indices, number_of_users, number_of_channels):
	preferred_channels = [[] for i in range(number_of_users)]
	for i in range(number_of_users):
		for j in range(number_of_channels):
			if (ucb_indices[i][j] > ucb_indices[i][assignments[i]]):
				preferred_channels[i].append(j)
		def ucb_index(channel):
			return ucb_indices[i][channel]
		preferred_channels[i] = sorted(preferred_channels[i], key = ucb_index, reverse = True)
	return preferred_channels


def rank_channels(assignments, observed_mean, sample_count, t, number_of_users, number_of_channels):
	ucb_indices = calculate_UCB_indices(observed_mean, sample_count, t, number_of_users, number_of_channels)
	preferred_channels = find_preferred_channels(assignments, ucb_indices, number_of_users, number_of_channels)
	return preferred_channels, ucb_indices

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

def find_initiator(flags, number_of_users):
	for i in range(len(flags)):
		if (flags[i] == 1):
			return i
	return 0


def owner(channel, assignments):
	for i in range(len(assignments)):
		if (assignments[i] == channel):
			return i	
	return -1

def propose_swap(responder, ucb_indices, initiator, assignments):
	if (responder == -1):
		return True
	elif (ucb_indices[responder][assignments[initiator]] > ucb_indices[responder][assignments[responder]]):
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

def execute_actions(assignments, reward_distribution, initiator, responder, t, Tsf, number_of_users, number_of_channels):
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


def reset(number_of_users):
	return -1, -1, [0 for i in range(number_of_users)]


#Main
initiation.initiate_assignments(number_of_users, number_of_channels, sample_count, observed_mean, reward_distribution)
time_slots_so_far = number_of_channels
assignments, time_slots_so_far = cfl.CFL(number_of_channels, number_of_users, time_slots_so_far, sample_count, observed_mean, reward_distribution)

for t in range(time_slots_so_far, T, 1):
	_, responder, _ = reset(number_of_users)
	if (beginning_of_SF(t, Tsf)):
		print('Assignments at t = ', t, 'are', assignments)
		initiator, responder, flags = reset(number_of_users)
		preferred_channels, ucb_indices = rank_channels(assignments, observed_mean, sample_count, t, number_of_users, number_of_channels)
		for i in range(number_of_users):
			if (len(preferred_channels[i]) != 0):
				flags[i] = calculate_flag(epsilon)
		if (not flag_collision(flags)):
			initiator = find_initiator(flags, number_of_users)
			preference = 0

	else:
		if (initiator != -1 and preference != -1 and preference < len(preferred_channels[initiator])):
			responder = owner(preferred_channels[initiator][preference], assignments)
			response = propose_swap(responder, ucb_indices, initiator, assignments)
			if (response == True):
				swap(preferred_channels[initiator][preference], initiator, assignments)
				preference = -1
			else:
				preference = preference + 1
	rewards = execute_actions(assignments, reward_distribution, initiator, responder, t, Tsf, number_of_users, number_of_channels)
	update_stats(rewards, observed_mean, sample_count, number_of_users, assignments, t, Tsf)
#
