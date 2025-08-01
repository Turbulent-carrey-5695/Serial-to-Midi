const int buttonPins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11};  // Just change the list for # of buttons
const int midiCCs[] =    {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};   // Make sure this matches pins!

const int numButtons = sizeof(buttonPins) / sizeof(buttonPins[0]);
bool lastButtonState[sizeof(buttonPins) / sizeof(buttonPins[0])] = {false};

void setup() {
  Serial.begin(31250);
  for (int i = 0; i < numButtons; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
  }
}

void loop() {
  for (int i = 0; i < numButtons; i++) {
    bool isPressed = digitalRead(buttonPins[i]) == LOW;
    if (isPressed && !lastButtonState[i]) {
      sendCC(midiCCs[i], 127);
      lastButtonState[i] = true;
    } else if (!isPressed && lastButtonState[i]) {
      sendCC(midiCCs[i], 0);
      lastButtonState[i] = false;
    }
  }
  delay(10);
}

void sendCC(byte cc, byte value) {
  Serial.print("CC ");
  Serial.print(cc);
  Serial.print(" ");
  Serial.println(value);
}

