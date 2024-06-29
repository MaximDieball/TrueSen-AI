#include <Mouse.h>
#include <hidboot.h>
#include <usbhub.h>

USB Usb;
HIDBoot<USB_HID_PROTOCOL_MOUSE> HidMouse(&Usb);

// Next mouse movement
int8_t moveX = 0;
int8_t moveY = 0;
int8_t scroll = 0;
uint8_t buttons = 0;

uint8_t injectX = 0;
uint8_t injectY = 0;

uint8_t oldInjectX = 0;
uint8_t oldInjectY = 0;

const int xPins[8] = { 2, 3, 4, 5, 6, 7 };
const int yPins[8] = { 9, 10, 11, 12, 13 };


class MouseRptParser : public MouseReportParser {
protected:
  void Parse(USBHID *hid, bool is_rpt_id, uint8_t len, uint8_t *buf) override {

    moveX = (int8_t)buf[1];
    moveY = (int8_t)buf[2];

    if (moveX != 0 || moveY != 0) {
    }

    // Check if buf[3] exists for scroll wheel data
    if (len > 3) {
      scroll = (int8_t)buf[3];  // Scroll wheel movement
    } else {
      scroll = 0;
    }

    // Mouse buttons
    buttons = buf[0];
  }
};

MouseRptParser mouseParser;

void setup() {

  Serial.begin(9600);

  for (int i = 2; i <= 13; i++) {
    pinMode(i, INPUT);
  }

  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);

  if (Usb.Init() == -1) {
    while (1)
      ;  // Stop if the USB host shield is not properly initialized
  }

  delay(200);

  HidMouse.SetReportParser(0, &mouseParser);
  Mouse.begin();
}

void loop() {

  Usb.Task();
  getInjectValues();

  if (moveX != 0 || moveY != 0) {
    Serial.print("x: ");
    Serial.print(moveX);
    Serial.print("  y: ");
    Serial.println(moveY);
  }

  // Send mouse movement
  //if (moveX != 0 | moveY != 0 | scroll != 0) {
    Mouse.move(moveX + injectX, moveY + injectY, scroll);
  //}

  // Mouse buttons
  if (buttons & MOUSE_LEFT) {
    Mouse.press(MOUSE_LEFT);
  } else {
    Mouse.release(MOUSE_LEFT);
  }

  if (buttons & MOUSE_RIGHT) {
    Mouse.press(MOUSE_RIGHT);
  } else {
    Mouse.release(MOUSE_RIGHT);
  }

  if (buttons & MOUSE_MIDDLE) {
    Mouse.press(MOUSE_MIDDLE);
  } else {
    Mouse.release(MOUSE_MIDDLE);
  }

  // Reset movements
  moveX = 0;
  moveY = 0;
  scroll = 0;
}


void getInjectValues() {
  injectX = 0;
  injectY = 0;
  Serial.println(analogRead(A3));
  if (analogRead(A3) < 500) {
    return;
  }

  for (int i = 0; i < 5; i++) {
    int xPinValue = digitalRead(xPins[i]);
    int yPinValue = digitalRead(yPins[i]);

    if (xPinValue == HIGH) {
      injectX |= (1 << i);  // Set the ith bit
    }
    if (yPinValue == HIGH) {
      injectY |= (1 << i);  // Set the ith bit
    }
  }
  if (digitalRead(xPins[5]) == HIGH) {
    injectX |= (1 << 5);  // Set the ith bit
  }

  if (analogRead(A1) > 500) {
    injectX = -injectX;
  }
  if (analogRead(A2) > 500) {
    injectY = -injectY;
  }

  if(injectY == oldInjectY && injectX == oldInjectX){
    injectY, injectX = 0;
  } else{
    oldInjectY = injectY;
    oldInjectX = injectX;
  }
}



