#Fuction that returns which user is unhappy, i.e the user hasn't been assigned its best arm.
#Best arm refers to arm with the highest reward.
def check_unhappy(g, k, price, number_of_users, number_of_arms, epsilon):
	#Net reward = (Index of user i with machine k[i]) - (Price or Penalty of playing machine k[i])
	for i in range(number_of_users):
		max_net_reward = g[i][k[i]] - price[k[i]] + epsilon
		for j in range(number_of_arms):
			if g[i][j] - price[j] > max_net_reward:
				return i
	return -1


#Function returns True if all arms have receieved a bid atleast once, and False otherwise. 
def all_received_bids(price, number_of_arms):
	for i in range(number_of_arms):
		if price[i] == 0:
			return False
	return True



#Function finds the arm with the highest net reward for the user i.
def find_best_arm(i, g, k, price, number_of_arms):
	max_net_reward = 0
	best_arm = k[i]
	for j in range(number_of_arms):
		if (g[i][j] - price[j] > max_net_reward):
			max_net_reward = g[i][j] - price[j]
			best_arm = j

	return best_arm

#Function finds the arm with the second highest net reward for the user i.
def find_second_best_arm(i, g, k, price, number_of_arms, best_arm):
	max_net_reward = 0
	second_best_arm  = k[i]
	for j in range(number_of_arms):
		if (j == best_arm):
			continue
		elif(g[i][j] - price[j] > max_net_reward):
			max_net_reward = g[i][j] - price[j]
			second_best_arm = j
	return second_best_arm

#Function returns the owner of the arm referenced by arm_held
def owner(arm_held, number_of_users, k):
	for i in range(number_of_users):
		if (k[i] == arm_held):
			return i
	return -1


#Function exchanges assigns best_arm to unhappy_user, and assigns arm previously held by unhappy_user to owner of the best arm
def exchange_arms(unhappy_user, best_arm, k, number_of_arms, number_of_users):
	owner_of_best_arm = owner(best_arm, number_of_users, k)

	if (owner_of_best_arm != -1):
		unhappy_user_arm = k[unhappy_user]
		k[unhappy_user] = best_arm
		k[owner_of_best_arm] = unhappy_user_arm
	else:
		k[unhappy_user] = best_arm


#Discrete Bipartite matching, in our case, is done using Auction Algorithm. 
#Explanation of Auction Algorithm is provided in the paper enclosed in the mail.

def DBM(g, prevk, number_of_users, number_of_arms):
	#epsilon represents E-complementary slackness. Given on Pg. 4 of the paper.
	epsilon = 0.05

	bid = 0

	#Price can be understood as a penalty for playing arms.
	price = [0 for i in range(number_of_arms)]

	#Values of prevk is copied to a new array, k, so that we don't affect values of prevk, since it was passed as reference from dUCB4.
	k = []
	for i in range(number_of_users):
		k.append(prevk[i])


	#Checking which user is unhappy at the beginning. -1 value indicates all users are happy.
	unhappy_user = check_unhappy(g, k, price, number_of_users, number_of_arms, epsilon)

	#This loop runs until all users are happy
	#This loop terminates as soon as all arms have receieved a bid once.
	while (unhappy_user != -1 and not all_received_bids(price, number_of_arms)):
		
		#Best arm of unhappy user is stored in best_arm
		best_arm = find_best_arm(unhappy_user, g, k, price, number_of_arms)

		#Second best arm of unhappy user is stored in second_best_arm.
		second_best_arm = find_second_best_arm(unhappy_user, g, k, price, number_of_arms, best_arm)

		#Exchange of arms b/w unhappy user and owner of best arm.
		exchange_arms(unhappy_user, best_arm, k, number_of_arms, number_of_users)
		difference_net_rewards = (g[unhappy_user][best_arm] - price[best_arm]) - (g[unhappy_user][second_best_arm] - price[second_best_arm]) 

		bid = difference_net_rewards + epsilon
		price[best_arm]  = price[best_arm] + bid
		unhappy_user = check_unhappy(g, k, price, number_of_users, number_of_arms, epsilon)
	return k


#The Code below is in comments, it was only written for debugging. Triple quotes, along with # symbol represent comments in Python.

'''
g = [[(j+5)/10 for j in range(5)] for i in range(5)]
k = [i for i in range(5)]
number_of_users = 5
number_of_arms = 5

print('Distribution: ')
for index in g:
	print(index)

print('Initial assignments: ', k)
print()

print('Final Assignments: ', DBM(g, k, number_of_users, number_of_arms))
print()

'''
