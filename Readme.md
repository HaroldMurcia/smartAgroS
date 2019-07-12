
# Smart AgroSensor for Irrigation Applications

This repository contents a decision support system for intelligent irrigation in crops from a low-cost Agroclimatic station, based on Arduino, Raspberry and Machine Learning. 

* [Watch the video on Youtube](https://www.youtube.com/watch?v=xa9odZJ_yn8&t=1s)

Repository folders:
```
/yourRoot    -path
  |--  Readme.md
  |-- src # source codes
	|-- Arduino     # slave source codes
	|-- Graphics    # Graphics code
    |-- Raspberry   # master source codes
    |-- Training    # Training code
  |-- Data
    |-- ciclo_1.csv # dataBase file for cicle 1
    |-- ciclo_2.csv # dataBase file for cicle 2
    |-- ciclo_3.csv # dataBase file for cicle 3
    |-- Validacion_1.csv # dataBase file validation for cicle 1
    |-- Validacion_2.csv # dataBase file validation for cicle 2
    |-- Validacion_3.csv # dataBase file validation for cicle 3
    |-- Learning_models # trained clasifiers in .sav
```

## Hardware requirements

  - [Agro-sensor system, developed at the University of Ibagué.](https://sites.google.com/a/unibague.edu.co/si2c/species-description)
   - Arduino Mega 2560
  -  Raspberry Pi 3 

## Software requirements
  - Arduino IDE
  - Libraries for arduino: 
    - [TSL2561](https://github.com/adafruit/TSL2561-Arduino-Library)
    - OneWire 
    - Wire
    - [DallasTemperature](https://www.arduinolibraries.info/libraries/dallas-temperature)
  - Raspbian OS
  - Python 2.7 in this case I used [Spyder](https://docs.spyder-ide.org/installation.html#installing-with-anaconda-recommended)
    - [Flask](http://flask.pocoo.org/) 
    - [Sklearn](https://scikit-learn.org/) 
    - [Pandas](https://pandas.pydata.org/)
    - [Serial](https://pyserial.readthedocs.io/en/latest/pyserial.html)
    - [smtplib](https://www.instructables.com/id/Send-Email-Using-Python/)

## How to run
### webControl mode:
- Load on arduino mega 2560 the file `/yourRoot/src/arduino/AgroSensor_Code.ino`
- Run the script: ` /yourRoot/src/raspberry/web.py by using` `sudo python web.py`
 - To access the interface:
   1. It must be connected to the same ethernet network of the raspberry Pi
   2. In your browser enter the IP address of your raspberry Pi, for example:         `http://172.17.100.26:8000` or the default IP of the server `http://0.0.0.0:8000`
   3. In the interface you will find the agroclimatic variables and the ON / OFF buttons to control the irrigation system

### Learning mode:
- If you want to start a data collection of irrigation cycles:
  1. Load on arduino mega 2560 the file `/yourRoot/src/arduino/AgroSensor_Code.ino`
  2. Run the script  `/yourRoot/src/raspberry/Agrosensor.py` by using `sudo python Agrosensor.py`
- If you want to train supervised classifiers with the obtained data:
    1. Open the python editor  and run the script `/yourRoot/src/training/Train.py`
    2. The data file is loaded, for example, `Ciclo1.csv`, this must be in the` /yourRoot/src/data/` folder
    3. Once the code is executed, it will give you  a `file.sav` of the classifier that was trained, this is generated in the folder  `/yourRoot/src/data/learning_models` 
### Automatic mode:
-  Load on Arduino mega 2560 the file `/yourRoot/src/arduino/AgroSensor_Smart.ino`
-  Before running, the code should load the `file.sav` of the classifier
-  Run the script  `/yourRoot/src/raspberry/AgrosensorS.py` by using `sudo python AgrosensorS.py`
## Authors:
**Universidad de Ibagué** - **Ingeniería Electrónica**
**Proyecto de Grado 2019/A**
- [Harold F. Murcia](www.haroldmurcia.com)
- Daniel J. Jimenez 
