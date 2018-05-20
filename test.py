def Cal_Sol(sol):
		result = [1]*2
		if sol % 2:
			result[0] = 1
		else:
			result[0] = -1
		if sol > 1 and sol < 4:
			result[1] = -1
		return result

print(Cal_Sol(4))