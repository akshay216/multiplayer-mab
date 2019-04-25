import time

def check_unhappy(g, k, price, number_of_users, number_of_arms):
	for i in range(number_of_users):
		max_net_reward = g[i][k[i]] - price[k[i]]
		for j in range(number_of_arms):
			if g[i][j] - price[j] > max_net_reward:
				return i
	return -1

def find_best_arm(i, g, k, price, number_of_arms):
	max_net_reward = 0
	best_arm = k[i]
	for j in range(number_of_arms):
		if (g[i][j] - price[j] > max_net_reward):
			best_arm = j

	return best_arm

def find_second_best_arm(i, g, k, price, number_of_arms, best_arm):
	max_net_reward = 0
	second_best_arm  = k[i]
	for j in range(number_of_arms):
		if (j == best_arm):
			continue
		elif(g[i][j] - price[j] > max_net_reward):
			second_best_arm = j
	return second_best_arm


def owner(arm, number_of_users, k):
	for i in range(number_of_users):
		if (k[i] == arm):
			return i
	return -1


def exchange_arms(unhappy_user, best_arm, k, number_of_arms, number_of_users):
	owner_of_best_arm = owner(best_arm, number_of_users, k)

	if (owner_of_best_arm != -1):
		print('previous owner of best_arm =', owner_of_best_arm)
		unhappy_user_arm = k[unhappy_user]
		k[unhappy_user] = best_arm
		k[owner_of_best_arm] = unhappy_user
		print('new arm of previous owner of best_arm = ', k[owner_of_best_arm])
	else:
		k[unhappy_user] = best_arm





def DBM(g, prevk, number_of_users, number_of_arms):
	k = []
	bid = 0
	price = [0 for i in range(number_of_arms)]
	for i in range(number_of_users):
		k.append(prevk[i])

	unhappy_user = check_unhappy(g, k, price, number_of_users, number_of_arms)

	while (unhappy_user != -1):
		time.sleep(1)
		print('unhappy_user =', unhappy_user)
		print('prev assigned arm = ', k[unhappy_user])
		best_arm = find_best_arm(unhappy_user, g, k, price, number_of_arms)
		print('best_arm = ', best_arm)
		second_best_arm = find_second_best_arm(unhappy_user, g, k, price, number_of_arms, best_arm)
		print('second_best_arm = ', second_best_arm)
		exchange_arms(unhappy_user, best_arm, k, number_of_arms, number_of_users)
		print('newly assigned arm =', k[unhappy_user])
		print('reward distribution = ', g[unhappy_user])
		print('price of best_arm = ', price[best_arm])
		print('price of second_best_arm = ', price[second_best_arm])
		print('effective reward of best_arm = ', g[unhappy_user][best_arm] - price[best_arm])
		print('effective reward of second_best_arm = ', g[unhappy_user][second_best_arm] - price[second_best_arm])
		bid = (g[unhappy_user][best_arm] - price[best_arm]) - (g[unhappy_user][second_best_arm] - price[second_best_arm])
		print('bid =', bid)
		print('old price of arm', best_arm, '=', price[best_arm])
		price[best_arm]  = price[best_arm] + bid
		print('new price of arm', best_arm, '=', price[best_arm])
		print()
		print()
		unhappy_user = check_unhappy(g, k, price, number_of_users, number_of_arms)






g = [[(j+5)/10 for j in range(5)] for i in range(5)]
'''
g = 

[[9.5, 9.4, 9.3, 9.2, 9.1]
[9.5, 10.4, 9.3, 9.2, 9.1]
[9.5, 9.4, 9.3, 9.2, 12.3]
[9.5, 9.4, 9.3, 11.2, 9.1]
[9.5, 9.4, 19.3, 9.2, 9.1]]
'''


k = [i for i in range(5)]
number_of_users = 5
number_of_arms = 5

price = [0 for i in range(5)]


DBM(g, k, number_of_users, number_of_arms)

for index in g:
	print(index)

print(k)














