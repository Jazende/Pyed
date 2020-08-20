def distance_by_values(point_a_x, point_a_y, point_b_x, point_b_y):
    return (abs(point_a_x - point_b_x)**2 + abs(point_a_y-point_b_y)**2)**(1/2)

def distance_by_points(point_a, point_b):
    return distance_by_values(*point_a, *point_b)

if __name__ == '__main__':
    print(distance_by_values(0, 0, 0, 3))
    print(distance_by_values(0, 0, 3, 0))
    print(distance_by_values(0, 0, 4, 3))
    print(distance_by_values(7, 10, 11, 7))