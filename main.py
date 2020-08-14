import pyglet
import time
from math import sin, cos, degrees, radians, acos
from pyglet.gl import *
from angle_calc import angle_between_origin_and_positions

gun_image = pyglet.image.load("gun_r_transparant.png")
gun_image.anchor_x = int(gun_image.width / 3.5)
gun_image.anchor_y = int(gun_image.height // 2)

shot_image = pyglet.image.load("shot_r_transparant.png")

directionals = {'up': [122, 65362], 'left': [113, 65361], 'right': [100, 65363]}

class Gun:
    def __init__(self, screen):
        self.screen = screen
        self._rotation = 0
        self._speed = 0
        self._strafe_speed = 0
        screen_width, screen_height = screen.get_size()
        self.x = (screen_width - gun_image.width) // 2
        self.y = (screen_height - gun_image.height) // 2
        self.sprite = pyglet.sprite.Sprite(gun_image, self.x, self.y)
        self.sprite.update(scale_x=0.7, scale_y=0.7)
        self.screen.register_object(self)
        self.time_between_shots = 0.5
        self.time_last_shot = 0

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = min(200, value)
    
    @property
    def strafe_speed(self):
        return self._strafe_speed

    @strafe_speed.setter
    def strafe_speed(self, value):
        self._strafe_speed = min(200, value)
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
    
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
    
    def update(self, dt):
        self.speed = max(0, self.speed - 10*dt)
        self.strafe_speed = max(0, self.strafe_speed - 2*dt)
        self.x = self.x + cos(radians(self.rotation))*self.speed*dt
        self.y = self.y - sin(radians(self.rotation))*self.speed*dt

    def draw(self):
        self.sprite.update(rotation=self.rotation, x=self.x, y=self.y)
        self.sprite.draw()

    def rotate_based_on_mouse_position(self, mouse_x, mouse_y):
        if (abs(self.x - mouse_x) + abs(self.y - mouse_y)) < 5:
            self.speed = 0
            self.strafe_speed = 0
            return
        self.rotation = -1 * angle_between_origin_and_positions(self.x, self.y, mouse_x, mouse_y)

    def strafe_left(self, dt):
        self.x += -cos(radians(self.rotation + 90))*self.strafe_speed*dt
        self.y += sin(radians(self.rotation + 90))*self.strafe_speed*dt

    def strafe_right(self, dt):
        self.x -= -cos(radians(self.rotation + 90))*self.strafe_speed*dt
        self.y -= sin(radians(self.rotation + 90))*self.strafe_speed*dt

    def shoot(self, *args):
        now = time.time()
        if (now - self.time_last_shot) > self.time_between_shots:
            shot = Shot(self.x, self.y, self.rotation, *self.screen.get_size())
            self.screen.register_object(shot)
            self.time_last_shot = time.time()

class Shot:
    def __init__(self, x, y, rotation, max_x, max_y):
        self.x = x
        self.y = y
        self.max_x = max_x
        self.max_y = max_y
        self.rotation = rotation
        self.sprite = pyglet.sprite.Sprite(shot_image, self.x, self.y)
        self.sprite.update(rotation=self.rotation)
        self.speed = 300
        self.out_of_bounds = False

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.x = self.x + cos(radians(self.rotation))*self.speed*dt
        self.y = self.y - sin(radians(self.rotation))*self.speed*dt
        self.sprite.update(self.x, self.y)
        if self.x < -10 or self.x > 1000 or self.y < -10 or self.y > 1000:
            self.out_of_bounds = True
        
class Screen(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_2d()
        self.movement_dict = {'strafe_left': False, 'strafe_right': False, 'up': False, 'down': False}
        self.mouse_dict = {'left_clicked': False}
        self.mouse_positions = [0, 0]
        self.objects = []
        self.delete_objects = []
        self.gun = Gun(self)
        glClearColor(1, 1, 1, 1)
        pyglet.clock.schedule_interval(self.update, 1.0 / 30)
    
    def register_object(self, object):
        self.objects.append(object)
    
    def on_draw(self):
        self.clear()
        self.set_2d()
        self.draw_border()
        for object in self.objects:
            object.draw()
    
    def draw_border(self, border_size=5):
        width, height = self.get_size()
        border_colour = (0.7, 0.7, 0.7, 1)
        self.draw_square(0, 0, width, border_size, border_colour)
        self.draw_square(0, 0, border_size, height, border_colour)
        self.draw_square(0, height-border_size, width, border_size, border_colour)
        self.draw_square(width-border_size, 0, border_size, height, border_colour)

    def draw_square(self, x, y, width, height, colour):
        glBegin(GL_TRIANGLES)
        glColor4f(*colour)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glVertex2f(x, y)
        glEnd()

    def update(self, dt):
        self.gun.rotate_based_on_mouse_position(*self.mouse_positions)
        self.update_movement(dt)
        for object in self.objects:
            object.update(dt)
        self.objects = [object for object in self.objects if not hasattr(object, 'out_of_bounds') or object.out_of_bounds == False]

    def update_movement(self, dt):
        if self.movement_dict['strafe_left']:
            self.gun.strafe_speed += 1
            self.gun.strafe_left(dt)
        if self.movement_dict['strafe_right']:
            self.gun.strafe_speed += 1
            self.gun.strafe_right(dt)
        if self.movement_dict['up']:
            self.gun.speed += 5

    def set_2d(self):
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def on_key_press(self, key, modifier):
        if key in directionals['left']:
            self.movement_dict['strafe_left'] = True
        if key in directionals['right']:
            self.movement_dict['strafe_right'] = True
        if key in directionals['up']:
            self.movement_dict['up'] = True

    def on_key_release(self, key, modifier):
        if key in directionals['left']:
            self.movement_dict['strafe_left'] = False
        if key in directionals['right']:
            self.movement_dict['strafe_right'] = False
        if key in directionals['up']:
            self.movement_dict['up'] = False

    def on_mouse_motion(self, *args, **kwargs):
        self.mouse_positions = args[:2]

    def on_mouse_press(self, mouse_x, mouse_y, button, modifiers):
        self.attempt_shot()

    def on_mouse_drag(self, *args, **kwargs):
        self.mouse_positions = args[:2]
        self.attempt_shot()

    def attempt_shot(self):
        self.gun.shoot()

def main():
    screen = Screen(width=800, height=640)
    pyglet.app.run()

if __name__ == '__main__':
    main()
