import matplotlib.pyplot as plt
import math

fig = plt.figure()

with open('data2.txt') as file:
    inp = file.read().split('\n')

SCAN_ENC_CPR = 200 # number of angle measurements per second

# calculates angle measurement, necessary because angle and istance are measured at different times
def process_ray(ray, ray_prev, ray_next):
    if ray == None or ray_prev == None or ray_next == None:
        return
    else:
        count_delta = int(ray_next[3]) - int(ray[3])
        if count_delta == 0:
            count_delta = int(ray[3]) - int (ray_prev[3])
        time_offset = int(ray[1]) - int(ray[3])
        new_count = (int(ray[2]) + time_offset / count_delta) % SCAN_ENC_CPR
        angle = 2 * math.pi * new_count / SCAN_ENC_CPR
        plt.scatter(float(ray[0]) * math.cos(angle), float(ray[0]) * math.sin(angle), c='black', s=.5)

# Ray format: [dist=0,  distance measurement
#              time=1,  time that distance was measured 
#              count=2,    number of angle measurements before time measurements
#              ctime=3,    time of most recent angle measurement
#              angle=4]    most recent angle measurement (what we need to calculate)
ray = None
prev_ray = None
next_ray = None
for i in inp:
    next_ray = i.strip().split(',')
    process_ray(ray, prev_ray, next_ray)
    prev_ray = ray
    ray = next_ray
plt.scatter(0, 0, c='red', s=10)
plt.show()