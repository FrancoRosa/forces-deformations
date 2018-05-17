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
#define req1 PB0 

#define dat1 PB9
#define dat2 PB8
#define dat3 PB7
#define dat4 PB6 
#define dat5 PB5 
#define dat6 PB4 
#define dat7 PA12 
#define dat8 PA15 

#define clk1 PA0 
#define clk2 PA1 
#define clk3 PA2 
#define clk4 PA3 
#define clk5 PA4 
#define clk6 PA5
#define clk7 PA6
#define clk8 PA7

#define dout1 PB15
#define sck1  PB14
#define dout2 PB13
#define sck2  PB12

#include <HX711.h> 
HX711 scale1(dout1, sck1);
HX711 scale2(dout2, sck2);

volatile int i1, i2, i3, i4, i5, i6, i7, i8=0;
volatile int k1, k2, k3, k4, k5, k6, k7, k8=0;
volatile int w1, w2, w3, w4, w5, w6, w7, w8=0;
volatile int mydata1[14];
volatile int mydata2[14];
volatile int mydata3[14];
volatile int mydata4[14];
volatile int mydata5[14];
volatile int mydata6[14];
volatile int mydata7[14];
volatile int mydata8[14];
volatile int count1,count2,count3,count4,count5,count6,count7,count8;
 
volatile float value1,value2,value3,value4,value5,value6,value7,value8,load1,load2,load3,load4;
volatile bool flagLed,flagRead1,flagRead2,flagRead3,flagRead4,flagRead5,flagRead6,flagRead7,flagRead8=false;
volatile bool flagValid1,flagValid2,flagValid3,flagValid4,flagValid5,flagValid6,flagValid7,flagValid8=false;
volatile bool flagReq;
long t;


void setup() {
  Serial1.begin(115200); 
  Serial1.println("...start - Uni - test");

  Timer2.setChannel1Mode(TIMER_OUTPUTCOMPARE);
  Timer2.setPeriod(200000); // in microseconds
  Timer2.setCompare1(1); // overflow might be small
  Timer2.attachCompare1Interrupt(callback);

  Timer3.setChannel1Mode(TIMER_OUTPUTCOMPARE);
  Timer3.setPeriod(1000); // in microseconds
  Timer3.setCompare1(1); // overflow might be small
  Timer3.attachCompare1Interrupt(callbackms);


  pinMode(ledPin, OUTPUT);
  pinMode(req1,OUTPUT);
  pinMode(clk1,INPUT_PULLUP);pinMode(dat1,INPUT_PULLUP);
  pinMode(clk2,INPUT_PULLUP);pinMode(dat2,INPUT_PULLUP);
  pinMode(clk3,INPUT_PULLUP);pinMode(dat3,INPUT_PULLUP);
  pinMode(clk4,INPUT_PULLUP);pinMode(dat4,INPUT_PULLUP);
  pinMode(clk5,INPUT_PULLUP);pinMode(dat5,INPUT_PULLUP);
  pinMode(clk6,INPUT_PULLUP);pinMode(dat6,INPUT_PULLUP);
  pinMode(clk7,INPUT_PULLUP);pinMode(dat7,INPUT_PULLUP);
  pinMode(clk8,INPUT_PULLUP);pinMode(dat8,INPUT_PULLUP);

  attachInterrupt(clk1, pulse1, FALLING); 
  attachInterrupt(clk2, pulse2, FALLING); 
  attachInterrupt(clk3, pulse3, FALLING); 
  attachInterrupt(clk4, pulse4, FALLING); 
  attachInterrupt(clk5, pulse5, FALLING); 
  attachInterrupt(clk6, pulse6, FALLING); 
  attachInterrupt(clk7, pulse7, FALLING); 
  attachInterrupt(clk8, pulse8, FALLING); 

}

void loop() {
    load1 = scale1.get_value(7);
    //scale1.set_gain(128); load1 = scale1.get_value(1);
    //scale1.set_gain(32);  load2 = scale1.get_value(1);
    //scale2.set_gain(128); load3 = scale2.get_value(1);
    //scale2.set_gain(32);  load4 = scale2.get_value(1);


    if (flagValid1==false) value1=999.99;
    if (flagValid2==false) value2=999.99;
    if (flagValid3==false) value3=999.99;
    if (flagValid4==false) value4=999.99;
    if (flagValid5==false) value5=999.99;
    if (flagValid6==false) value6=999.99;
    if (flagValid7==false) value7=999.99;
    if (flagValid8==false) value8=999.99;
    
    Serial1.print(value1,2);Serial1.print(",");
    Serial1.print(value2,2);Serial1.print(",");
    Serial1.print(value3,2);Serial1.print(",");
    Serial1.print(value4,2);Serial1.print(",");
    Serial1.print(value5,2);Serial1.print(",");
    Serial1.print(value6,2);Serial1.print(",");
    Serial1.print(value7,2);Serial1.print(",");
    Serial1.print(value8,2);Serial1.print(",");
    Serial1.print(load1,2);
    //Serial1.print(load2,2);Serial1.print(",");
    //Serial1.print(load3,2);Serial1.print(",");
    //Serial1.print(load4,2);
    Serial1.println();

    flagValid1=false;
    flagValid2=false;
    flagValid3=false;
    flagValid4=false;
    flagValid5=false;
    flagValid6=false;
    flagValid7=false;
    flagValid8=false;
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
  flagReq=!flagReq;
  if (flagReq) digitalWrite(req1, LOW); else digitalWrite(req1, HIGH);
}

void callbackms()
{
  count1++;count2++;count3++;count4++;count5++;count6++;count7++;count8++;
  if (count1>1000) count1=0;
  if (count2>1000) count2=0;
  if (count3>1000) count3=0;
  if (count4>1000) count4=0;
  if (count5>1000) count5=0;
  if (count6>1000) count6=0;
  if (count7>1000) count7=0;
  if (count8>1000) count8=0;
}

void pulse1()
{
digitalWrite(ledPin, flagLed); flagLed=!flagLed;
if (count1>50) {flagRead1=true;}
if (flagRead1)
  {
  bitWrite(k1, w1, (digitalRead(dat1) & 0x1)); 
  w1++;
  if (w1>3){
    mydata1[i1] = k1;
    k1=0;w1=0;
    i1++;}
  if (i1>13) {i1=0;k1=0;w1=0; value1 = processing(mydata1); flagRead1=false; flagValid1=true;}
  }
count1=0;
}

void pulse2()
{
digitalWrite(ledPin, flagLed); flagLed=!flagLed;
if (count2>50) {flagRead2=true;}
if (flagRead2){
    bitWrite(k2, w2, (digitalRead(dat2) & 0x1)); 
  w2++;
  if (w2>3){
    mydata2[i2] = k2;
    k2=0;w2=0;
    i2++;}
  if (i2>13) {k2=0; i2=0; w2=0;value2 = processing(mydata2); flagRead2=false; flagValid2=true;}
  }
count2=0;  
}

void pulse3()
{
digitalWrite(ledPin, flagLed); flagLed=!flagLed;
if (count3>50) {flagRead3=true;}
if (flagRead3){
    bitWrite(k3, w3, (digitalRead(dat3) & 0x1)); 
  w3++;
  if (w3>3){
    mydata3[i3] = k3;
    k3=0;w3=0;
    i3++;}
  if (i3>13) {k3=0; i3=0; w3=0;value3 = processing(mydata3); flagRead3=false; flagValid3=true;}
  }
count3=0;  
}

void pulse4()
{
digitalWrite(ledPin, flagLed); flagLed=!flagLed;
if (count4>50) {flagRead4=true;}
if (flagRead4){
    bitWrite(k4, w4, (digitalRead(dat4) & 0x1)); 
  w4++;
  if (w4>3){
    mydata4[i4] = k4;
    k4=0;w4=0;
    i4++;}
  if (i4>13) {k4=0; i4=0; w4=0; value4 = processing(mydata4); flagRead4=false; flagValid4=true;}
  }
count4=0;  
}

void pulse5()
{
digitalWrite(ledPin, flagLed); flagLed=!flagLed;
if (count5>50) {flagRead5=true;}
if (flagRead5){
    bitWrite(k5, w5, (digitalRead(dat5) & 0x1)); 
  w5++;
  if (w5>3){
    mydata5[i5] = k5;
    k5=0;w5=0;
    i5++;}
  if (i5>13) {k5=0; i5=0; w5=0;value5 = processing(mydata5); flagRead5=false; flagValid5=true;}
  }
count5=0;  
}

void pulse6()
{
digitalWrite(ledPin, flagLed); flagLed=!flagLed;
if (count6>50) {flagRead6=true;}
if (flagRead6){
    bitWrite(k6, w6, (digitalRead(dat6) & 0x1)); 
  w6++;
  if (w6>3){
    mydata6[i6] = k6;
    k6=0;w6=0;
    i6++;}
  if (i6>13) {k6=0; i6=0; w6=0;value6 = processing(mydata6); flagRead6=false; flagValid6=true;}
  }
count6=0;  
}


void pulse7()
{
digitalWrite(ledPin, flagLed); flagLed=!flagLed;
if (count7>50) {flagRead7=true;}
if (flagRead7){
    bitWrite(k7, w7, (digitalRead(dat7) & 0x1)); 
  w7++;
  if (w7>3){
    mydata7[i7] = k7;
    k7=0;w7=0;
    i7++;}
  if (i7>13) {k7=0; i7=0; w7=0;value7 = processing(mydata7); flagRead7=false; flagValid7=true;}
  }
count7=0;  
}

void pulse8()
{
digitalWrite(ledPin, flagLed); flagLed=!flagLed;
if (count8>50) {flagRead8=true;}
if (flagRead8){
    bitWrite(k8, w8, (digitalRead(dat8) & 0x1)); 
  w8++;
  if (w8>3){
    mydata8[i8] = k8;
    k8=0;w8=0;
    i8++;}
  if (i8>13) {k8=0; i8=0; w8=0;value8 = processing(mydata8); flagRead8=false; flagValid8=true;}
  }
count8=0;  
}
