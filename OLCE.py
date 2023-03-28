import pyglet
from math import radians, sin, cos, pi

class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def set_min_x(self, value):
        self.min_x = value

    def set_max_x(self, value):
        self.max_x = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if hasattr(self, 'max_x'):
            value = min(getattr(self, 'max_x'), value)
        if hasattr(self, 'min_x'):
            value = max(getattr(self, 'min_x'), value)
        self._x = value

    def set_min_y(self, value):
        self.min_y = value

    def set_max_y(self, value):
        self.max_y = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if hasattr(self, 'max_y'):
            value = min(getattr(self, 'max_y'), value)
        if hasattr(self, 'min_y'):
            value = max(getattr(self, 'min_y'), value)
        self._y = value

class Pixel:
    def __init__(self, x, y, width, height, color=None, batch=None):
        self.shape = pyglet.shapes.Rectangle(x=x, y=y, width=width, height=height, color=color, batch=batch)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.batch = batch
        self._column = x // width
        self._row = y // height
        self._base_color = (0, 0, 0)

    def clear(self):
        self.color = self._base_color

    @property
    def color(self):
        return self.shape.color

    @color.setter
    def color(self, value):
        self.shape.color = value

    def __repr__(self):
        return f'{self._column}x{self._row}'

class Screen:
    def __init__(self, screen_width, screen_height, pixel_width, pixel_height):
        self.width = screen_width // pixel_width
        self.height = screen_height // pixel_height
        self.pixel_width = pixel_width
        self.pixel_height = pixel_height
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.batch = pyglet.graphics.Batch()
        self.pixels = {
            (x, y): Pixel(x*pixel_width, y*pixel_height, pixel_width, pixel_height, color=(0, 0, 0), batch=self.batch) 
            for x in range(screen_width // pixel_width) 
            for y in range(screen_height // pixel_height)
        }

    def draw(self):
        self.batch.draw()

    def __getitem__(self, key):
        if key in self.pixels.keys():
            return self.pixels[key]
        raise ValueError(f'No pixel at {key}')

    def pixel_at(self, x, y):
        col = x // self.pixel_width
        row = y // self.pixel_height
        return self.pixels[(col, row)]

class Map:
    def __init__(self):
        self.map = {
            (0, 0): '#', (1, 0): '#', (2, 0): '#', (3, 0): '#', (4, 0): '#', (5, 0): '#', (6, 0): '#', (7, 0): '#', (8, 0): '#', 
            (0, 1): '#', (1, 1): '.', (2, 1): '.', (3, 1): '.', (4, 1): '.', (5, 1): '.', (6, 1): '.', (7, 1): '.', (8, 1): '#', 
            (0, 2): '#', (1, 2): '.', (2, 2): '.', (3, 2): '.', (4, 2): '.', (5, 2): '.', (6, 2): '.', (7, 2): '.', (8, 2): '#', 
            (0, 3): '#', (1, 3): '.', (2, 3): '.', (3, 3): '.', (4, 3): '.', (5, 3): '.', (6, 3): '.', (7, 3): '.', (8, 3): '#', 
            (0, 4): '#', (1, 4): '.', (2, 4): '.', (3, 4): '.', (4, 4): '.', (5, 4): '.', (6, 4): '.', (7, 4): '.', (8, 4): '#', 
            (0, 5): '#', (1, 5): '#', (2, 5): '#', (3, 5): '#', (4, 5): '#', (5, 5): '#', (6, 5): '#', (7, 5): '#', (8, 5): '#', 
        }
        self.width = 9
        self.height = 6

    def __getitem__(self, key):
        if key in self.map.keys():
            return self.map[key]
        raise ValueError()

class Window(pyglet.window.Window):
    def __init__(self, screen_width, screen_height, pixel_width, pixel_height):
        if not screen_width % pixel_width == 0: screen_width -= screen_width % pixel_width 
        if not screen_height % pixel_height == 0: screen_width -= screen_height % pixel_height 
        super().__init__(width=screen_width, height=screen_height)
        self.set_location(1400, 100)
        self.fps_display = pyglet.window.FPSDisplay(self)
        self.screen_ = Screen(screen_width, screen_height, pixel_width, pixel_height)

        self.map = Map()
        self.player = Player(3, 3, 0)
        self.player.set_min_x(1)
        self.player.set_max_x(7)
        self.player.set_min_y(1)
        self.player.set_max_y(4)
        self.pov = radians(90)

        self.key_handler = { 'up': False, 'down': False, 'left': False, 'right': False }

        pyglet.clock.schedule(self.update, 1/30)

    def on_draw(self):
        self.clear()
        self.screen_.draw()
        self.fps_display.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol in [100, 65363]:
            self.key_handler['right'] = True
        if symbol in [113, 65361]:
            self.key_handler['left'] = True
        if symbol in [115, 65364]:
            self.key_handler['down'] = True
        if symbol in [122, 65362]:
            self.key_handler['up'] = True

    def on_key_release(self, symbol, modifiers):
        if symbol in [100, 65363]:
            self.key_handler['right'] = False
        if symbol in [113, 65361]:
            self.key_handler['left'] = False
        if symbol in [115, 65364]:
            self.key_handler['down'] = False
        if symbol in [122, 65362]:
            self.key_handler['up'] = False

    def update(self, i, dt):
        if self.key_handler['left']:
            self.player.angle -= pi / 2 * dt
        if self.key_handler['right']:
            self.player.angle += pi / 2 * dt
        if self.key_handler['up']:
            self.player.x += sin(self.player.angle) * dt
            self.player.y += cos(self.player.angle) * dt
        if self.key_handler['down']:
            self.player.x -= sin(self.player.angle) * dt
            self.player.y -= cos(self.player.angle) * dt

        for x in range(self.screen_.width):
            ray_angle = (self.player.angle - (self.pov / 2)) + x * (self.pov / self.screen_.width)

            line_x = sin(ray_angle)
            line_y = cos(ray_angle)
            distance = 0

            while True:
                if distance > 7:
                    break
                distance += 0.1
                
                test_x = self.player.x + line_x * distance
                test_y = self.player.y + line_y * distance

                if not (0 <= test_x <= self.screen_.width):
                    distance = 7
                    break
                if not (0 <= test_y <= self.screen_.height):
                    distance = 7
                    break
                
                try:
                    if self.map[(int(test_x), int(test_y))] == '#':
                        break
                except:
                    distance = 7
                    break

            wall_height = int(self.screen_.height * (1 / distance))
            floor_height = (self.screen_.height - wall_height) // 2
            ceiling_height = self.screen_.height - floor_height

            for y in range(self.screen_.height):
                if y > ceiling_height:
                    self.screen_[(x, y)].color = (30, 30, 130)
                elif y < floor_height:
                    self.screen_[(x, y)].color = (130, 30, 30)
                else:
                    self.screen_[(x, y)].color = (30, 130, 30)

window = Window(512, 512, 8, 8)
pyglet.app.run()
