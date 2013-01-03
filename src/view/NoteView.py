from pyglet.gl import *
from StaffView import StaffView
from midi import MidiInput

class NoteView:
    '''
    TODO:
        Draw clefs
        Draw key signatures
        Draw accidentals
        Handle overlap of notes at same y-position
        Lines and clef (static imagery) as vertex buffers or arrays
        Time (in beats) - draw only notes near the current time
        Line color
        Note color
    '''

    def __init__(self, window, left_hand_track=None, right_hand_track=None):
        # Initialize position and sizing info
        self.window = window
        self.y = window.height / 2
        self.note_height = 20
        self.line_width = 3
        self.staff_height = 5 * self.note_height + self.line_width
        self.staves = [StaffView(x=0, y=self.y - self.staff_height * .8, width=self.window.width, clef='bass', track=left_hand_track),
                       StaffView(x=0, y=self.y + self.staff_height * .8, width=self.window.width, clef='treble', track=right_hand_track)]

        # Initialize MIDI input
        self.midi_in = MidiInput()

    def draw(self):
        for s in self.staves:
            s.draw()
        
        glColor4f(0.8, 0, 0.8, 0.5)
        notes = self.midi_in.get_pressed_notes()
        for n in notes:
            s = self.staves[0] if int(n) < 60 else self.staves[1]
            s.draw_note(n, s.width / 2)
