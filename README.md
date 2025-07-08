# Arduino Serial to MIDI Bridge

Simple Python app to forward MIDI CC messages from Arduino serial output to a MIDI virtual port.

## Requirements

- Python 3.x
- Arduino sending lines like: `CC <num> <val>`
- Virtual MIDI port (IAC on Mac, loopMIDI on Windows)

### Install Python Libraries

pip install pyserial mido python-rtmidi
or
pip3 install pyserial mido python-rtmidi

## Usage

1. Plug in your Arduino.
2. Set up a virtual MIDI port.
3. Run the script.
4. Select your serial port and click Connect.

## Example Arduino Output

CC 1 127
CC 2 0





##Note: This is made for MaxOS
