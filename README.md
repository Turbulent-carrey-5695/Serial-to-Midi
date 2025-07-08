# Arduino MIDI Button Box

Simple project: use an Arduino with push buttons to send MIDI CC messages to your DAW via a Python serial-to-MIDI bridge.

---

## Contents

- `Arduino_Button_serial.ino` — Arduino sketch for reading button presses and sending MIDI CC over serial
- `serial_to_midi_gui.py` — Python script to forward serial MIDI data to a virtual MIDI port

---

## Requirements

- Arduino board (Uno, Nano, etc.)
- Momentary push buttons (1 per input)
- Python 3.x
- Virtual MIDI port (IAC on Mac, loopMIDI on Windows)

---

## Arduino Setup

1. **Wiring:**  
   - One side of each button: connect to a digital pin (see `buttonPins[]` in the Arduino code).
   - Other side of each button: connect to GND.
   - No resistors needed (uses `INPUT_PULLUP`).
2. **Edit** `buttonPins[]` and `midiCCs[]` in `arduino_midi_buttons.ino` to match your wiring and desired MIDI CC numbers.
3. **Upload** the sketch to your Arduino at 31250 baud.

---

## Python Serial to MIDI Bridge

### Install Required Libraries

```
pip install pyserial mido python-rtmidi
```

## How to Create a Virtual MIDI Port (Mac)

1. Open Audio MIDI Setup (in Applications > Utilities)
2. Go to Window > Show MIDI Studio
3. Double-click IAC Driver
4. Check "Device is online"
5. Click the + button to add a port (e.g. name it ArduinoMIDI)


## Usage

1. Plug in your Arduino (with the uploaded sketch).
2. Make sure your virtual MIDI port (e.g. ArduinoMIDI) exists and is enabled.
3. Run the Python script.
4. Select your Arduino serial port in the GUI and click Connect.
5. Set your DAW's MIDI input to ArduinoMIDI (or whatever you named your port).
6. Button presses will now send MIDI CC messages to your DAW.

**Example Arduino Output**

CC 21 127
CC 21 0



## Note: I made this for MacOS, for controlling Archetype: Petrucci (NeuralDSP Plugin) Live on stage.
