int greenPin = 2;
int greenPin_ = 2;
int yellowPin = 3;
int redPin = 4;
int activePin;
int targetPin;
int targetPin2;

char trafficLamb_;
int trafficLamb;
char targetTLS_;
int targetTLS;
char targetTLS2_;
int targetTLS2;

int activeTLS;

char delayTLS_;
int delayTLS;

void setup() {
  Serial.begin(9600);

  for (int i = 2; i <= 13; i++) {
    pinMode(i, OUTPUT);
  }
}

void loop() {
  if (Serial.available() > 3) {

    trafficLamb_ = Serial.read();
    trafficLamb = trafficLamb_ - '0'; 
    
    // startSystem(greenPin, redPin, trafficLamb);

    targetTLS_ = Serial.read(); 
    targetTLS = targetTLS_ - '0'; 

    targetTLS2_ = Serial.read(); 
    targetTLS2 = targetTLS2_ - '0'; 

    // second
    delayTLS_ = Serial.read(); 
    delayTLS = delayTLS_ - '0'; 

    activeTLS = activeTLSPin(greenPin, trafficLamb);
    activePin = (activeTLS - 1) * 3 + 2;
    targetPin = TargetPin(greenPin, targetTLS);
    targetPin2 = TargetPin(greenPin, targetTLS2);

    // control
    getGreen(delayTLS, activePin, targetPin);

    activePin = targetPin;

    getYellow(activePin, targetPin2);
  }
    
}

void highLED(int pin){
  digitalWrite(pin, HIGH);
}

void lowLED(int pin){
  digitalWrite(pin, LOW);
}

void getGreen(int delayTLS, int active, int target){
  // target pin 8 || active pin 2

  // open green
  highLED(target);
  highRed(delayTLS, 'g');

  delay(delayTLS*1000);
  
  // close green
  lowRed(delayTLS, 'g');
  lowLED(target);
}

void getYellow(int active, int target){
  // open yellow
  highLED(target+1);
  // open yellow
  highLED(active+1);

  highRed(0, 'y');
  

  delay(2500);

  lowRed(0, 'y');

  // close yellow
  lowLED(target+1);
  // close yellow
  lowLED(active+1);


}

void highRed(int delayTLS, char mode){
  if (mode == 'g'){
    for (int tls=1; tls <= trafficLamb; tls++) {
      if(targetTLS == tls){
        lowLED(tls*3+1);
      } else {
        highLED(tls*3+1);
      }
    }
  } else if (mode == 'y'){
    for (int tls=1; tls <= trafficLamb; tls++) {
      if(targetTLS == tls || targetTLS2 == tls){
        lowLED(tls*3+1);
      } else {
        highLED(tls*3+1);
      }
    }
  }

}

void lowRed(int delayTLS, char mode){
  if (mode == 'g'){
    for (int tls=1; tls <= trafficLamb; tls++) {
      if(activeTLS == tls){
        highLED(tls*3+1);
      } else {
        lowLED(tls*3+1);
      }
    }
  } else if (mode == 'y'){
    for (int tls=1; tls <= trafficLamb; tls++) {
      if(targetTLS2 == tls){
        lowLED(tls*3+1);
      } else {
        highLED(tls*3+1);
      }
    }
  }

}

void startSystem(int greenP, int redP, int trafficL){
  highLED(greenP);
  for (int pin = redP + 3; pin < 13; pin += trafficL){
    highLED(pin);
  }
  delay(5000);
}

bool isPinHigh(int pin) {
    return digitalRead(pin) == HIGH;
}

// return activeTLSPin
int activeTLSPin(int pin, int trafficL) {
  for (int p = pin; p < 13; p += trafficL){
    if (isPinHigh(p)) {
      return (int)((p / 2) + 1);;
    }
  }
  return 1;
}

// return targetPin
int TargetPin(int pin, int target){
  return (pin + ((target - 1) * 3));
}