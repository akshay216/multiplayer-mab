import numpy as np
import bernoulli_reward

def create_collision_list(arm_order, number_of_users, number_of_time_slots):
	collision_list = [set() for i in range(number_of_time_slots)]
	for t in range(number_of_time_slots):
		arm_set = set()
		for i in range(number_of_users):
			if (not arm_order[i][t] in arm_set):
				arm_set.add(arm_order[i][t])
			else:
				collision_list[t].add(arm_order[i][t])
	return collision_list


def play_arms(arm_order, collision_list, number_of_users, number_of_arms, number_of_time_slots, sample_count, observed_mean, reward_distribution):
	for i in range(number_of_users):
		for t in range(number_of_time_slots):
			sample_count[i][arm_order[i][t]] += 1
			if (arm_order[i][t] in collision_list[t]):
				observed_mean[i][arm_order[i][t]] = (observed_mean[i][arm_order[i][t]]  * (sample_count[i][arm_order[i][t]] - 1))/sample_count[i][arm_order[i][t]]
			else:
				instantanious_reward = bernoulli_reward.find_reward(reward_distribution[i][arm_order[i][t]])
				observed_mean[i][arm_order[i][t]] = (observed_mean[i][arm_order[i][t]]*(sample_count[i][arm_order[i][t]]-1) + instantanious_reward)/sample_count[i][arm_order[i][t]]




def initiate_assignments(number_of_users, number_of_arms, sample_count, observed_mean, reward_distribution):
	number_of_time_slots = number_of_arms
	arm_order = [np.random.permutation(number_of_arms).tolist() for i in range(number_of_users)]
	collision_list = create_collision_list(arm_order, number_of_users, number_of_time_slots)
	play_arms(arm_order, collision_list, number_of_users, number_of_arms, number_of_time_slots, sample_count, observed_mean, reward_distribution)


	
'''
number_of_users = 5
number_of_arms = 5
reward_distribution =  [[0.3,0.1,0.5,0.4,0.2],
 [0.4,0.2,0.7,0.4,0.1],
 [0.8,0.4,0.2,0.4,0.1],
 [0.5,0.6,0.2,0.1,0.4],
 [0.1,0.7,0.5,0.3,0.6]]


observed_mean = [[0 for i in range(number_of_arms)] for i in range(number_of_users)]
sample_count = [[0 for i in range(number_of_arms)] for j in range(number_of_users)]
initiate_assignments(number_of_users, number_of_arms, sample_count, observed_mean, reward_distribution)
print('Observed Mean')
for mean in observed_mean:
	print(mean)
print()

print('Sample Count')
for sample in sample_count:
	print(sample)
print()
'''



