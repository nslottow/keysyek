import math
import mingus.core.notes as notes

from pyglet.gl import *
from mingus.containers import *

class StaffView:
    def __init__(self, x, y, width, note_height=20, line_width=3,
                 clef='treble', track=None):
        # Initialize sizing and position info
        self.x = x
        self.y = y
        self.width = width
        self.note_height = note_height
        self.line_width = line_width
        self.staff_height = 5 * self.note_height + self.line_width

        # Initialize note info
        self.clef = clef
        self.track = track

        if clef == 'treble':
            self.middle_note = Note('B', 5)
        elif clef == 'bass':
            self.middle_note = Note('D', 4)

    def get_nearby_containers(self, beat, width=8):
        '''Returns the note containers surrounding the specified absolute beat'''
        pass

    def note_to_offset(self, note):
        '''
        Returns the offset of a note from the middle note of the staff in units
        of steps into the C-major scale 
        '''

        map = {'C':0, 'D':1, 'E':2, 'F':3, 'G':4, 'A':5, 'B':6}
        a = map[self.middle_note.name[0]] + 7 * self.middle_note.octave
        b = map[note.name[0]] + 7 * note.octave
        return b - a

    def draw_note(self, note, x):
        offset = self.note_to_offset(note)
        steps = 8
        angle_step = 6.283 / steps
        note_width = self.note_height * 1.5
        y = self.y + offset * self.note_height / 2

        # Draw ledger lines if necessary
        if offset > 5 or offset < -5:
            if offset > 5:
                line_step = self.note_height
                line_y = self.y + self.note_height * 3
            else:
                line_step = -self.note_height
                line_y = self.y - self.note_height * 3

            half_width = note_width / 1.6
            if offset % 2 == 0:
                glPushMatrix()
                glLoadIdentity()
                glTranslatef(x, y, 0)
                glBegin(GL_LINES)
                glVertex2f(-half_width, 0)
                glVertex2f(half_width, 0)
                glEnd()
                glPopMatrix()

            glPushMatrix()
            glLoadIdentity()
            glTranslatef(x, line_y, 0)
            glLineWidth(self.line_width)
            glBegin(GL_LINES)
            for i in range(0, (abs(offset) - 5) / 2):
                glVertex2f(-half_width, i * line_step)
                glVertex2f(half_width, i * line_step)
            glEnd()
            glPopMatrix()

        # Draw notehead
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(x, y, 0)
        glRotatef(10, 0, 0, 1)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0, 0)
        for i in range(steps + 1):
            glVertex2f(note_width / 2 * math.cos(i * angle_step),
                       self.note_height / 2 * math.sin(i * angle_step))
        glEnd()
        glPopMatrix()

    def draw(self):
        glLineWidth(self.line_width)
        glColor3f(0, 0, 0)
        glBegin(GL_LINES)
        for i in range(-2, 3):
            glVertex2f(0, self.y + i * self.note_height)
            glVertex2f(self.width, self.y + i * self.note_height)
        glEnd()

        if self.clef == 'treble':
            self.draw_note(Note('B', 5), self.width / 2)
            self.draw_note(Note('G', 5), self.width / 2)
            self.draw_note(Note('E', 5), self.width / 2)
            self.draw_note(Note('F', 5), self.width / 2 - self.note_height)
