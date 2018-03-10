/*
  Wiring code:
  C16A..20t       Gen
  blue/green  +E  red
  grey/black  -E  black
  red         -A  white
  white       +A  green

*/

//Pin Maping for scale and Micrometers
#define ledPin PC13
#define req1 PB9 
#define req2 PB8 
#define req3 PB7 
#define req4 PB6 
#define req5 PB5 
#define req6 PA8

#define dat1 PA6 
#define dat2 PA7 
#define dat3 PB0 
#define dat4 PB1 
#define dat5 PB10 
#define dat6 PB11

#define clk1 PA0 
#define clk2 PA1 
#define clk3 PA2 
#define clk4 PA3 
#define clk5 PA4 
#define clk6 PA5

#define dout PB12
#define sck PB13

#include <HX711.h> 
HX711 scale(dout, sck);

volatile int i1, i2, i3, i4, i5, i6=0;
volatile int k1, k2, k3, k4, k5, k6=0;
volatile int w1, w2, w3, w4, w5, w6=0;
 
volatile float value1,value2,value3,value4,value5,value6,load;
volatile bool flagLed,flagRead1,flagRead2,flagRead3,flagRead4,flagRead5,flagRead6=false;
volatile bool flagValid1,flagValid2,flagValid3,flagValid4,flagValid5,flagValid6=false;
volatile int mydata1[14],mydata2[14],mydata3[14],mydata4[14],mydata5[14],mydata6[14];

long t;


void setup() {
  // initialize digital pin PB1 as an output.
  Serial1.begin(9600); 
  Serial1.println("...start");

  Timer2.setChannel1Mode(TIMER_OUTPUTCOMPARE);
  Timer2.setPeriod(250000); // in microseconds
  Timer2.setCompare1(1); // overflow might be small
  Timer2.attachCompare1Interrupt(callback);

  pinMode(ledPin, OUTPUT);
  pinMode(req1,OUTPUT);pinMode(clk1,INPUT_PULLUP);pinMode(dat1,INPUT_PULLUP);
  pinMode(req2,OUTPUT);pinMode(clk2,INPUT_PULLUP);pinMode(dat2,INPUT_PULLUP);
  pinMode(req3,OUTPUT);pinMode(clk3,INPUT_PULLUP);pinMode(dat3,INPUT_PULLUP);
  pinMode(req4,OUTPUT);pinMode(clk4,INPUT_PULLUP);pinMode(dat4,INPUT_PULLUP);
  pinMode(req5,OUTPUT);pinMode(clk5,INPUT_PULLUP);pinMode(dat5,INPUT_PULLUP);
  pinMode(req6,OUTPUT);pinMode(clk6,INPUT_PULLUP);pinMode(dat6,INPUT_PULLUP);
  
  attachInterrupt(clk1, pulse1, FALLING); 
  attachInterrupt(clk2, pulse2, FALLING); 
  attachInterrupt(clk3, pulse3, FALLING); 
  attachInterrupt(clk4, pulse4, FALLING); 
  attachInterrupt(clk5, pulse5, FALLING); 
  attachInterrupt(clk6, pulse6, FALLING); 

  scale.read_average(20);
  scale.set_scale(1);                      // this value is obtained by calibrating the scale with known weights; see the README for details
  scale.tare(20);
}

void loop() {
  //get smoothed value from data set + current calibration factor
  if (millis() > t + 500)
  {

    load = scale.get_value(5);
    if (flagValid1==false) value1=999.99;
    if (flagValid2==false) value2=999.99;
    if (flagValid3==false) value3=999.99;
    if (flagValid4==false) value4=999.99;
    if (flagValid5==false) value5=999.99;
    if (flagValid6==false) value6=999.99;
    
    Serial1.print(value1,2);Serial1.print(",");
    Serial1.print(value2,2);Serial1.print(",");
    Serial1.print(value3,2);Serial1.print(",");
    Serial1.print(value4,2);Serial1.print(",");
    Serial1.print(value5,2);Serial1.print(",");
    Serial1.print(value6,2);Serial1.print(",");
    Serial1.print(load,2);
    Serial1.println();

    flagValid1=false;
    flagValid2=false;
    flagValid3=false;
    flagValid4=false;
    flagValid5=false;
    flagValid6=false;
    t = millis();
    /*
    // datinputdebug
    Serial1.print("dat:");
    Serial1.print(digitalRead(dat1));Serial1.print(digitalRead(dat2));Serial1.print(digitalRead(dat3));
    Serial1.print(digitalRead(dat4));Serial1.print(digitalRead(dat5));Serial1.print(digitalRead(dat6));
    Serial1.println();

    // clkinputdebug
    Serial1.print("clk:");
    Serial1.print(digitalRead(clk1));Serial1.print(digitalRead(clk2));Serial1.print(digitalRead(clk3));
    Serial1.print(digitalRead(clk4));Serial1.print(digitalRead(clk5));Serial1.print(digitalRead(clk6));
    Serial1.println();
    */
  }

}

volatile float processing(volatile int mydata[14])
{
  int decimal=0;
  long value_int;
  int sign;
  float value=0;
  sign = mydata[4];
  value_int = mydata[6]*10000 + mydata[7]*1000 + mydata[8]*100 + mydata[9]*10 + mydata[10]; 
  if (sign==8){value_int=value_int*(-1);}
  value = value_int/100.0; 
  return value;
}

void callback()
{
  digitalWrite(ledPin, flagLed); flagLed=!flagLed;

  if(flagRead1==false) {digitalWrite(req1, HIGH); flagRead1=true; k1=0; i1=0; w1=0;}
  else {digitalWrite(req1, LOW); flagRead1=false;}

  if(flagRead2==false) {digitalWrite(req2, HIGH); flagRead2=true; k2=0; i2=0; w2=0;}
  else {digitalWrite(req2, LOW); flagRead2=false;}

  if(flagRead3==false) {digitalWrite(req3, HIGH); flagRead3=true; k3=0; i3=0; w3=0;}
  else {digitalWrite(req3, LOW); flagRead3=false;}

  if(flagRead4==false) {digitalWrite(req4, HIGH); flagRead4=true; k4=0; i4=0; w4=0;}
  else {digitalWrite(req4, LOW); flagRead4=false;}

  if(flagRead5==false) {digitalWrite(req5, HIGH); flagRead5=true; k5=0; i5=0; w5=0;}
  else {digitalWrite(req5, LOW); flagRead5=false;}

  if(flagRead6==false) {digitalWrite(req6, HIGH); flagRead6=true; k6=0; i6=0; w6=0;}
  else {digitalWrite(req6, LOW); flagRead6=false;}
}




void pulse1()
{
if (flagRead1){
    bitWrite(k1, w1, (digitalRead(dat1) & 0x1)); 
  w1++;
  if (w1>3){
    mydata1[i1] = k1;
    k1=0;w1=0;
    i1++;}
  if (i1>13) {value1 = processing(mydata1); flagRead1=false;digitalWrite(req1, LOW); flagValid1=true;}
  }
}

void pulse2()
{
if (flagRead2){
    bitWrite(k2, w2, (digitalRead(dat2) & 0x1)); 
  w2++;
  if (w2>3){
    mydata2[i2] = k2;
    k2=0;w2=0;
    i2++;}
  if (i2>13) {value2 = processing(mydata2); flagRead2=false;digitalWrite(req2, LOW); flagValid2=true;}
  }
}

void pulse3()
{
if (flagRead3){
    bitWrite(k3, w3, (digitalRead(dat3) & 0x1)); 
  w3++;
  if (w3>3){
    mydata3[i3] = k3;
    k3=0;w3=0;
    i3++;}
  if (i3>13) {value3 = processing(mydata3); flagRead3=false;digitalWrite(req3, LOW); flagValid3=true;}
  }
}

void pulse4()
{
if (flagRead4){
    bitWrite(k4, w4, (digitalRead(dat4) & 0x1)); 
  w4++;
  if (w4>3){
    mydata4[i4] = k4;
    k4=0;w4=0;
    i4++;}
  if (i4>13) {value4 = processing(mydata4); flagRead4=false;digitalWrite(req4, LOW); flagValid4=true;}
  }
}

void pulse5()
{
if (flagRead5){
    bitWrite(k5, w5, (digitalRead(dat5) & 0x1)); 
  w5++;
  if (w5>3){
    mydata5[i5] = k5;
    k5=0;w5=0;
    i5++;}
  if (i5>13) {value5 = processing(mydata5); flagRead5=false;digitalWrite(req5, LOW); flagValid5=true;}
  }
}

void pulse6()
{
if (flagRead6){
    bitWrite(k6, w6, (digitalRead(dat6) & 0x1)); 
  w6++;
  if (w6>3){
    mydata6[i6] = k6;
    k6=0;w6=0;
    i6++;}
  if (i6>13) {value6 = processing(mydata6); flagRead6=false;digitalWrite(req6, LOW); flagValid6=true;}
  }
}
