
def LoadGCode(filename, offsetx, offsety):
	file_obj = open(filename, "r")
	list_of_line = file_obj.readlines()
	list_of_gcode = []
	z = 0
	list_of_point = []
	for ls in list_of_line:
		if ("G1" in ls) or ("M300" in ls):
			list_of_gcode.append(ls)

	for ls in list_of_gcode:
		if "M300" in ls:
			ls_split_space = ls.split(" ")
			if ls_split_space[1] == "S30.00":
				z = 1
			elif(ls_split_space[1] == "S50.00"):
				z = 0
		if "G1" in ls:
			ls_split_space = ls.split(" ")
			x = offsetx + float(ls_split_space[1][1:])
			y = offsety + float(ls_split_space[2][1:])
			list_of_point.append([x, y, z])
	return list_of_point


ls  = LoadGCode("robotsm6.gcode", 0, 0)
# print(ls)
for i in ls:
	print(i)





		