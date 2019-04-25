from random import randint

def find_reward(probability):
	probability = probability * 100
	random_number = randint(0, 99)
	if (random_number >= probability):
		return 0
	else:
		return 1