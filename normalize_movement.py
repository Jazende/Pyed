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