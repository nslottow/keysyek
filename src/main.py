import pyglet

from pyglet.gl import *
from mingus.containers import *
from view import NoteView

g_window = pyglet.window.Window(width=800, height=600)
g_view = NoteView(g_window)

@g_window.event
def on_resize(width, height):
    pass

@g_window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    g_view.draw()

def update(dt):
    pass

if __name__ == '__main__':
    # Setup OpenGL
    glEnable(GL_BLEND)
    glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0.3, 0.3, 0.3, 1)
    glMatrixMode(GL_MODELVIEW)

    # Run the pyglet application
    pyglet.clock.schedule(update)
    pyglet.app.run()