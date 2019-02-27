import matplotlib.pyplot as plt
import math

fig = plt.figure()

with open('data.txt') as file:
    inp = file.read().split('\n')

SCAN_ENC_CPR = 200 # number of angle measurements per second

# calculates angle measurement, necessary because angle and distance are measured at different times
def process_ray(ray, ray_prev, ray_next):
    if ray == None or ray_prev == None or ray_next == None:
        return
    else:
        try:
            count_delta = int(ray_next[3]) - int(ray[3])
            if count_delta == 0:
                count_delta = int(ray[3]) - int (ray_prev[3])
            time_offset = int(ray[1]) - int(ray[3])
            new_count = (int(ray[2]) + time_offset / count_delta) % SCAN_ENC_CPR
            angle = 2 * math.pi * new_count / SCAN_ENC_CPR
            ray.append(angle)
            return ray
        except:
            print("formatting error detected")
        

def euclidean_dist(ray_one, ray_two):
    pt_one = [float(ray_one[0]) * math.cos(ray_one[4]), float(ray_one[0]) * math.sin(ray_one[4])]
    pt_two = [float(ray_two[0]) * math.cos(ray_two[4]), float(ray_two[0]) * math.sin(ray_two[4])]
    return math.sqrt((pt_one[0] - pt_two[0]) ** 2 + (pt_one[1] - pt_two[1]) ** 2)

NUM_SURR_POINTS = 20 # number of points used to calculate avg distance from neighboring points
NOISE_CUTOFF = 1.1 # cutoff probability that a point is a noise point
# https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0201280
def remove_noise(rays):
    cleaned_rays = []
    for ray in rays:
        closest_rays = []
        greatest_dist = None
        for num, other_ray in enumerate(rays):
            if ray != other_ray:
                dist_temp = euclidean_dist(ray, other_ray)
                if len(closest_rays) < NUM_SURR_POINTS:
                    closest_rays.append(dist_temp)
                elif greatest_dist == None:
                    closest_rays.append(dist_temp)
                    greatest_dist = dist_temp
                elif dist_temp < greatest_dist:
                    closest_rays[closest_rays.index(greatest_dist)] = dist_temp
                    greatest_dist = max(closest_rays)
        avg = sum(closest_rays) / len(closest_rays)
        ray.append(avg)
    global_avg = sum(i[5] for i in rays) / len(rays)
    for ray in rays:
        local_density = ray[5] / global_avg
        if local_density <= NOISE_CUTOFF:
            cleaned_rays.append(ray)
    return cleaned_rays

# Ray format: [dist=0,  distance measurement
#              time=1,  time that distance was measured 
#              count=2,    number of angle measurements before time measurements
#              ctime=3,    time of most recent angle measurement
#              angle=4]    most recent angle measurement (what we need to calculate)
ray = None
prev_ray = None
next_ray = None
processed_data = []
for i in inp:
    next_ray = i.strip().split(',')
    processed_ray = process_ray(ray, prev_ray, next_ray)
    prev_ray = ray
    ray = next_ray
    if processed_ray != None: processed_data.append(processed_ray)

clean_data = remove_noise(processed_data) 

for ray in clean_data:
    plt.scatter(float(ray[0]) * math.cos(ray[4]), float(ray[0]) * math.sin(ray[4]), c='black', s=.5)
plt.scatter(0, 0, c='red', s=10)
plt.show()