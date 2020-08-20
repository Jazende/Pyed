from math import sin, asin, cos, acos, radians, degrees, sqrt

def deg_sin(angle):
    return sin(radians(angle))

def deg_cos(angle):
    return cos(radians(angle))

def distance_by_values(point_a_x, point_a_y, point_b_x, point_b_y):
    return sqrt(abs(point_a_x - point_b_x)**2 + abs(point_a_y-point_b_y)**2)

def distance_by_points(point_a, point_b):
    return distance_by_values(*point_a, *point_b)

def angle_between_origin_and_positions(self_x, self_y, mouse_x, mouse_y):
    delta_x_mouse = mouse_x - self_x
    delta_y_mouse = mouse_y - self_y
    hypotenuse = sqrt(delta_x_mouse**2 + delta_y_mouse**2)

    cosinus = delta_x_mouse / hypotenuse
    sinus = delta_y_mouse / hypotenuse
    
    cos_angle = degrees(acos(cosinus))
    sin_angle = degrees(asin(sinus))

    if sin_angle < 0:
        cos_angle = (0 - cos_angle) % 360
    
    return cos_angle

def normalize_movement_with_speed(delta_x, delta_y, speed):
    sum_ = delta_x + delta_y
    proportional_x = delta_x / sum_
    proportional_y = delta_y / sum_
    movement_x = proportional_x * speed
    movement_y = proportional_y * speed
    return movement_x, movement_y

def normalize(x, y):
    abs_sum = abs(x) + abs(y)
    if abs_sum == 0:
        return 0, 0
    x, y = x / abs_sum, y / abs_sum
    return x, y

if __name__ == '__main__':
    print(normalize_movement_with_speed(3, 7, 10))
    print(normalize_movement_with_speed(14, 8, 23))
    print(normalize(5, 20))
    print(normalize(-3, 2))
    print(angle_from_origin_and_positions(0, 0, 1, 0))
    print(angle_from_origin_and_positions(0, 0, 1, 0.5))
    print(angle_from_origin_and_positions(0, 0, 1, 1))
    print(angle_from_origin_and_positions(0, 0, 0.5, 1))
    print(angle_from_origin_and_positions(0, 0, 0, 1))
    print(angle_from_origin_and_positions(0, 0, -0.5, 1))
    print(angle_from_origin_and_positions(0, 0, -1, 1))
    print(angle_from_origin_and_positions(0, 0, -1, 0.5))
    print(angle_from_origin_and_positions(0, 0, -1, 0))
    print(angle_from_origin_and_positions(0, 0, -1, -0.5))
    print(angle_from_origin_and_positions(0, 0, -1, -1))
    print(angle_from_origin_and_positions(0, 0, -0.5, -1))
    print(angle_from_origin_and_positions(0, 0, 0, -1))
    print(angle_from_origin_and_positions(0, 0, 0.5, -1))
    print(angle_from_origin_and_positions(0, 0, 1, -1))
    print(angle_from_origin_and_positions(0, 0, 1, -0.5))
    print(angle_from_origin_and_positions(0, 0, 1, -0.01))
    print(distance_by_values(0, 0, 0, 3))
    print(distance_by_values(0, 0, 3, 0))
    print(distance_by_values(0, 0, 4, 3))
    print(distance_by_values(7, 10, 11, 7))