from pyglet import *
from pyglet.gl import *

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(200, 200)
        self.text = text.Label('Test', 
            font_size=16, bold=True, color=(0, 0, 0, 255),
            x=self.width//2, y=self.width//3, 
            multiline=True, width=500)

    def on_draw(self):
        self.clear()
        self.text.draw()

    def on_key_press(s2elf, key, modifiers):
        if key == 65363:
            loc = self.get_location()
            self.set_location(loc[0] + 25, loc[1])
        elif key == 65361:
            loc = self.get_location()
            self.set_location(loc[0] - 25, loc[1])
        if key == 65363:
            loc = self.get_location()
            self.set_location(loc[0] + 25, loc[1])
        elif key == 65361:
            loc = self.get_location()
            self.set_location(loc[0] - 25, loc[1])
        elif key == 65307:
            pyglet.app.exit()
        elif 97 <= key <= 122:
            if modifiers == 17:
                self.text.text += chr(key).upper()
            else:
                self.text.text += chr(key)
        elif key == 32:
            self.text.text += ' '
        elif key == 65288:
            self.text.text = self.text.text[:-1]
        elif key == 65293:
            self.text.text += '\n'
        elif key == 44 and modifiers == 17:
            self.text.text += '?'
        else:
            print(key)

    def on_mouse_enter(self, *args):
        print('Mouse Enter')

    def on_mouse_leave(self, *args):
        print('Mouse Leaves')

def main():
    options = { 
        'resizable': False, 'vsync': False, 
        'style': pyglet.window.Window.WINDOW_STYLE_OVERLAY, 
    }

    win = Window(**options)
    pyglet.app.run()

if __name__ == '__main__':
    main()
