#coding: utf-8
import serial,time,requests,os,sys
import datetime
import urllib
import httplib
import smtplib, socket,fcntl, struct
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
##from PIL import Image



arduino = serial.Serial('/dev/ttyACM0', 9600)

urlTest='https://thingspeak.com'
timeoutTest=5
Ruta='/home/pi/Desktop/Agrosensor/Data/'

THINGSPEAKURL  ='https://api.thingspeak.com/channels/487900'
THINGSPEAKKEY  ='13CH4NRJ6PM9A07K'

varNames=['FI', 'FV', 'FL', 'PT', 'DST', 'Res', 'HS', 'TQ', 'RI' ]
FI=''; FV=''; FL=''; PT=''; DST=''; Res=''; HS=''; TQ=''; RI='';

#System
ErrorMode=0; InternetFail=0; DataReport=0; StartReport=0; myiP='0.0.0.0'



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
    global varNames, FI,FV,FL,PT,DST,Res,HS,TQ,RI
    global Luz,Temperatura,Humedad,Tanque,Riego
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
            time.sleep(5)
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
        

def ThingSpeak(KEY,d1,d2,d3,d4,d5):
        params = urllib.urlencode( {'field1':d1,'field2':d2,'field3':d3,'field4':d4,'field5':d5,'api_key':KEY})
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
    
##    var,aux=dataRaw[0].split(':')
##    TQ=float(aux)
##    print(aux)
    if(TQ==0):
        body='El Tanque se esta quedando sin Agua. \n'+'Date:'+time.strftime("%d-%m-%y")+'\n'+'Time: '+time.strftime("%I-%M-%S")
        sendEmail('bersek991@gmail.com','Tanque',body,'')
        time.sleep(5)
            #sendSMS(userPhone,body)
        StartReport=1
        print('Initial info Sended')
    else:    
        print('Tanque con Agua\n')
        
if __name__ == "__main__":
    time.sleep(10)
    createFile()
    InternetTest()
    while True:
        InternetTest()
        f = open(fileText,"a") #opens file with name of "test.txt"
        Tic=time.time()
        Serial=arduino.readline()
        GuardarDatos()
        data=Serial.split('\t')
        N=len(data)
        print('N: '+str(N))
        ReadData(data)
        Advertencia()
        try:
            if(N>2):
                                
                ThingSpeak(THINGSPEAKKEY,FL,DST,HS,TQ,RI)
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




