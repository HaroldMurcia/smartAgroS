#include <OneWire.h>              //--->Sonda DS18B20
#include <DallasTemperature.h>    //--->Sonda DS18B20
#include <Wire.h>                 //--->Flora Light
#include "TSL2561.h"              //--->Flora Light
#include <SHT1x.h>                //--->Sensor Tem,Hum
#include <avr/sleep.h>            //--->Sleep 3526
#include <avr/power.h>            //--->Power Mode 
#include <avr/wdt.h>              //--->WatchDog Mode
#include <ResponsiveAnalogRead.h> //--->Filtrado y Normalizado
ResponsiveAnalogRead PT11Average(A0,true);
ResponsiveAnalogRead PT12Average(A1,true);
ResponsiveAnalogRead Lm35Average(A10,true);
ResponsiveAnalogRead BattAverage(A11,true);
ResponsiveAnalogRead SS14Average(A14,true);
ResponsiveAnalogRead SS15Average(A15,true);
SHT1x sht1x(22,23);               //----(dataPin, clockPin)      
TSL2561 tsl(TSL2561_ADDR_FLOAT);
OneWire oneWire_in1(A12);
OneWire oneWire_in2(A13);
DallasTemperature DS18B201(&oneWire_in1);
DallasTemperature DS18B202(&oneWire_in2);

int flag_ini = 1;

int PinesOUT[]={2,6,7,8,9,10,13,25,28,45,43,48,52,53};
int PinesIN[]={11,12,29,31,51,47,49,A3,A4,A5}; 


volatile int f_wdt=1;             // WathDogTImer
int FV,FI,FL,V1,V2,mode,HS;
int Si,Fl,Sh,Pt,Ds,Bt,Lf,Lm,Sw;
float DS181,DS182,DS181R,PT11Tem,PT12Tem,Vb,TemInterna,uvIntensity,Res,R,ResR;
float x[5]; // Las 5 muestras para su posterior procesado
float supplyVoltage = 0;                   // La salida del filtro
float x1[5]; // Las 5 muestras para su posterior procesado
float sensorValue = 0; // La salida del filtro
float x2[5]; // Las 5 muestras para su posterior procesado
float supplyVoltage2 = 0;                   // La salida del filtro
float x3[5]; // Las 5 muestras para su posterior procesado
float sensorValue2 = 0; 
float ResA[2];

float Res1=0;
float Res2=0;
float knownResistor = 10000;  // Constant value of known resistor in Ohms
float voltage1,voltage2,voltage3,voltage4,voltage1F,voltage2F,voltage3F,voltage4F;
float ElapsedTime,tic,toc;
int val=0;
int val1=0;
int Estado;
int Riego;
int Activacion;
int button=0;
float const Ts=600000;
float X,P;
int long SleepCycles;
  float temp_c;
  float temp_f;
  float humidity;
  
struct DATA {
    float meassurement;
    float P;
    float Q;
    float R;
    float X;
  };
 
DATA SOILM={0,1e3,0.5e-3,0.01,0};
DATA LUX={0,1e3,0.5e-3,0.9818,0};  
DATA RES={0,1e3,0.5e-3,0.01,0};
// ------------------
void ConfigPines(){
int Pin,NOUT,NIN,NAUX;
NOUT  = sizeof(PinesOUT)/2;
NIN   = sizeof(PinesIN)/2;
//NAUX  = sizeof(PinesAUX)/2;
for(Pin=0; Pin<NOUT; Pin++){pinMode(PinesOUT[Pin],OUTPUT);}
for(Pin=0; Pin<NIN; Pin++) {pinMode(PinesIN[Pin],INPUT);}
//for(Pin=0; Pin<NAUX; Pin++){pinMode(PinesAUX[Pin],INPUT);}
}
void LedsPulsadores(){
//LEDS (7,8,9,10) - Pulsadores (11,12)
digitalWrite(7,!digitalRead(11));
digitalWrite(8,!digitalRead(12));
digitalWrite(9,LOW);
digitalWrite(10,LOW);
digitalWrite(13,LOW);
}
void Cooler(){
if(TemInterna >= 40.0){
digitalWrite(25,HIGH);  
}else{digitalWrite(25,LOW);}
}
void Buzzer(){
digitalWrite(28,!digitalRead(11));
}
void Sensor(){
digitalWrite(2,HIGH);
delay(10);
}
void SensorOFF(){
digitalWrite(2,LOW);

}
void XbeeON(){
digitalWrite(48,HIGH);
}
void XbeeOFF(){
digitalWrite(48,LOW);
}
void XbeeSleepON(){
digitalWrite(6,HIGH);
}
void XbeeSleepOFF(){
digitalWrite(6,LOW);
}
void Lm35(){
Lm35Average.update();
TemInterna=((Lm35Average.getValue()*407.0)/1024.0);
delay(100);
//Serial.print2ln(TemInterna); 
}
void Bateria(){
BattAverage.update(); 

//Vb=BattAverage.getValue();
Vb=((BattAverage.getValue()* 0.0048));
//Serial.println(Vb); 
}
void Pt100_1(){
PT11Average.update();
PT11Tem=PT11Average.getValue()*4.8828/8.2;
//Serial.println(PT11Tem); 
}
void Pt100_2(){
PT12Average.update();
PT12Tem=(PT12Average.getValue()*0.4473-3.1594);
//Serial.println(PT12Tem); 
}
void MH8511(){
int uvLevel = averageAnalogRead(A3);
int refLevel = averageAnalogRead(A4);
float outputVoltage = 3.3 / refLevel * uvLevel;
uvIntensity = mapfloat(outputVoltage, 0.99, 2.8, 0.0, 15.0);
delay(100);
}
void DS18B20_1(){
float DS18;
DS18B201.begin();                    delay(10);
DS18B201.requestTemperatures();      delay(1);
DS181=(DS18B201.getTempCByIndex(0));  delay(1);
DS181R=DS181* 0.8651    +4.8444; 
//Serial.println(DS181);
}
void DS18B20_2(){
float DS18;
DS18B202.begin();                    delay(10);
DS18B202.requestTemperatures();      delay(1);
DS182=(DS18B202.getTempCByIndex(0));  delay(1);
DS182=DS182* 0.8651    +4.8444; 
//Serial.println(DS182);  
}
void Bomba(){

button = digitalRead(47);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
if (button == HIGH){
    // turn LED on:
  
    digitalWrite(45,LOW);
    Riego=1;
    delay(35000);
    digitalWrite(45,HIGH);
   }
else if (button == LOW ) {
    // turn LED off:
    
    digitalWrite(45, HIGH);
    Riego=0;
    
  }
}
void WebBomba(){
   if(Serial.available()){
    //Leemos el primer caracter(pin)
    //Leemos el segundo caracter(Estado)
   char pin = Serial.read();
   char mode = Serial.read();  
   //En funcion del pin recibido se realiza una operacion
   switch(pin){
      case '5':
        ligths(45,mode);
      break;
      case '9':
        ligths(9,mode);
      break;
      case '0':
        ligths(10,mode);
      break;
   } 
  }
  delay(250);
 
}
//Esta funcion enciende o apaga un led en funcion del pin y del modo recibido.
void ligths(byte pin,char mode){
  if(mode=='H'){
    digitalWrite(pin,LOW);
    delay(15000);
    Riego=1;
 
    
  }else{
       if(mode=='L')
          digitalWrite(pin, HIGH);
          Riego=0;   
  }
  
 }
void Bomba1(){
// Ciclo 1
//
//    if( HS > 390 && FL >10){
//      Riego=1;
//      digitalWrite(45,LOW);
//      delay(25000);
//      digitalWrite(45,HIGH);
//
//
//
//    }else if( HS < 370 && FL >10){
//        Riego=0;
//        digitalWrite(45,HIGH);        
//     } 
//     if (FL==0){
//      Riego=0;
//      digitalWrite(45,HIGH);   
//     }
//  }


// Ciclo 2
//   if( HS > 390 && FL == 0 && DS181R < 25.0 ){
//      Riego=1;
//      digitalWrite(45,LOW);
//      delay(25000);
//      digitalWrite(45,HIGH);
//
//
//
//   }else if( HS < 370 && FL >10 && DS181R < 25.0){
//        Riego=0;
//        digitalWrite(45,HIGH);        
//   } 
//     if (FL>0){
//      Riego=0;
//      digitalWrite(45,HIGH);   
//     }
//  }

  
// Ciclo 3
     if( HS > 390 && FL >10 && DS181R < 25.0 ){
      Riego=1;
      digitalWrite(45,LOW);
      delay(25000);
      digitalWrite(45,HIGH);



    }else if( HS < 370 && FL >10 && DS181R < 25.0){
        Riego=0;
        digitalWrite(45,HIGH);        
     } 
     if (FL==0){
      Riego=0;
      digitalWrite(45,HIGH);   
     }
  }


void Tanque(){
val= digitalRead(51);
val1= digitalRead(49);
delay(200);
if(val==1 && val1==1){
  Estado=0;
  }
if(val==0 && val1==0)
{
  Estado=2;
}

if(val==1 && val1==0)
{
  Estado=1;
}
}
void SoilSensor(){
  
  HS = averageAnalogRead(A5);
}
void S200SS(){

  digitalWrite(53, HIGH); 
  digitalWrite(52, LOW);
  delay(5000);
  supplyVoltage = analogRead(A15);
  delay(25);
  sensorValue = analogRead(A14);
  delay(25);
//  SS15Average.update();
//  SS14Average.update();
  x[0] = (supplyVoltage* (5.0 / 1024.0));
//  voltage1F=(SS15Average.getValue()* (5.0 / 1024.0));
//  Serial.print(voltage1F);
//  voltage1F=((0.5*voltage1F)+0.5*voltage1);

  if (flag_ini == 1) {
     x[1]=x[0];
     x[2]=x[0];
     x[3]=x[0];
     x[4]=x[0];
  }

  voltage1F=(x[0] + x[1] + x[2] + x[3] + x[4])/5.0;
  x[4] = x[3]; // Actualizamos los valores de las muestras
  x[3] = x[2];
  x[2] = x[1];
  x[1] = x[0];
  
  x1[0] = (sensorValue * (5.0 / 1024.0));
//  voltage2F=((0.5*voltage2F)+0.5*voltage2);
//  voltage2F=(SS14Average.getValue()* (5.0 / 1024.0));
//  Serial.print(voltage2F);
  if (flag_ini == 1) {
     x1[1]=x1[0];
     x1[2]=x1[0];
     x1[3]=x1[0];
     x1[4]=x1[0];
  }
  
  voltage2F=(x1[0] + x1[1] + x1[2] + x1[3] + x1[4])/5.0;
  x1[4] = x1[3];               // Actualizamos los valores de las muestras
  x1[3] = x1[2];
  x1[2] = x1[1];
  x1[1] = x1[0];
  Res1=(((voltage1F *knownResistor )/voltage2F)-knownResistor);
//  Serial.println(Res1);
  digitalWrite(53, LOW); 
  digitalWrite(52, HIGH);
  delay(5000);
  supplyVoltage = analogRead(A14);
  delay(25);
  sensorValue = analogRead(A15);
  delay(25);
//  SS14Average.update();
//  SS15Average.update();
  x2[0] = (supplyVoltage* (5.0 / 1024.0));
//  voltage3F=(SS14Average.getValue()* (5.0 / 1024.0));;
//  Serial.print(voltage3F);
  if (flag_ini == 1) {
     x2[1]=x2[0];
     x2[2]=x2[0];
     x2[3]=x2[0];
     x2[4]=x2[0];
  }
  voltage3F = (x2[0] + x2[1] + x2[2] + x2[3] + x2[4])/5;
  x2[4] = x2[3];               // Actualizamos los valores de las muestras
  x2[3] = x2[2];
  x2[2] = x2[1];
  x2[1] = x2[0];
  x3[0] = (sensorValue * (5.0 / 1024.0));

  if (flag_ini == 1) {
     x3[1]=x3[0];
     x3[2]=x3[0];
     x3[3]=x3[0];
     x3[4]=x3[0];
     flag_ini = 0;
  }
  
  voltage4F =(x3[0] + x3[1] + x3[2] + x3[3] + x3[4])/5;
  x3[4] = x3[3];               // Actualizamos los valores de las muestras
  x3[3] = x3[2];
  x3[2] = x3[1];
  x3[1] = x3[0];
  
}


void HumedadS200ss(){
  if (ResR <= 8000){
   R=ResR/1000;
   HS =(-3.213*R-4.093)/(1.0 -0.009733*R - 0.01205*DS181R);
       
  }else if (ResR > 8000){
   R=ResR/1000;
   HS =-2.246-5.239*R*(1.0+0.018*(DS181R-24.0)) - 0.06756*(R*R)*((1.0+0.018*(DS181R-24.0))*(1.0+0.018*(DS181R-24.0)));
   
  }
   }
void Flora(){
tsl.begin();
tsl.setGain(TSL2561_GAIN_0X);
tsl.setTiming(TSL2561_INTEGRATIONTIME_13MS);
uint16_t x = tsl.getLuminosity(TSL2561_VISIBLE);     
uint32_t lum = tsl.getFullLuminosity();
uint16_t ir, full;
ir = lum >> 16;
full = lum & 0xFFFF;
FV =(full - ir);                  
FI =(ir);                                
FL =(tsl.calculateLux(full, ir)); 
delay(100);  
}
void SHT10(){
  // Read values from the sensor
  temp_c = sht1x.readTemperatureC();
  temp_f = sht1x.readTemperatureF();
  humidity = sht1x.readHumidity();  
}
void Filtro(float meassurement, float p, float Q, float R, float x){
  p=p+Q;
  float K=p/(p+R);
  x=x+K*(meassurement-x);
  p=(1-K)*p;
  //P_1=P;
  X=x; P=p; 
}
void PrintData(){
// Light Flora
switch(mode){
case 0:
Serial.print("FV:");Serial.print(FV);Serial.print('\t'); 
Serial.print("FI:");Serial.print(FI);Serial.print('\t');
Serial.print("FL:");Serial.print(FL);Serial.print('\t');
Serial3.print("FV:");Serial3.print(FV);Serial3.print('\t'); 
Serial3.print("FI:");Serial3.print(FI);Serial3.print('\t');        
Serial3.print("FL:");Serial3.print(FL);Serial3.print('\t');
break;
case 1:
Serial3.print("FV:");Serial3.print(FV);Serial3.print('\t'); 
Serial3.print("FI:");Serial3.print(FI);Serial3.print('\t');
Serial3.print("FL:");Serial3.print(FL);Serial3.print('\t');
break;}
// MH8511 UV Sensor
switch(mode){
case 0:
Serial.print("UV:");  Serial.print(uvIntensity);Serial.print('\t'); 
Serial3.print("UV:"); Serial3.print(uvIntensity);Serial3.print('\t'); 
break;
case 1:
Serial3.print("UV:"); Serial3.print(uvIntensity);Serial3.print('\t');
break;} 
// SHT10
switch(mode){
case 0:
//Serial.print("SHT:");Serial.print(temp_c);Serial.print('\t');
Serial.print("SHH:");Serial.print(humidity);Serial.print('\t');
Serial3.print("SHT:");Serial3.print(temp_c);Serial3.print('\t');
Serial3.print("SHH:");Serial3.print(humidity);Serial3.print('\t'); 
break;
case 1:
Serial3.print("SHT:");Serial3.print(temp_c);Serial3.print('\t');
Serial3.print("SHH:");Serial3.print(humidity);Serial3.print('\t');
break;}    
// PT100
switch(mode){
case 0:
Serial.print("PT:");   Serial.print(PT11Tem); Serial.print('\t');
//Serial.print("pt100-temp2=");Serial.print(PT12Tem); Serial.print('\t');
Serial3.print("PT:");  Serial3.print(PT11Tem);Serial3.print('\t');
//Serial3.print("PT2"); Serial3.print(PT12Tem);Serial3.print('\t');
break;
case 1:
Serial3.print("PT:");  Serial3.print(PT11Tem);Serial3.print('\t');
//Serial3.print("PT2"); Serial3.print(PT12Tem);Serial3.print('\t');
break;}
// SondaDS18B20
switch(mode){
case 0:
Serial.print("DST:");Serial.print(DS181R);Serial.print('\t');
Serial3.print("DST:");Serial3.print(DS181R);Serial3.print('\t');
break;
case 1:
Serial3.print("DST:");Serial3.print(DS181R);Serial3.print('\t');
break;}
// SoilWater
switch(mode){
case 0:
Serial.print("Res:");Serial.print(ResR);Serial.print('\t');
Serial.print("HS:");Serial.print(HS);Serial.print('\t');
Serial3.print("Res:"); Serial3.print(ResR);Serial3.print('\t'); 
Serial3.print("HS:"); Serial3.print(HS);Serial3.print('\t'); 
break;
case 1:
Serial3.print("Res:");Serial3.print(Res);Serial3.print('\t'); 
Serial3.print("HS:"); Serial3.print(SOILM.X);Serial3.print('\t'); 
break;}
//Tanque
switch(mode){
case 0:
Serial.print("TQ:");Serial.print(Estado);Serial.print('\t');
Serial3.print("TQ:");Serial3.print(Estado);Serial3.print('\t');
break;
case 1:
Serial3.print("TQ:");Serial3.print(Estado);Serial3.print('\t');
break;}
//Bomba
switch(mode){
case 0:
Serial.print("RI:");Serial.print(Riego);Serial.print('\t');
Serial3.print("RI:");Serial3.print(Riego);Serial3.print('\t');
break;
case 1:
Serial3.print("RI:");Serial3.print(Riego);Serial3.print('\t');
break;}
//// Battery
//switch(mode){
//case 0:
//Serial.print("BT:");Serial.print(Vb);Serial.print('\t');
//Serial3.print("BT");Serial3.print(Vb);Serial3.print('\t');
//break; 
//case 1:
//Serial3.print("BT:");Serial3.print(Vb);Serial3.print('\t');
//break;}
// LM35 - Internal Temperature
switch(mode){
case 0:
Serial.print("TI:");Serial.println(TemInterna);
Serial3.print("TI:");Serial3.println(TemInterna);
break; 
case 1:
Serial3.print("TI:");Serial3.println(TemInterna);   
break;}  
}
void enterSleep(void){
    set_sleep_mode(SLEEP_MODE_PWR_DOWN);
    sleep_enable();
    sleep_mode();
    sleep_disable();
    power_all_enable();
}
void setupWatchDogTimer() {
    MCUSR &= ~(1<<WDRF);
    WDTCSR |= (1<<WDCE) | (1<<WDE);
    WDTCSR  = (0<<WDP3) | (1<<WDP2) | (1<<WDP1) | (0<<WDP0);
    WDTCSR |= _BV(WDIE);
}
ISR(WDT_vect){if(f_wdt == 0){f_wdt=1;}}

void setup(){
digitalWrite(45, HIGH);  
Serial.begin(9600);
Serial3.begin(57600);
flag_ini= 1;
ConfigPines(); 

mode=0;
setupWatchDogTimer();
}
void loop(){tic=millis();if(f_wdt!=1){return;}
  digitalWrite(45, HIGH);
  LedsPulsadores();
  Cooler();
  //Buzzer();
  Sensor();
  XbeeON();
  XbeeSleepOFF();
  Lm35();
  //Bateria();
  Pt100_1();
  //Pt100_2();
  MH8511();
  DS18B20_1();
  Flora();
  SHT10();
//DS18B20_2();
  Tanque();
  SoilSensor();
  //S200SS();
  //Humedad();
  Bomba();
  WebBomba();
  //Bomba1();
  PrintData();
  delay(2000);
//  XbeeOFF();
  SensorOFF();
//  digitalWrite(53, LOW); 
//  digitalWrite(52, LOW);
// Tiempo de espera para cada toma de datos.
// En la Aplicacion Web--> tiempo 0
  toc=millis();SleepCycles=550;//550 -> 10M
  f_wdt = 0;for (int i=0; i <= SleepCycles; i++){enterSleep();}
}

int averageAnalogRead(int pinToRead){
byte numberOfReadings = 8;
unsigned int runningValue = 0; 
for(int x = 0 ; x < numberOfReadings ; x++)
runningValue += analogRead(pinToRead);
runningValue /= numberOfReadings;
return(runningValue);  
}
float mapfloat(float x, float in_min, float in_max, float out_min, float out_max){
return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
