import atexit
from mingus.containers.Note import Note
import rtmidi

NOTE_ON = 0x9
NOTE_OFF = 0x8

def input_callback(event, data):
    data._on_event(event[1], event[0])

class NoPortsAvailableError(Exception):
    pass

class MidiInput:
    def __init__(self, port_name=None):
        # Open MIDI port and listen for events
        self._device = rtmidi.MidiIn()
        self.time = 0

        ports = self._device.get_ports()
        print "MIDI input ports: " + str(ports)
        if not ports:
            raise NoPortsAvailableError()
            
        if port_name and port_name in ports:
            port = ports.index(port_name)
            self.port_name = port_name
        else:
            port = 0
            self.port_name = ports[0]

        print "Opening MIDI input port '%s'" % self.port_name
        self._device.open_port(port)
        self._device.set_callback(input_callback, self)

        # Setup array and list of keys for querying
        self._key_states = [False] * 128

    def _on_event(self, dt, msg):
        self.time += dt
        cmd, note, vel = msg
        channel = cmd & 0xF
        cmd = cmd >> 4
        note_str = str(Note().from_int(note))

        # Update key state
        if cmd == NOTE_ON:
            self._key_states[note] = True
        elif cmd == NOTE_OFF:
            self._key_states[note] = False

    def is_note_on(self, note):
        return self._key_states[int(note)]

    def get_pressed_notes(self):
        pressed_notes = []
        for key, pressed in enumerate(self._key_states):
            if pressed:
                pressed_notes.append(Note().from_int(key))

        return pressed_notes
