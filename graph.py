from sys import argv
from GlobalFunc import *
import OpenGLControl as DrawRB
from Robot import *
from Trajectory import *
import numpy as np
import matplotlib.pyplot as plt
script, first = argv

trj = Trajectory()
f_point = np.array([220, 310, 70])
e_point = np.array([-100, 430, 260])
trj.SetSpTime(0.1)
trj.SetPoint(f_point, e_point, 30)
points = trj.Calculate()
T  = 0.1 * len(points[1])
t = np.arange(0., T, 0.1)
objRB = Robot()
AllJVar=np.array([[None, None, None, None]])
for p in points[1]:
	p = np.append(p, [objRB.EVars[3], objRB.EVars[4], objRB.EVars[5]])
	JVar = objRB.CalInvPositionEx(p, sol = 4)
	AllJVar = np.append(AllJVar, [JVar[1]], axis = 0)
AllJVar = np.delete(AllJVar, 0, axis = 0)

if first == 'x':
	plt.plot(t, points[1][:, 0], 'r', t, points[1][:,1], 'g--', t, points[1][:, 2], 'b:')
	plt.xlabel('t(s)')
	plt.ylabel('mm')
	plt.title('Đồ thị điểm thao tác theo thời gian')
	plt.legend(['x', 'y', 'z'], loc = 'center right')

elif first == 'xdot':
	plt.plot(t, points[2][:, 0], 'r', t, points[2][:,1], 'g--', t, points[2][:, 2], 'b:')
	plt.xlabel('t(s)')
	plt.ylabel('mm/s')
	plt.title('Đồ thi vận tốc điểm thao tác theo thời gian')
	plt.legend(['vx', 'vy', 'vz'], loc = 'upper right')
elif first == 'xdotdot':
	plt.plot(t, points[3][:, 0], 'r', t, points[3][:,1], 'g--', t, points[3][:, 2], 'b:')
	plt.xlabel('t(s)')
	plt.ylabel('mm/s2')
	plt.title('Đồ thi gia tốc điểm thao tác theo thời gian')
	plt.legend(['ax', 'ay', 'az'], loc = 'upper right')
elif first == 'q':
	# print(len(AllJVar[:, 0]))
	plt.plot(t, AllJVar[:, 0], 'r', t, AllJVar[:, 1], 'g--', t, AllJVar[:, 2], 'b:', t, AllJVar[:, 3])
	plt.xlabel('t(s)')
	plt.ylabel('rad')
	plt.title('Bộ nghiệm thứ 4')
	plt.legend(['q1', 'q2', 'q3', 'q4'], loc = 'center right')

plt.grid()
plt.show()
print(objRB.EVars[3])