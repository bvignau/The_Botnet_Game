import matplotlib.pyplot as plt

t=[1,2,3,4,5,6]
t2=[3,2,5,4,3]
t3=[4,8,12,16]

plt.axis([0,6,0,20])
plt.plot(t, 'r--')
plt.plot(t2,'g--')
plt.plot(t3,'bs')

plt.show()