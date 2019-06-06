#coding: utf-8
import serial,time,requests,os
import datetime
import urllib
import httplib
import smtplib, socket,fcntl, struct
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from flask import Flask, render_template,request
from threading import Timer
import threading, webbrowser

app = Flask(__name__)
app._static_folder = os.path.abspath("static/")
arduino = serial.Serial('/dev/ttyUSB0', 57600)

urlTest='https://thingspeak.com'
timeoutTest=5
Ruta='/home/pi/Desktop/Agrosensor/Data/'
THINGSPEAKURL  ='https://api.thingspeak.com/channels/683862'
THINGSPEAKKEY  ='YIL0J7AXI96PQUQD'
varNames=['FI', 'FV', 'FL', 'PT', 'DST', 'Res', 'HS', 'TQ', 'RI' ]
FI=''; FV=''; FL=''; PT=''; DST=''; Res=''; HS=''; TQ=''; RI='';

#System
ErrorMode=0; InternetFail=0; DataReport=0; StartReport=0; myiP='0.0.0.0'


@app.route("/")
def index():
    def GuardarDatos():
         data=Serial
         data=data.strip()
         print('dato:' + data)
         Fichero = open ('Datos.txt','a')
         Times='\t'+'Date:'+time.strftime("%d-%m-%y")+'\t'+'Time: '+time.strftime("%I-%M-%S")+'\r\n'
         Fichero.write(Times + data)
         Fichero.close()
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
            fromaddr='bersek991@gmail.com'
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
                sendEmail('danilot275@gmail.com','System State',body,'')
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
                sendEmail('danilot275@gmail.com','Tanque',body,'')
                time.sleep(5)
            #sendSMS(userPhone,body)
                StartReport=1
                print('Initial info Sended')
            else:    
                print('Tanque con Agua\n')

    
    while True:    
                
                now= datetime.datetime.now()
                timeString= now.strftime(" a las %H:%M %p del %d-%m-%y")
                response = "Bienvenido a datos Agrosensor "+timeString
                Serial=arduino.readline()
                GuardarDatos()
                InternetTest()
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
            
                templateData = {            
                        'title': 'AGROSENSOR SMART IRRIGATION!',
                        'response':response,
                        'FL' : FL,
                        'DST': DST,
                        'HS' : HS,
                        'TQ' : TQ,
                        'RI' : RI,
                         }
                
                return render_template('index2.html', **templateData) 

@app.route("/<action>")    
def action(action):
        now= datetime.datetime.now()
        timeString= now.strftime("%H:%M %p del %d-%m-%y")
	if action == "on":
		arduino.write('5H')
	if action == "off":
		arduino.write('5L')
	templateData = {
	'MT' : 'MOTOBOMBA ',
        
##        'RI'  : Riego,
	}
	
	return render_template('index2.html', **templateData)
    
                
if __name__ == "__main__":
    app.run(debug=True, port=8000, host='0.0.0.0')
    
