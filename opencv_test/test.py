import numpy as np
from numpy.linalg import norm

line2 = [[1186, 340], [1568, 999]]
line3 = [[1201, 336], [1595, 1002]]

current_point = (1367, 667)
previous_point = (1408, 669)

def distance_of_point_and_line(line, point):
    p1, p2 = np.array(line)
    p3 = np.array(point)
    distance = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)
    print(distance)

distance_of_point_and_line(line2, current_point)
distance_of_point_and_line(line3, current_point)
distance_of_point_and_line(line2, previous_point)
distance_of_point_and_line(line3, previous_point)