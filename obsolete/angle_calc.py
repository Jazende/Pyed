from math import radians, acos, degrees, sqrt, asin

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

if __name__ == '__main_-':
    angle_from_origin_and_positions(0, 0, 1, 0)
    angle_from_origin_and_positions(0, 0, 1, 0.5)
    angle_from_origin_and_positions(0, 0, 1, 1)
    angle_from_origin_and_positions(0, 0, 0.5, 1)
    angle_from_origin_and_positions(0, 0, 0, 1)
    angle_from_origin_and_positions(0, 0, -0.5, 1)
    angle_from_origin_and_positions(0, 0, -1, 1)
    angle_from_origin_and_positions(0, 0, -1, 0.5)
    angle_from_origin_and_positions(0, 0, -1, 0)
    angle_from_origin_and_positions(0, 0, -1, -0.5)
    angle_from_origin_and_positions(0, 0, -1, -1)
    angle_from_origin_and_positions(0, 0, -0.5, -1)
    angle_from_origin_and_positions(0, 0, 0, -1)
    angle_from_origin_and_positions(0, 0, 0.5, -1)
    angle_from_origin_and_positions(0, 0, 1, -1)
    angle_from_origin_and_positions(0, 0, 1, -0.5)
    angle_from_origin_and_positions(0, 0, 1, -0.01)
