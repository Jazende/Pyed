import pyglet
import random
import time
from pyglet.gl import *
from math_utilities import angle_between_origin_and_positions
from math_utilities import distance_by_values
from math_utilities import normalize
from math_utilities import sin
from math_utilities import cos
from math_utilities import radians

player_image = pyglet.image.load("red_circle_p_transparant.png")
player_image.anchor_x = int(player_image.width // 2)
player_image.anchor_y = int(player_image.height // 2)

shot_image = pyglet.image.load("shot_r_with_start_transparant.png")

enemy_angry_image = pyglet.image.load("boss_angry_face_transparant.png")
enemy_angry_image.anchor_x = int(enemy_angry_image.width // 2)
enemy_angry_image.anchor_y = int(enemy_angry_image.height // 2)

enemy_shocked_image = pyglet.image.load("boss_shocked_face_transparant.png")
enemy_shocked_image.anchor_x = int(enemy_shocked_image.width // 2)
enemy_shocked_image.anchor_y = int(enemy_shocked_image.height // 2)

crosshair_image = pyglet.image.load("black_crosshair_transparant.png")
cursor = pyglet.window.ImageMouseCursor(crosshair_image, 5, 5)

directionals = {'up': [122, 65362], 'left': [113, 65361], 'right': [100, 65363], 'down': [115, 65364]}

class Enemy:
    FLAG_ROTATING_TO_PLAYER = True

    def __init__(self, screen):
        self.screen = screen
        self.screen.register_object(self)

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        pass

    def rotate_based_on_player_position(self, player):
        if not self.FLAG_ROTATING_TO_PLAYER:
            return
        self.rotation = -1 * angle_between_origin_and_positions(self.x, self.y, player.x, player.y)
        self.sprite.update(rotation=self.rotation)

class Ruski(Enemy):
    def __init__(self, screen):
        super().__init__(screen)
        w, h = screen.get_size()
        self.x = w // 2
        self.y = (h * 4) // 5
        self.sprites = {'angry': pyglet.sprite.Sprite(enemy_angry_image, self.x, self.y), 'shocked': pyglet.sprite.Sprite(enemy_shocked_image, self.x, self.y)}
        self.current_sprite = 'angry'
        self.moving = False
        self.shooting = False
        self.destination = (0, 0)
        self.speed = 200
        width, height = screen.get_size()

        def x_calc(x, width, size):
            return (100*(x+1)) if x < 2 else width-(100*(size-x))

        def y_calc(y, height, size):
            return (100*(y+1)) if y < 2 else height-(100*(size-y))

        def neighbours_calc(x, y, size):
            return [location for location in [(x-1, y), (x+1, y), (x, y-1), (x, y+1), (x-1, y-1), (x+1, y+1), (x-1, y+1), (x+1, y-1)] if location in [(i, j) for i in range(size) for j in range(size)]]

        size = 4

        self.destinations = {
            (i, j): {'x': x_calc(i, width, size), 'y': y_calc(j, height, size), 'neighbours': neighbours_calc(i, j, size)} for i in range(size) for j in range(size)
        }
        self.destinations['current'] = (2, 3)
    
    @property
    def current_sprite(self):
        return self._current_sprite
    
    @current_sprite.setter
    def current_sprite(self, value):
        if not value in self.sprites.keys():
            return
        self._current_sprite = value

    @property
    def sprite(self):
        return self.sprites[self.current_sprite]

    def swap_shocked_face(self, *args, **kwargs):
        self.current_sprite = 'shocked'
        self.FLAG_ROTATING_TO_PLAYER = False
        pyglet.clock.schedule_once(self.swap_angry_face, 3)
        pyglet.clock.schedule_interval(self.rotate_on_hit, 0.01)

    def swap_angry_face(self, dt, *args, **kwargs):
        self.current_sprite = 'angry'
        self.FLAG_ROTATING_TO_PLAYER = True
        pyglet.clock.unschedule(self.rotate_on_hit)

    def update_sprites(self, **kwargs):
        for sprite in self.sprites.keys():
            self.sprites[sprite].update(**kwargs)

    def rotate_on_hit(self, dt):
        self.rotation += 360 * dt

    def draw(self):
        self.sprites[self.current_sprite].draw()

    def update(self, dt):
        if self.moving:
            delta_x, delta_y = normalize(self.destination[0] - self.x, self.destination[1] - self.y)

            delta_x = min(delta_x*self.speed*dt, abs(self.destination[0] - self.x))
            delta_y = min(delta_y*self.speed*dt, abs(self.destination[1] - self.y))

            self.x += delta_x
            self.y += delta_y

            if (self.x, self.y) == self.destination:
                self.moving = False
                self.shooting = True
        elif self.shooting:
            self.shooting = False
        else:
            self.choose_new_destination()
            self.moving = True
        self.update_sprites(x=self.x, y=self.y, rotation=self.rotation)
    
    def choose_new_destination(self):
        self.destinations['current'] = random.choice(self.destinations[self.destinations['current']]['neighbours'])
        self.destination = (self.destinations[self.destinations['current']]['x'], self.destinations[self.destinations['current']]['y'])
        if distance_by_values(self.destination[0], self.destination[1], self.screen.player.x, self.screen.player.y) < (self.sprite.width * 2):
            self.choose_new_destination()

    def collision(self, object):
        if isinstance(object, Shot):
            for collision_check in object.collision_checks:
                x, y = collision_check
                # +2 for some leeway in hitting
                if distance_by_values(x, y, self.x, self.y) < (self.sprite.width // 2 + 2):
                    object.out_of_bounds = True
                    self.update_sprites(scale_x=self.sprite.scale_x-0.1, scale_y=self.sprite.scale_y-0.1)
                    self.speed += 25
                    self.swap_shocked_face()
                    return True
                return False
        else:
            raise NotImplemented
            return False

class Player:
    def __init__(self, screen):
        self.screen = screen
        self._rotation = 0
        self.speed = 100
        screen_width, screen_height = screen.get_size()
        self.x = (screen_width - player_image.width) // 2
        self.y = (screen_height - player_image.height) // 2
        self.sprite = pyglet.sprite.Sprite(player_image, self.x, self.y)
        self.sprite.update(scale_x=0.7, scale_y=0.7)
        self.screen.register_object(self)
        self.time_between_shots = 0.5
        self.time_last_shot = 0
        self.movement_update = {'x': 0, 'y': 0}
        self.shots = []

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value
    
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
        self.x += self.movement_update['x']*dt
        self.y += self.movement_update['y']*dt
        self.movement_update['x'] = 0
        self.movement_update['y'] = 0

    def movement(self, movement):
        if movement['left'] and not movement['right']:
            self.movement_update['x'] += -cos(radians(self.rotation + 90))*self.speed
            self.movement_update['y'] += sin(radians(self.rotation + 90))*self.speed
        if movement['right'] and not movement['left']:
            self.movement_update['x'] += cos(radians(self.rotation + 90))*self.speed
            self.movement_update['y'] += -sin(radians(self.rotation + 90))*self.speed
        if movement['up'] and not movement['down']:
            self.movement_update['x'] += cos(radians(self.rotation))*self.speed
            self.movement_update['y'] += -sin(radians(self.rotation))*self.speed
        if movement['down'] and not movement['up']:
            self.movement_update['x'] += -cos(radians(self.rotation))*self.speed
            self.movement_update['y'] += sin(radians(self.rotation))*self.speed

    def draw(self):
        self.sprite.update(rotation=self.rotation, x=self.x, y=self.y)
        self.sprite.draw()

    def rotate_based_on_mouse_position(self, mouse_x, mouse_y):
        if (abs(self.x - mouse_x) + abs(self.y - mouse_y)) < 5:
            self.speed = 0
            self.strafe_speed = 0
            return
        self.rotation = -1 * angle_between_origin_and_positions(self.x, self.y, mouse_x, mouse_y)

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

    @property
    def collision_checks(self):
        return [(self.x, self.y), (self.x + self.sprite.width * cos(radians(self.rotation)), self.y + self.sprite.height * sin(radians(self.rotation)))]

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
        self.set_mouse_cursor(cursor)
        self.set_2d()
        self.movement_dict = {'left': False, 'right': False, 'up': False, 'down': False}
        self.mouse_dict = {'left_clicked': False, 'x': 0, 'y': 0}
        self.mouse_positions = [0, 0]
        self.objects = []
        self.player = Player(self)
        self.enemy = Ruski(self)
        glClearColor(1, 1, 1, 1)
        pyglet.clock.schedule_interval(self.update, 1.0 / 60)
    
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
        self.player.rotate_based_on_mouse_position(self.mouse_dict['x'], self.mouse_dict['y'])
        self.enemy.rotate_based_on_player_position(self.player)
        if self.mouse_dict['left_clicked']:
            self.player.shoot()

        self.update_movement(dt)
        for object in self.objects:
            object.update(dt)
            if not isinstance(object, Shot):
                continue
            for target in self.objects:
                if not isinstance(target, Enemy):
                    continue
                if not hasattr(target, 'collision'):
                    continue
                target.collision(object)
        self.objects = [object for object in self.objects if not hasattr(object, 'out_of_bounds') or object.out_of_bounds == False]

    def update_movement(self, dt):
        self.player.movement(self.movement_dict)

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
        for direction, key_numbers in directionals.items():
            if key in key_numbers:
                self.movement_dict[direction] = True

    def on_key_release(self, key, modifier):
        for direction, key_numbers in directionals.items():
            if key in key_numbers:
                self.movement_dict[direction] = False

    def on_mouse_motion(self, mouse_x, mouse_y, delta_x, delta_y):
        self.mouse_dict['x'] = mouse_x
        self.mouse_dict['y'] = mouse_y

    def on_mouse_drag(self, mouse_x, mouse_y, delta_x, delta_y, button, modifiers):
        self.mouse_dict['x'] = mouse_x
        self.mouse_dict['y'] = mouse_y
        if button == 1:
            self.mouse_dict['left_clicked'] = True

    def on_mouse_press(self, mouse_x, mouse_y, button, modifiers):
        if button == 1:
            self.mouse_dict['left_clicked'] = True

    def on_mouse_release(self, mouse_x, mouse_y, button, modifiers):
        if button == 1:
            self.mouse_dict['left_clicked'] = False

def main():
    screen = Screen(width=800, height=640)
    pyglet.app.run()

if __name__ == '__main__':
    main()
