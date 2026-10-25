/*
  Project: AI Based Early Fire Detection System
  Hardware: Arduino Uno, Piezo Buzzer, Status LED
  Communication: Serial (9600 Baud)
*/

const int buzzerPin = 8; // Buzzer connected to digital pin 8
const int ledPin = 13;   // On-board LED or external warning LED

void setup() {
  // Initialize serial communication at 9600 baud rate
  Serial.begin(9600);
  
  // Set pin modes
  pinMode(buzzerPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  
  // Initial state: Off (Safe)
  digitalWrite(buzzerPin, LOW);
  digitalWrite(ledPin, LOW);
}

void loop() {
  // Check if data is available on the serial port
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    // If Hazard 'H' is received from Python/Flask backend
    if (command == 'H') {
      digitalWrite(buzzerPin, HIGH); // Turn on buzzer
      digitalWrite(ledPin, HIGH);    // Turn on warning LED
    }
    // If Clear 'L' is received
    else if (command == 'L') {
      digitalWrite(buzzerPin, LOW);  // Turn off buzzer
      digitalWrite(ledPin, LOW);     // Turn off warning LED
    }
  }
}