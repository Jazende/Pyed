import pyglet
import pyglet.gl as gl
from pyglet import image

border_image = image.load('top.png')
border_image.anchor_x = 0
border_image.anchor_y = 0

class Circle:

    def __init__(self, x, y, radius, points=10):
        self.x = x
        self.y = y
        self.radius = radius
        self.points = min(100, max(5, points))
        self.sprites = []
        self.batch = pyglet.graphics.Batch()
        self.setup()
    
    def setup(self):
        self.circle_image = image.load('top.png')
        self.circle_image.anchor_x = self.circle_image.width//2
        self.circle_image.anchor_y = self.circle_image.height + self.radius
        circle_angle = 360 // self.points
        for idx in range(self.points):
            rot_sprite = pyglet.sprite.Sprite(self.circle_image, batch=self.batch)
            rot_sprite.update(x=self.x, y=self.y, rotation=circle_angle*idx)
            self.sprites.append(rot_sprite)

    def draw(self):
        self.batch.draw()

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sprites = []
        self.batch = pyglet.graphics.Batch()
        self.setup()
        self.circle = Circle(self.width//2, self.height//2, 100, 30)
    
    def setup(self):
        for idx in range(self.width // border_image.width):
            top_sprite = pyglet.sprite.Sprite(border_image, x=idx * border_image.width, y=self.height-border_image.height, batch=self.batch)
            bottom_sprite = pyglet.sprite.Sprite(border_image, batch=self.batch)
            bottom_sprite.update(rotation=180, x=(idx+1) * border_image.width, y=border_image.height)
            self.sprites.append(top_sprite)
            self.sprites.append(bottom_sprite)

    def on_draw(self):
        gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()
        self.circle.draw()

def main():
    window = Window()
    pyglet.app.run()

if __name__ == '__main__':
    main()
