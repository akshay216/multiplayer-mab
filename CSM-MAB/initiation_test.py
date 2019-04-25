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
				print('instantanious_reward at collision at timeslot, user, arm, :', t,  i, arm_order[i][t], '=', -1)
			else:
				instantanious_reward = bernoulli_reward.find_reward(reward_distribution[i][arm_order[i][t]])
				print('instantanious_reward for timeslot, user, arm, :', t,  i, arm_order[i][t], '=', instantanious_reward)
				observed_mean[i][arm_order[i][t]] = (observed_mean[i][arm_order[i][t]]*(sample_count[i][arm_order[i][t]]-1) + instantanious_reward)/sample_count[i][arm_order[i][t]]
		print()




def initiate_assignments(number_of_users, number_of_arms, sample_count, observed_mean, reward_distribution):
	number_of_time_slots = number_of_arms
	arm_order = [np.random.permutation(number_of_arms).tolist() for i in range(number_of_users)]
	
	print('arm_order:')
	for arm in arm_order:
		print(arm)
	print()
	

	collision_list = create_collision_list(arm_order, number_of_users, number_of_time_slots)
	print('collision_list')
	print(collision_list)
	print()

	play_arms(arm_order, collision_list, number_of_users, number_of_arms, number_of_time_slots, sample_count, observed_mean, reward_distribution)
	print('observed_mean:')
	for mean in observed_mean:
		print(mean)
	print()


	print('sample_count:')
	for sample in sample_count:
		print(sample)





'''

######	
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
'''