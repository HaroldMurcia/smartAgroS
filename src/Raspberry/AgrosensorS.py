#coding: utf-8
import serial,time,requests,os,sys
import datetime
import urllib
import httplib
import smtplib, socket,fcntl, struct
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
##from PIL import Image
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import pickle


arduino = serial.Serial('/dev/ttyACM0', 9600)

urlTest='https://thingspeak.com'
timeoutTest=5
Ruta='/home/pi/Desktop/Agrosensor/Data/'

THINGSPEAKURL  ='https://api.thingspeak.com/channels/487900'
THINGSPEAKKEY  ='13CH4NRJ6PM9A07K'

varNames=['FI', 'FV', 'FL', 'PT', 'DST', 'Res', 'HS', 'TQ', 'RI','PRE' ]
FI=''; FV=''; FL=''; PT=''; DST=''; Res=''; HS=''; TQ=''; RI=''; PRE='';

#System
ErrorMode=0; InternetFail=0; DataReport=0; StartReport=0; myiP='0.0.0.0'
cont=0;


def createFile():
    global fileText
    fileText=Ruta+time.strftime("%d-%m-%y")+'-'+time.strftime("%I-%M-%S")+".txt"
    print("Fichero: "+fileText+"\n")
    f = open(fileText,'w')
    f.close()


def GuardarDatos():
         data=Serial
         data=data.strip()
         print('dato:' + data)
##         Fichero = open ('Datos.txt','a')
         Times='\t'+'Date:'+time.strftime("%d-%m-%y")+'\t'+'Time: '+time.strftime("%I-%M-%S")+'\r\n'
         f.write(Times + data)
         
def ReadData(dataRaw): 
    global varNames, FI,FV,FL,PT,DST,Res,HS,TQ,RI,PRE
    global Luz,Temperatura,Humedad,Tanque,Riego,prediccion
    L=len(dataRaw)
    for k in range (0,L-1):
        try:
            var,aux= dataRaw[k].split(':')
            print(aux)
            
        except:
            aux=''
        print(aux)
        print(dataRaw[k])
        # Variable Cases
        if varNames[2] in dataRaw[k]:
            if(aux!=''):
                FL=float(aux)
                Luz=aux
                
            else:
                FL=''
        elif varNames[4] in dataRaw[k]:
            if(aux!=''):
                DST=float(aux)
                Temperatura=aux
            else:
                DST=''
    
        elif varNames[6] in dataRaw[k]:
            if(aux!=''):
                HS=float(aux)
                Humedad=aux
            else:
                HS=''
            
        elif varNames[7] in dataRaw[k]:
            if(aux!=''):
                TQ=float(aux)
                Tanque=aux
                
            else:
                TQ=''
                
        elif varNames[8] in dataRaw[k]:
            if(aux!=''):
                RI=float(aux)
                Riego=aux
            else:
                RI=''
        elif varNames[9] in dataRaw[k]:
            if(aux!=''):
                PRE=float(aux)
                prediccion=aux
            else:
                PRE=''
            
        else:
           print ('No dato')
def ReadData2(dataRaw): 
    global varNames, FI,FV,FL,PT,DST,Res,HS,TQ,RI,PRE
    global Luz,Temperatura,Humedad,Tanque,Riego,prediccion
    L=len(dataRaw)
    for k in range (0,L-1):
        try:
            var,aux= dataRaw[k].split(':')
            print(aux)
            
        except:
            aux=''
        print(aux)
        print(dataRaw[k])
        # Variable Cases
        if varNames[8] in dataRaw[k]:
            if(aux!=''):
                RI=float(aux)
                Riego=aux
            else:
                RI=''
        elif varNames[9] in dataRaw[k]:
            if(aux!=''):
                PRE=float(aux)
                prediccion=aux
            else:
                PRE=''
            
        else:
           print ('No dato')           

def sendEmail(toaddr,subject,body,fileData):
	msg = MIMEMultipart()
	if(fileData!=''):
		msg.attach(MIMEText(file(fileData).read()))
	fromaddr='danilot275@gmail.com'
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subject
	msg.attach(MIMEText(body, 'plain'))
	mailer = smtplib.SMTP('smtp.gmail.com', 587)
	mailer.starttls()
	mailer.login(fromaddr, "lorenzoelrey6")
	text = msg.as_string()
	mailer.sendmail(fromaddr, toaddr, text)
	mailer.quit()
def getIpAddress(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def InternetTest():
    global InternetFail, StartReport, myiP
    try:
        r = requests.get(urlTest, timeout=timeoutTest)
        print("Internet ok. \n")
        InternetFail=0
        #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #s.connect(("gmail.com",80))
        #myiP=s.getsockname()[0]
        try:
            myiPeth=getIpAddress('eth0')
        except:
            print('No Ehternet Conection\n')
        
        
        if(StartReport==0):
            body='AgroSense OK. \n'+'Eth ip Address: '+myiPeth+'\n'+'Date:'+time.strftime("%d-%m-%y")+'\n'+'Time: '+time.strftime("%I-%M-%S")
            sendEmail('bersek991@gmail.com','System State',body,'')
            #sendSMS(userPhone,body)
            StartReport=1
            print('Initial info Sended')
    except requests.ConnectionError:
        print("No internet. \n")
        print("-------------------------------")
        InternetFail=InternetFail+1
        if(InternetFail>12):
            ErrorMode=2
            InternetFail=0
            print ("Reboot")
            time.sleep(1)
            os.system("sudo reboot")
        

def ThingSpeak(KEY,d1,d2,d3,d4,d5,d6):
        params = urllib.urlencode( {'field1':d1,'field2':d2,'field3':d3,'field4':d4,'field5':d5,'field6':d6,'api_key':KEY})
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response=conn.getresponse()
            print (response.status, response.reason)
            datai=response.read()
            conn.close()
            print(datai)
        except:
            print ("Conection Failed")

def Advertencia():
    

    if(TQ==0):
        body='El Tanque se esta quedando sin Agua. \n'+'Date:'+time.strftime("%d-%m-%y")+'\n'+'Time: '+time.strftime("%I-%M-%S")
        sendEmail('bersek991@gmail.com','Tanque',body,'')
        time.sleep(5)
            #sendSMS(userPhone,body)
        StartReport=1
        print('Initial info Sended')
    else:    
        print('Tanque con Agua\n')
        
def Automatico():
           global PRE,Action
           filename =open('/home/pi/Desktop/Agrosensor/finalized_model2.sav','rb')
           clf = pickle.load(filename)
           test=np.zeros([1,3])
           #luz
           test[0,0]= FL
# temp 
           test[0,1]= DST
# h
           test[0,2]= HS
	   print(test)
           pred=clf.predict(test)
           Action=pred[0]
           if(Action==0.0):
               arduino.write('5L')# Envia caracter de LOW mantener Bomba Apagada
              
           if(Action==1.0):
               arduino.write('5H')#Envia Caracter de HIGH activacion Bomba
               time.sleep(33)
if __name__ == "__main__":
    createFile()
    while True:
        cont+= 1        
        InternetTest()
        f = open(fileText,"a") #Añadir finchero para añadir al final Archivo del Dia ".txt"
        Tic=time.time()
        Serial=arduino.readline()
        data=Serial.split('\t')
        print(cont)
        if(cont==1):
            ReadData(data)
            Automatico()
            GuardarDatos()
            N=len(data)
            print('N: '+str(N))
        if(cont==2):#Añadir finchero para añadir al final Archivo del Dia ".txt"
            ReadData2(data)
            Advertencia()
            
        try:
                
            if(cont==2):
                cont=0       
                ThingSpeak(THINGSPEAKKEY,FL,DST,HS,TQ,RI,PRE)
        except:
                print('Error uploading Data')
        Toc=time.strftime("%H-%M-%S")
        Toc=Toc.split('-')
        Hour=float(Toc[0])
        Minutes=float(Toc[1])
        if(Hour!=0):
            DataReport=0
        if(Hour==0 and Minutes>0 and Minutes<20 and DataReport==0):
            print('OK')
            f.close()
            if(InternetFail==0):
                sendEmail('bersek991@gmail.com','Report','This is the data report. ',fileText)
                DataReport=1
            createFile()
        Toc=time.time()
        dT=Toc-Tic
##        f.close()        

