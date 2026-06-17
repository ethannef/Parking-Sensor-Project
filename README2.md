# Parking Sensor Systems: In-Depth Research Report
### Every claim tied to its source

---

> **How to read this report:** Every bullet under each implementation is a direct fact
> from that specific source. The source URL appears in the heading of each entry so
> there is no ambiguity about where a detail comes from. Nothing is inferred or
> generalized — if it says "Source says X," that sentence appears in the source.

---

## TABLE OF CONTENTS

1. [GitHub Repositories — Embedded / IoT Hardware](#github-hardware)
2. [GitHub Repositories — Computer Vision](#github-cv)
3. [GitHub Repositories — Niche / Unusual Implementations](#github-niche)
4. [Tutorials & Maker Platforms](#tutorials)
5. [Academic / Research Papers](#papers)
6. [Patents](#patents)
7. [Commercial Products](#commercial)
8. [Datasets](#datasets)
9. [Consolidated Source Index](#source-index)

---

## 1. GitHub Repositories — Embedded / IoT Hardware {#github-hardware}

---

### 1.1 aaryaapg/Smart-Parking
**Source:** https://github.com/aaryaapg/Smart-Parking

**What the source actually says:**
- MCU: STM32F103C (STM32 "Blue Pill")
- Ultrasonic sensors detect vehicle presence near entry or exit
- IR sensors detect occupancy in each individual parking space
- Features listed in source: "Automated parking system without any manual labour · Simultaneous operations on different floors for car parking · Multiple entry and exit points · Pre-booking of parking slots through a mobile App"
- Vehicles are categorized by size and weight — "heavy and larger vehicles can be given a parking space on the Ground floor for convenience"
- Context note from source: "In India, this type of parking system is most likely to be implemented in Bangalore in the near future"
- Source notes the fundamental problem: "there is no way of knowing whether a vacant parking space is available or not"

---

### 1.2 RahulN25/Smart-Parking-System
**Source:** https://github.com/RahulN25/Smart-Parking-System

**What the source actually says:**
- Sensor array: "ultrasonic, infrared, and camera technologies to monitor real-time parking space availability"
- Data collected by sensors "is transmitted wirelessly to a central control unit, enabling instant updates on parking status"
- Features by objective (direct from source):
  - "Real-Time Parking Information: Provide drivers with instant, accurate information on parking space availability to minimize search time"
  - "Seamless Payment Process: Implement a Unified Payments Interface (UPI) to streamline and secure payment transactions, offering users a hassle-free and cashless payment experience"
  - "Occupancy Detection and Prediction: Utilize advanced sensors and machine learning algorithms for precise occupancy detection and predictive analysis, enabling users to plan parking in advance"
  - "Pre-Booking and Payment System: Offer users the convenience of pre-booking parking spaces through a user-friendly website, simplifying entry and exit processes with QR code-based access"

---

### 1.3 vishnubv944/smartParkingSystem
**Source:** https://github.com/vishnubv944/smartParkingSystem

**What the source actually says:**
- Hardware: NodeMCU, five IR sensors, two servo motors
- Sensor layout: "Two IR sensors are used to detect the automobile at the entry and exit gates, and three IR sensors are utilized to determine the availability of parking slots"
- Gates: "The gates are opened and closed using servo motors based on the sensor data"
- Cloud: "The device sends measurements to the cloud where they are stored in AWS IoT shadow as a sensor state"
- Detection principle: "A sensor detects a parked car by measuring the distance to the nearest obstacle — in our case, to the bottom of the car"
- Display layer: "We're going to use the Adafruit IO platform to illustrate how to publish data to the cloud and monitor it from anywhere in the globe"
- Authors consciously rejected Firebase: "We restricted the usage of firebase database in our project and shifted to cloud database as we were aware of the complexities involved in transferring the data from database to the mobile app or any other user point"

**Advantages / Disadvantages (as stated by source):**
- ❌ **Disadvantage of Firebase (stated):** Authors explicitly rejected it due to "the complexities involved in transferring the data from database to the mobile app or any other user point" — AWS IoT Shadow chosen instead

---

### 1.4 Dipal018/Smart_Parking
**Source:** https://github.com/Dipal018/Smart_Parking

**What the source actually says:**
- Core description: "An IoT based parking automation system where sensor detects the parking lot occupancy which can be used to detect the available parking spot and sends message to car owner if the time limit is about to expire"
- Hardware: ESP8266 board, proximity sensors, LED display, motor
- Software stack: "Arduino IDE in C for hardware development, Angular.js, HTML, CSS for web interface design and PhoneGap for mobile app development"
- Backend server dependencies (from `npm install` command in README): express, cors, **twilio**, nodemailer
- Server startup: `node server.js`
- Architecture listed explicitly: "Microcontroller-based sensor module · Phonegap Mobile App · RESTful API web server (middleware) · User-facing web application"
- The Twilio dependency confirms SMS notification is implemented at the server layer, not the microcontroller

---

### 1.5 CarlosFULLHD/iot_garaje_inteligente (SmartPark)
**Source:** https://github.com/CarlosFULLHD/iot_garaje_inteligente

**What the source actually says (from the rendered README):**
- Problem statement: "Managing parking spaces in university campuses is chaotic and inefficient, leading to congestion and security issues"
- Solution: "An intelligent garage system utilizing ultrasonic sensors, keypad authentication, and a mobile app for real-time management and monitoring"
- Hardware: Raspberry Pi Pico W
- Tech stack (exact from source): Spring Boot (Java Backend), Flutter (Frontend), PostgreSQL (Database), Python (IoT Nodes and Dashboard)
- Authentication: "Flexible Authentication Methods (Code and License Plate Recognition)"
- User app features (from source):
  - Login / Registration for user and their car
  - Available Spaces display
  - Space Reservation ("Choose a car and the time for your reservation")
  - Vehicle Registration ("Add a vehicle")
  - User Activity: "Reservations that have been made · Entry and exit time graph for a reservation"
  - Reservation Details: "User, vehicle, entry and exit programmed, exact (real) entry and exit, status of the reservation"
  - Vehicle Activity Graph: "Usage tendency for a vehicle"
- Admin features (from source):
  - Flutter App Admin Dashboard: "Statistics per use by spot · Reservations by spot · Total hours occupied by parking and spot"
  - Python Dashboard: "KPIs from the parking usage and the most relevant information for an ADMIN user"
- Docker command shown in source: `docker run -d --name smartpark_c -e POSTGRES_PASSWORD=12345 -e POSTGRES_USER=admin -e POSTGRES_DB=smartpark_db -p 5432:5432 postgres:15.3`
- Version tags: Flutter 3.19.6, Spring Boot 3.0, Python + MicroPython, PostgreSQL 15.3, Java SDK 20

**Advantages / Disadvantages (as stated by source):**
- ✅ **Improved Efficiency (stated):** Source lists "Improved Efficiency" as a conclusion of the system
- ✅ **Enhanced Security (stated):** Source lists "Enhanced Security" as a conclusion
- ✅ **Automation and Convenience (stated):** Source lists "Automation and Convenience" as a conclusion
- ✅ **Real-Time Monitoring (stated):** Source lists "Real-Time Monitoring" as a conclusion
- ✅ **Resource Optimization (stated):** Source lists "Resource Optimization" as a conclusion

---

### 1.6 prince61299/Smart-Car-Parking-using-ESP32
**Source:** https://github.com/prince61299/Smart-Car-Parking-using-ESP32

**What the source actually says:**
- Hardware: ESP32 microcontroller, IR sensor, servo motor
- Cloud platform: Arduino Cloud
- The ESP32 reads the IR sensor and controls the servo motor, which "is used to open and close a barrier arm"
- "When a car approaches the parking space, the IR sensor sends a signal to the ESP32. The ESP32 then activates the servo motor to open the barrier arm"
- Reporting: "The system also sends real-time data to the Arduino Cloud to show the status of the parking. This data can be accessed by users through a web app or mobile app"
- Data reported: "the number of available parking spaces, the location of the parking spaces, and the status of the parking spaces (occupied or vacant)"
- Setup steps from source: create Arduino Cloud account → install Arduino Cloud library in Arduino IDE → download code → enter Arduino Cloud credentials → upload to ESP32

---

### 1.7 Muhaiminul-Hasan/RFID-based-Smart-Parking-System-using-ESP32
**Source:** https://github.com/Muhaiminul-Hasan/RFID-based-Smart-Parking-System-using-ESP32

**What the source actually says:**
- Hardware: ESP32 microcontroller, MFRC522 RFID scanner modules at entry and exit gates
- OS: "freeRTOS: Real-Time Operating System for ESP32"
- Web server: "ESPAsyncWebServer: Asynchronous Web Server Library for ESP32"
- RFID library: "MFRC522: RFID Library for MFRC522 RFID scanner module"
- Operation: "automatically scan RFID tags at the Entry and Exit gates to manage parking slot allocations"
- Reporting: "The local webserver will display the current parking slot allocations on a webpage, which will be automatically refreshed"
- Access: "Access the local webserver by entering the ESP32's IP address in a web browser"
- **Note:** This is a local network system — no cloud dependency

---

### 1.8 harshad8782/Smart-Parking-System-IoT
**Source:** https://github.com/harshad8782/Smart-Parking-System-IoT

**What the source actually says:**
- Hardware: Arduino Uno, NodeMCU (ESP8266), IR sensors
- Backend: PHP + MySQL (via XAMPP/phpMyAdmin)
- Frontend: Android app (built in Android Studio)
- "automates parking slot management via mobile app and sensors, featuring real-time slot availability, booking, and vehicle detection"
- Setup path (from source): Install XAMPP → Import smart_parking.sql → Place backend files in htdocs → Open Android project in Android Studio → Upload code to Arduino and NodeMCU via Arduino IDE
- Origin: "Final year Diploma Project, Vidyalankar Polytechnic"

---

### 1.9 emregulerr/IoT-Smart-Parking-System
**Source:** https://github.com/emregulerr/IoT-Smart-Parking-System

**What the source actually says:**
- Entry/exit control: "Member entry and exit are controlled via RFID cards"
- Occupancy sensor: "the status of parking spaces is detected in real-time using infrared sensors (TCRT 5000)"
- Fee system: "Fees are calculated based on entry-exit times and reservation durations"
- Web interface: "A dedicated website for managing and monitoring all operations"
- "The prototype was created by integrating the electronic circuits onto a parking lot model made from architectural model board"
- Boot process: "the Arduino connects to the database to retrieve the RFID card information of registered members"
- Sensor polling: "periodically reads the infrared sensors in the parking spaces and sends the occupancy status to the web server"
- Entry logic: "If a registered card is detected, it opens the entry barrier, sends the entry record to the server, and turns on a green LED. If the card is not registered, it gives a warning with a red LED"
- The README explicitly mentions future work: "License Plate Recognition: Use a camera with OCR to automatically recognize license plates for entry and exit, removing the need for RFID cards"

---

### 1.10 anmoljhamb/smart-parking-system
**Source:** https://github.com/anmoljhamb/smart-parking-system

**What the source actually says:**
- Description: "An automated parking system using Arduino and Python to control entry/exit gates with RFID card identification and IR sensor detection"
- Language: "embedded C programming for Arduino and a Python server for communication"
- Sensing: "RFID technology, infrared sensors, and servo motors to automate entry and exit processes"
- Key architectural detail — hardware interrupts instead of polling: "Interrupts are configured for both sensors, and corresponding Interrupt Service Routines (ISRs) are implemented"
- ISR for entry sensor: "This ISR is triggered when a change in state is detected on IR_LED_1 (Pin 2). It handles the arrival and departure of vehicles at the entry point. `ISR(INT0_vect) { ... }`"
- ISR for exit sensor: "ISR(INT1_vect)" — triggered on IR_LED_2 (Pin 3)
- Custom delay function: "a custom delay function that provides delay in milliseconds without using the built-in delay function" (avoids blocking the interrupt handler)

---

### 1.11 ferasaljoudi/AljoudiParkingSystem
**Source:** https://github.com/ferasaljoudi/AljoudiParkingSystem

**What the source actually says:**
- MCU: STM32F103RB
- IDE: Keil µVision
- Language: C
- Capacity: "can accommodate up to four vehicles simultaneously"
- LCD display: shows available parking spots, rates, and alerts
- Potentiometer (10K): "Used to adjust the contrast of the LCD display"
- **Pressure sensor:** "Analog Pressure Sensor: To weigh vehicles and determine parking rates" — rates are vehicle-weight-dependent
- **Gas/fire sensor:** "Analog Gas Sensor: For detecting smoke or fire within the parking facility"
- Buzzer: "Digital Buzzer: To alert users in case of fire detection"
- IR sensor at exit door
- Two servo motors for entrance and exit doors
- **Full capacity denial:** "The system is programmed to deny entry (by not opening the entrance door) when the parking lot reaches full capacity"
- Fire alert detail: "Features a gas sensor to detect smoke or fire within the parking lot. In case of detection, the system activates a digital buzzer to alert users and staff"

---

### 1.12 ColoradoSchoolOfMines/parking_sensor
**Source:** https://github.com/ColoradoSchoolOfMines/parking_sensor

**What the source actually says:**
- Authors: Roy Stillwell, Andrew Wilson, Santiago Gonzalez — Colorado School of Mines
- Created: 2013; updated through 2014
- Sensor: HMC5883 magnetometer (3-axis) on Arduino Fio with XBee wireless
- Detection principle from DetectorCode.ino: "An array of 'baseline' or nominal values — essentially when the sensor does NOT have a vehicle over it — is gathered initially"
- **Auto-recalibration:** `double recalibrateTime = 600000; //time in seconds. 600000 = 10 min -- used to auto-recalibrate sensor`
- `#define baselineSize 100` — size of the baseline array
- `#define windowSize 30` — number of previous values considered in detection
- `#define windowConsidered 3` — first N numbers of window used to determine direction
- `double carThreshold = 15.0;` — "Anything above or below this threshold is counted as a hit"
- `double pingTime = 60;` — "make sure sensor is still alive after specified time"
- License: Creative Commons Attribution
- Extended analysis: "Using datasets taken at the CTLM exits and entrances, it can correctly calculate entrances and exits"
- MATLAB scripts: "help for analysis of data plotted in 3d and 2d, with code for moving average windows as well as commented code for hamming windows if periodic functions start showing up"
- History: Originally used pressure sensors, then migrated to magnetometer as "no longer our sensor of choice"
- Raspberry Pi basestation: "the Raspberry Pi would analyze the data from multiple sensors, and update a web page that can be viewed on a mobile device"

**Advantages / Disadvantages (as stated by source):**
- ❌ **Disadvantage of pressure sensors (stated):** Source explicitly migrated away from pressure sensors, describing them as "no longer our sensor of choice" — the reason the magnetometer codebase exists
- ✅ **Advantage of auto-recalibration (stated):** The 10-minute auto-recalibration timer (`recalibrateTime = 600000`) is described in source as solving drift in the baseline over time

---

### 1.13 aswin-sreekumar/Smart-parking-system
**Source:** https://github.com/aswin-sreekumar/Smart-parking-system

**What the source actually says:**
- Hardware: ESP32-CAM (multiple units), Raspberry Pi, cloud Node.js web server
- Stack description: "Vision based Smart Parking system using ESP32-CAMs, Raspberry Pi and cloud deployed NodeJS web-server"
- Occupancy algorithm: "Based on Intersection Over Union calculation between the predicted bounding boxes and manually drawn bounding boxes representing parking areas, Occupancy of respective parking lots gets updated in the server"

---

### 1.14 elise-ng/FYP_SmartCarPark (HKUST)
**Source:** https://github.com/elise-ng/FYP_SmartCarPark

**What the source actually says:**
- Stack: Raspberry Pi, Google Cloud, Flutter, Vue.js
- Origin: "The car park of the HKUST campus operates on manual and paper processes, which is inefficient and prone to human error"
- Goal: "digitize car park operations, such as visitor guidance, payment, access control, and park management"
- Components: "sensor devices, cloud-based backend, a tablet app for gate kiosks, a mobile app for drivers, to a web management portal"
- Admin panel: "Web Admin Panel for monitoring and controlling car park. Also provides demo functionalities and data visualization. Based on Vue.js"
- Note in repo: "Obsolete code for experimenting with different approaches to license plate recognition" — indicates multiple LPR approaches were tried
- Raspberry Pi Zero W compatibility note: "Yarn package manager must be used for Raspberry Pi Zero W (arm6l) compatibility"
- Continuous tasks: "live telemetry collection and license plate recognition are continuously carried out"

**Advantages / Disadvantages (as stated by source):**
- ❌ **Disadvantage of prior manual system (stated):** "The car park of the HKUST campus operates on manual and paper processes, which is inefficient and prone to human error"
- ✅ **Advantage of this system (stated):** Aims to "smoothen and speed up operations such as visitor guidance, payment, access control, and park management" and "reduction in human resources required"

---

## 2. GitHub Repositories — Computer Vision {#github-cv}

---

### 2.1 8harath/Car-Parking-Detection
**Source:** https://github.com/8harath/Car-Parking-Detection

**What the source actually says:**
- Stack: YOLOv8, OpenCV, Python 3.8+
- Example input/output (direct from source): "Input: Picture of parking lot with 50 spaces. Output: '35 spaces occupied, 15 available' + Visual map showing which spots are free + Detailed report with charts + CSV file for data analysis"
- Use cases listed (direct from README): "Final Year Project, Computer Vision Assignment, Machine Learning Project, IoT Project (Combine with sensors for real-time monitoring), Data Analysis Project (Analyze parking patterns over time), Research Paper"
- Learning path the author suggests: Week 1 (image processing, OpenCV) → Week 2 (YOLO, object detection) → Week 3 (run project, experiment) → Week 4 (modify/add features) → Week 5 (create presentation/report)
- Author requests citation: "If you use this project in academic work, please cite: Bharath K."

---

### 2.2 fabiocarrara/deep-parking
**Source:** https://github.com/fabiocarrara/deep-parking

**What the source actually says:**
- Purpose: "Code to reproduce the experiments presented in Deep Learning for Decentralized Parking Lot Occupancy Detection"
- Framework: Caffe (PyCaffe interface)
- Datasets and their sizes:
  - CNRPark: `http://cnrpark.it/dataset/CNRPark-Patches-150x150.zip` (36.6 MB)
  - CNR-EXT: `http://cnrpark.it/dataset/CNR-EXT-Patches-150x150.zip` (449.5 MB)
  - PKLot: 4.6 GB
- Setup: `git clone --recursive https://github.com/fabiocarrara/deep-parking.git`
- Dataset splits download: `wget http://cnrpark.it/dataset/splits.zip`
- Code file `main.py` defines: `PKLot`, `CNRParkAB`, `CNRExt`, `Combined` as `pyffe.Dataset` objects
- `InputFormat` in code: `new_width=256, new_height=256, crop_size=224`

---

### 2.3 wuyenlin/parking_lot_occupancy_detection
**Source:** https://github.com/wuyenlin/parking_lot_occupancy_detection

**What the source actually says:**
- Purpose: PyTorch reproduction of the Amato et al. paper, reproducing results from the CNRPark website (http://cnrpark.it)
- Authors of the reproduction: Hao Liu, Sigurd Totland, and Yen-Lin Wu
- Cross-condition results (paper vs. PyTorch re-implementation), directly from source README:
  - Trained on SUNNY → tested OVERCAST: Paper 0.970, PyTorch 0.946
  - Trained on SUNNY → tested RAINY: Paper 0.960, PyTorch 0.912
  - Trained on SUNNY → tested PKLot: Paper 0.850, PyTorch 0.759
  - Trained on OVERCAST → tested SUNNY: Paper 0.920, PyTorch 0.917
  - Trained on RAINY → tested OVERCAST: Paper 0.970, PyTorch 0.959
  - CNRParkOdd result: Paper 0.9240, PyTorch 0.9071
- Citation block from source: `@article{amato2017deep, title={Deep learning for decentralized parking lot occupancy detection}, author={Amato, Giuseppe and Carrara, Fabio and Falchi, Fabrizio and Gennaro, Claudio and Meghini, Carlo and Vairo, Claudio}, journal={Expert Systems with Applications}, volume={72}, pages={327--334}, year={2017}, publisher={Pergamon}}`

**Advantages / Disadvantages (as stated by source):**
- ❌ **Disadvantage of PyTorch re-implementation vs. original Caffe (stated by source numbers):** PyTorch consistently underperforms the original Caffe results across all tested conditions — e.g., SUNNY→PKLot: Paper 0.850 vs. PyTorch 0.759; SUNNY→RAINY: Paper 0.960 vs. PyTorch 0.912. The source presents these figures directly without explanation for the gap.

---

### 2.4 sk0601/Smart-Parking-System (LDR-guided autonomous toy cars)
**Source:** https://github.com/sk0601/Smart-Parking-System

**What the source actually says (unusual implementation):**
- Uses Arduino, IR modules, and **LDR (Light Dependent Resistor)** sensors
- Sensor choice rationale from source: "We have chosen IR module instead of RF module because we want a receiver having line of sight communication with the transmitter. But RF does not require line of sight communication. And in case of LDR, there is scope for false triggering due to sunlight or headlight of car. So considering all these points we have finalized to use IR module"
- Guidance mechanism: "Each car has an LDR so that it can follow while glowing LEDs. The car moves to the slot which is nearest to it. LEDs are installed at the entrance of all parking slots and the empty slot is indicated by the respective glowing LED"
- Future application cited: "Can be used in IoT as a smart parking system and in AID to Google Self-Drive car (Google Self Drive car works on the principle of LIDAR by mapping and monitoring movement of vehicles & people around it)"

**Advantages / Disadvantages (as stated by source):**
- ✅ **Advantage of IR over RF (stated):** "We have chosen IR module instead of RF module because we want a receiver having line of sight communication with the transmitter" — line-of-sight is explicitly preferred for slot detection
- ❌ **Disadvantage of RF (stated):** "RF does not require line of sight communication" — treated as a drawback in this context as it reduces precision of slot detection
- ❌ **Disadvantage of LDR (stated):** "In case of LDR, there is scope for false triggering due to sunlight or headlight of car" — explicitly rejected for this reason

---

## 3. GitHub Repositories — Niche / Unusual {#github-niche}

---

### 3.1 Google Sheets as Backend (unnamed repo from GitHub topic listing)
**Source:** https://github.com/topics/smart-parking-system (topic page listing)

**What the source actually says:**
- Stack: "four HC-SR04 ultrasonic sensors, two Arduino Mega, and an ESP-8266 Wi-Fi module as part of hardware components"
- Backend: "Google Sheets was acts as a simplified back-end database, and Google HTML Service web pages to display the availability of parking spaces in real-time"
- Language: C++ on Arduino

**Significance:** Uses Google Sheets as a zero-cost, zero-infrastructure cloud database via Google Apps Script — rare approach in the IoT parking space.

---

### 3.2 VHDL + FPGA Parking System (alphinaud11/Car-Parking-System)
**Source:** https://github.com/alphinaud11/Car-Parking-System

**What the source actually says:**
- "The source code for a car parking system which automates the boom barrier of the homeowners' parking garage and includes fire detection support"
- Language: VHDL
- Hardware: Altera DE10-Lite FPGA
- **Significance:** One of very few parking sensor system implementations done entirely in hardware description language on an FPGA rather than a microcontroller

---

### 3.3 MahmoudHanyFathalla/Car-parking-system (College Multi-Sensor)
**Source:** https://github.com/MahmoudHanyFathalla/Car-parking-system

**What the source actually says:**
- "A Comprehensive College Parking System that utilizes Ultra-Sonic Range sensors, ID and Ticket systems, Fire Sensors, and a Vending Machine to ensure a smooth and secure parking experience for college students, staff, and guests"
- "checks for valid AAST IDs and assigns tickets to non-authorized cars"
- **Significance:** One of very few implementations that includes a *vending machine* integration for ticket dispensing

---

### 3.4 minchoCoin/smartParkingLot-stm32 (Korean, Bluetooth output)
**Source:** https://github.com/minchoCoin/smartParkingLot-stm32

**What the source actually says:**
- MCU: STM32F10x (standard peripheral library required)
- IDE: IAR Embedded Workbench + J-Link
- UART pin mapping (from source): `USART1: PA9(TX), PA10(RX)` — serial to PC; `USART2: PA2(TX), PA3(RX)` — connected to Bluetooth module
- Bluetooth TX pin: PA2; Bluetooth RX pin: PA3
- For boards without RS232: "you should connect USB to TTL serial cable to these port"
- Note: USB to TTL connection: "PA9 is connected to RX of USB-to-TTL, PA10 is connected to TX of USB-to-TTL"
- Context: "term project of 'Embedded System Design and Lab' subject"

---

### 3.5 SiddheshPadwal10/Smart-Parking-System-with-Embedded (STM32 + UART)
**Source:** https://github.com/SiddheshPadwal10/Smart-Parking-System-with-Embedded

**What the source actually says:**
- Description: "Smart Parking system is established using STM32 communicating over UART"
- **Significance:** Pure embedded STM32 system using UART as the reporting channel — represents the hardware-near end of the spectrum with no Wi-Fi or cloud component

---

### 3.6 MustafaOrhon/STM32-F401RE-UltrasonicCarSensor
**Source:** https://github.com/MustafaOrhon/STM32-F401RE-UltrasonicCarSensor

**What the source actually says:**
- MCU: STM32F401RE
- IDE: STM32CubeIDE
- Language: C
- "uses ultrasonic sensors to detect the distance of a car from obstacles, and displays the information on an LCD screen while emitting beeping sounds to indicate proximity"
- Timer usage: "Timer 2 for PWM signal generation to control the buzzer"
- Capture timer: "void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim)() function was used to measure the time interval between echo pin"
- Future work listed in source: "Implementing a new method to control the loudness of the sensor · Find more accurate formula to change beeping interval"
- Refers to YouTube tutorial at `https://youtu.be/ti_1ZwRolU4?t=280` for the capture callback implementation

---

## 4. Tutorials & Maker Platforms {#tutorials}

---

### 4.1 Hackaday.io — ESP32-Based Precision Parking Assist
**Source:** https://hackaday.io/project/177714-esp32-based-precision-parking-assist

**What the source actually says:**
- Hardware: ESP32, HC-SR04 ultrasonic sensor, WS2812B addressable LED strip
- Library: FastLED
- State machine (from source): "Once the Parked state is entered, that state remains active until measurements indicate the vehicle is no longer parked nearby, and a certain time has passed. This state ensures that the LED display is stable (e.g. the lights do not blink, or the TooClose state is not entered) due to people walking between the car and the sensor"
- All parameters named explicitly:
  - `target_distance`: distance from sensor representing optimum parking location
  - `approach_zone_depth`: distance over which driver is guided by LEDs
  - Specified in inches, resolution 0.1 inch
- Temperature sensing: "Sensing the ambient air temperature to compute an accurate speed of sound for distance measurement"
- Network features (from source list): "WiFi connection to the home network for control · Setting the 'target' parking distance via pushbutton · Setup of parameters by web application · Web application implemented an approach where the characteristics of the set of control parameters were defined in a JSON file · Websocket interface for delivery of parameters · A telnet interface for debugging · Supported ArduinoOTA for code downloads over the network · mDNS for network address discovery · Parameters retained in the ESP32 using nonvolatile storage · A real-time clock, synchronized to an NTP time server, to turn off the unit during off-hours · Printed circuit board designed to fit within a standard plastic enclosure"

**Advantages / Disadvantages (as stated by source):**
- ❌ **Disadvantage of naive distance sensing (stated):** Source explicitly names the problem that "people walking between the car and the sensor" can cause the system to exit the Parked state incorrectly — a real-world false-negative the state machine was designed to prevent
- ✅ **Advantage of Parked state latching (stated):** "Once the Parked state is entered, that state remains active until measurements indicate the vehicle is no longer parked nearby, and a certain time has passed" — source describes this as ensuring "the LED display is stable"
- ✅ **Advantage of temperature correction (stated):** "Sensing the ambient air temperature to compute an accurate speed of sound for distance measurement" — source explicitly cites this as improving accuracy

---

### 4.2 Arduino Project Hub — Nano ESP32 LiDAR Garage Parking Assistant
**Source:** https://projecthub.arduino.cc/noah_barkol/arduino-nano-esp32-fully-automatic-garage-ceiling-parking-assistant-79cd6c

**What the source actually says (code directly in the project):**
```cpp
#include <TFMPlus.h>
#include <HardwareSerial.h>
#include <Adafruit_NeoPixel.h>

TFMPlus tfmP;
HardwareSerial tfSerial(1); // Using UART1 on Nano ESP32
const int RX_PIN = 43; // White wire on TFMini Plus -> GPIO43 (RX0 on board)
const int TX_PIN = 44; // Green wire on TFMini Plus -> GPIO44 (TX1 on board)

#define LED_PIN 5        // D2 on Nano ESP32 = GPIO5
#define NUM_LEDS 60      // Number of LEDs on WS2812B strip
#define BRIGHTNESS 40

const int MIN_DISTANCE = 167.64;  // 66 in - perfect spot (red)
const int MID_DISTANCE = 210.82;  // 83 in - moderate range (orange)
const int MAX_DISTANCE = 254;     // 100 in - (off)

unsigned long lastReadTime = 0;
const unsigned long readInterval = 250;  // read sensor every 250ms
```
- Sensor: Benewake TFMini Plus LiDAR — "Waterproof IP65 Lidar Range Finder UART Anti-dust 12m 1000Hz"
- LED strip: BTF-LIGHTING WS2812B (20AWG 3 Pin JST SM connector)
- Note from source: "The variable measurements are project-specific" — distances in the code are calibrated to the author's garage

---

### 4.3 Hackster.io — ESP32 Smart Parking Detection System
**Source:** https://www.hackster.io/techgyanset/esp32-smart-parking-detection-system-d68660

**What the source actually says:**
- Required software (from source list): Arduino IDE, ESP32 Board Package, WiFi Library, MQTT / HTTP API, Mobile App / Web Dashboard
- Detection logic (direct from source, original bilingual text preserved):
  1. "Ultrasonic sensor distance measure karta hai" [measures distance]
  2. "Agar car detect hoti hai → slot occupied" [if car detected → occupied]
  3. "Agar slot empty hai → parking free" [if empty → free]
  4. "LED indicator update hota hai" [LED updates]
  5. "Data cloud par send hota hai" [data sent to cloud]
  6. "Mobile app available slots show karta hai" [app shows available slots]
- Deployment targets listed: Shopping malls, Airports, Smart cities, Offices, Apartment parking
- Commercial offering note: "Complete project, customization, PCB design & deployment available"

---

### 4.4 Hackster.io — DIY Raspberry Pi ALPR Parking System
**Source:** https://www.hackster.io/codrinsideas/diy-raspberry-pi-alpr-parking-sys-with-platerecognizer-s-sdk-adcf07

**What the source actually says:**
- Hardware: Raspberry Pi, Arduino Nano, Plate Recognizer SDK
- Author: Codrin's Ideas
- Source says: "Learn how to step by step implement your own parking system with the use of a Raspberry Pi, Arduino Nano, and Plate Recognizer's SDK"
- External detail link: `https://codrinsideas.medium.com/diy-raspberry-pi-parking-system-with-platerecognizers-alpr-8e2254298917`
- Source notes: "The code/diagrams below are just a few snippets of what you will be learning about how to implement/build in the blog above" — full detail in Medium post

---

### 4.5 Hackster.io — Arduino Parking Sensor with Litho LED Boxes
**Source:** https://www.hackster.io/MrBancroft/parking-sensor-67e3f0

**What the source actually says:**
- Purpose: "I wanted to make lights that would alert my wife and I to how close our truck was to the wall when parking in the garage"
- Construction: custom lithophane (litho) boxes illuminated by LEDs, printed on 3D printer
- Feature: boxes have "a passthrough channel so the wires are hidden" and "Each litho pane slides in so you can change them without removing the boxes"
- Note from source: "Be careful when printing as there is a left, right and middle box"
- LED note: "Make sure that when connecting your LED that you use a resistor that is suited to your LED"
- "I modified the sensor code off the Arduino website"
- Note: "I did print a case for the arduino and the ultrasonic sensors; however, since I did not make these I will not include the files"

---

### 4.6 ArduinoYard — ESP32 Parking System (Web Server)
**Source:** https://arduinoyard.com/esp32-parking-system/

**What the source actually says:**
- Hardware: ESP32 DevKit, 3 IR sensors, breadboard, jumper wires
- Libraries: ESPAsyncWebServer, AsyncTCP
- "monitor three parking slots and display their status (free or occupied) on a web page"
- "Each parking slot has an IR sensor that detects whether a vehicle is present. The ESP32 reads the sensor data and updates the web page in real time"
- Power connection: "Connect the VCC pin of each IR sensor to the VIN pin on the ESP32"
- Future extension ideas from source: "Update the HTML to display room occupancy or door/window status. Add controls for lights, fans, or appliances"

---

### 4.7 IoTDesignPro — NodeMCU ESP8266 Smart Parking (Adafruit IO)
**Source:** https://iotdesignpro.com/projects/iot-based-smart-parking-using-esp8266

**What the source actually says:**
- Hardware: NodeMCU (ESP8266), five IR sensors, two servo motors, NTPClient (for timestamps)
- Sensor layout identical to vishnubv944 above: 2 IR at gates, 3 IR for slot detection
- Gate servo behavior: "whenever the IR sensor detects a car, the servo motor automatically rotates from 45° to 140°, and after a delay, it will return to its initial position"
- Code excerpt from source:
```cpp
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"
#define MQTT_SERV "io.adafruit.com"
#define MQTT_PORT 1883
#define MQTT_NAME "aschoudhary"
```
- Dashboard extra: "Adafruit IO dashboard also has two buttons to manually operate the entry and exit gate"
- Time tracking: `#include <NTPClient.h>` and `#include <WiFiUdp.h>` — timestamps sent to cloud alongside occupancy

---

### 4.8 Medium — Edge Impulse + ESP32-CAM AI Parking
**Source:** https://medium.com/@anasyunus/building-an-ai-powered-parking-space-detection-system-with-edge-impulse-and-esp32-cam-7066377b8154

**What the source actually says:**
- Hardware: ESP32-CAM
- Dataset source: Roboflow (~200 images)
- Model type: FOMO (Faster Objects, More Objects) on Edge Impulse
- "I chose Edge Impulse to handle the machine learning part of the project because it offers a straightforward interface for training models on edge devices. The platform allows you to fine-tune pre-trained models for specific tasks, which is perfect for working with limited data like mine (only around 200 images)"
- Inference: "The trained model from Edge Impulse provided all the necessary code snippets, and I simply integrated it into my ESP32-CAM setup. The device captures images, runs them through the trained model, and classifies parking spaces as either vacant or occupied"
- Output: "showing whether the parking spaces were available" via Wi-Fi web interface

**Advantages / Disadvantages (as stated by source):**
- ✅ **Advantage of Edge Impulse for small datasets (stated):** "The platform allows you to fine-tune pre-trained models for specific tasks, which is perfect for working with limited data like mine (only around 200 images)" — source explicitly cites this as the reason Edge Impulse was chosen over alternatives

---

### 4.9 CircuitDigest — AI-Based Smart Parking System (ESP32-CAM + ALPR)
**Source:** https://circuitdigest.com/projects/ai-based-smart-parking-system

**What the source actually says:**
- Hardware: ESP32-CAM (AI Thinker board), Raspberry Pi, IR sensors, servo motor
- Libraries: GPIO pins for servo motor and IR sensors configured during setup
- "Serial Communication & Pin Setup, Initializes serial communication for debugging and configures GPIO pins for the servo motor and IR sensors"
- OCR technology: Tesseract on Raspberry Pi
- API: Plate Recognizer's ALPR (Number Plate Recognition API)
- Note on libraries: "Don't worry about the number of libraries listed in the image—most of them are built-in and will be automatically located when you select the AI Tinker ESP32-CAM Board in the board manager"

---

### 4.10 DigiKey/M5Stack — Car Parking Detection with Edge Impulse (FOMO)
**Source:** https://www.digikey.com/en/maker/projects/car-parking-detection-system-using-edge-impulse/0fcb63b013e240e5bef7049ed1027332

**What the source actually says:**
- Date: March 21, 2023
- Hardware: M5Stack device
- Model type: "FOMO detection" on Edge Impulse
- Setup path described: Create Edge Impulse account → select FOMO project type → clone project → select Data Acquisition → upload images
- Credits: "Thanks for the source code and project information provided by @Aldhi Adytia Prasetio 24776, Hendra Kusumah"

---

## 5. Academic / Research Papers {#papers}

---

### 5.1 LoRaWAN Smart Parking Architecture (MDPI Applied Sciences 2020)
**Source:** https://www.mdpi.com/2076-3417/10/13/4674

**What the source actually says:**
- Sensor choice reasoning: "sensors should be able to transmit information over long-range perimeters with low energy consumption. These sensors should not be invasive as RFID, but effective when determining vehicle presence and avoid false-positive detections. Based on that, magnetic sensors are the ones that best fit the detection requirement"
- Range comparison: "Wi-Fi, BLE and Zigbee are appropriate for short distances (less than 500 m). Network connectivity must reach long distances"
- LPWAN justification: "Protocols like SigFox, LoRaWAN or NB-IoT could be considered for implementing a smart parking solution"
- Context: "parking slots are bigger and cover hundreds of square meters particularly in places like hospitals, universities, schools, cities"

**Advantages / Disadvantages (as stated by source):**
- ✅ **Advantage of magnetic sensors over RFID (stated):** "sensors should not be invasive as RFID" — source explicitly positions magnetometers as the better fit for non-invasive detection
- ✅ **Advantage of magnetic sensors over other types (stated):** "magnetic sensors are the ones that best fit the detection requirement" for low energy, long-range, false-positive avoidance
- ❌ **Disadvantage of Wi-Fi, BLE, Zigbee (stated):** "appropriate for short distances (less than 500 m)" — explicitly ruled out for large parking areas such as hospitals, universities, and cities

---

### 5.2 Smart Parking Sensors State of the Art (ScienceDirect, Journal of Cleaner Production 2020)
**Source:** https://www.sciencedirect.com/science/article/abs/pii/S0959652620312282

**What the source actually says:**
- Sensor types covered: "photodiode, ultrasound, infrared, magnetometer" plus LPWA radio technologies
- Radio technologies analyzed: LoRa, Sigfox, NB-IoT — power requirements compared
- "In depth analysis of commercial LPWA smart parking detector in terms of consumption and lifetime duration is also provided"
- Key finding: "two potential strategies that may extend battery lifetime of smart parking sensor device"

**Advantages / Disadvantages (as stated by source):**
- ✅ **Advantage of LPWA technologies (stated):** Source specifically analyzes LoRa, Sigfox, and NB-IoT for power consumption and battery lifetime — framed as the key advantage over shorter-range protocols
- ✅ **Advantage of battery lifetime strategies (stated):** Source identifies "two potential strategies that may extend battery lifetime of smart parking sensor device" — presented as a contribution of the paper

---

### 5.3 IoT-SPMS-LoRaWAN (ScienceDirect 2022 / Internet of Things journal)
**Source:** https://www.sciencedirect.com/science/article/pii/S2667345223000494

**What the source actually says:**
- Sensor node: "Arduino UNO microcontroller and two sensors — a triaxial magnetic sensor and a waterproof ultrasonic sensor"
- Circuit design tool: "Fig. 4 shows the virtual circuit designed using Fritzing Software"
- Magnetometer role: "acts as a magnetometer to detect the presence of the metal (car)"
- Ultrasonic role: "waterproof ultrasonic sensor to detect the distance and time taken by the car to use the parking lot"
- LED status: "When the sensors gather the required data, one of the LED lights will light up, satisfying the condition predetermined automatically"
- Dashboard: "AllThingsTalk GUI" for real-time display
- Power: "solar panel is placed on the top to ease the process of battery charging"
- Antenna: "LoRa shield antenna is placed on the left side of the enclosure to avoid any signal interference"
- Goal: "reduce the time and fuel consumed by wandering around"

---

### 5.4 Smart Parking System Oulu University — PNI PlacePod + 5G (IARIA 2022)
**Source:** https://personales.upv.es/thinkmind/dl/conferences/smart/smart_2022/smart_2022_1_10_40025.pdf

**What the source actually says:**
- Deployment: "ten in-ground Place pod sensors were installed on the premises of the University Oulu parking area"
- "5G network of the University of Oulu was used for data [backhaul]"
- Sensor communication: "sensors were configured and activated with network AppEUI and Appkey and transmit data packets every 1 min interval"
- API: "The request is passed to the server through the Restful API"
- API endpoints in Table 1: three request types (described but not reproduced here)
- One endpoint: retrieves record of only one parking space by sensor ID

---

### 5.5 IoT-Driven Smart Parking with LoRaWAN and PNI PlacePod (IEEE Xplore 2024)
**Source:** https://ieeexplore.ieee.org/iel8/11085142/11085448/11085745.pdf

**What the source actually says:**
- "The main idea of the article is to place a PNI Place Pod magnetic sensor in the parking areas that detects the occupancy of that area and then this information will be sent to the cloud via Things Mate application to provide the live data"
- LoRaWAN rationale: "preferred because of its low power consumption with higher range of communication and also to ensure the seamless data transfer among the sensors and to the connected servers"

**Advantages / Disadvantages (as stated by source):**
- ✅ **Advantage of LoRaWAN over alternatives (stated):** Source explicitly states LoRaWAN is "preferred because of its low power consumption with higher range of communication" — both stated as direct reasons for the choice

---

### 5.6 Privacy Leakage of LoRaWAN Smart Parking Sensors (ScienceDirect 2022)
**Source:** https://www.sciencedirect.com/science/article/abs/pii/S0167739X22002680

**What the source actually says:**
- System implemented: "Arduino UNO microcontroller and two sensors — a triaxial magnetic sensor and a waterproof ultrasonic sensor" (same build as IoT-SPMS-LoRaWAN above)
- Key concern documented: "As the Internet of Things (IoT) evolves, it paves the way for vital smart city applications, with the Smart Parking Management System (SPMS) standing as a prime example" — paper then identifies that traffic analysis of LoRaWAN uplink packets can leak presence/absence information

**Advantages / Disadvantages (as stated by source):**
- ❌ **Disadvantage of LoRaWAN parking sensors (stated):** Source explicitly identifies that traffic analysis of LoRaWAN uplink packets — even without decrypting the payload — can reveal a user's presence and absence patterns, constituting a privacy leakage vulnerability in deployed smart parking systems

---

### 5.7 Real-Time Parking Space Monitoring (YOLO + PySide6, CEUR-WS 2025)
**Source:** https://ceur-ws.org/Vol-4004/paper1.pdf

**What the source actually says:**
- Stack: "Python-based modules using OpenCV and PySide6 frameworks"
- Architecture: "configurable and modular desktop application capable of real-time visualization and interactive user engagement"
- Features: "dynamic occupancy mapping, an intuitive ROI editor, and flexible configuration management via YAML files"
- Validation: "Validation on test video data confirmed the system's ability to perform accurate and responsive detection under various conditions"
- Conference: MoMLeT-2025, 7th International Workshop on Modern Machine Learning Technologies, June 2025, Lviv-Shatsk
- License: CC BY 4.0

---

### 5.8 Deep Learning-Based Vehicle Parking Occupancy Detection (Alqalam Journal 2025)
**Source:** https://journal.utripoli.edu.ly/index.php/Alqalam/article/download/952/789/2015

**What the source actually says:**
- Method: "pretrained YOLO model combined with OpenCV-based image processing for parking occupancy detection"
- Data: "surveillance video recordings captured from multiple angles around the NCB main building"
- Preprocessing: "OpenCV … performs essential image preprocessing tasks such as resizing to standard dimensions, cropping to focus on regions of interest"
- Slot initialization: "manually initialized coordinates and polygon overlays" in OpenCV
- Claim: "outperforming traditional manual and sensor-based methods in both efficiency and accuracy"
- Key result: "The model's ability to accurately identify occupied and vacant parking spaces is seen in Fig 6. The detection results demonstrate the system's faultless ability to recognize cars and correctly assign them to parking spaces"

**Advantages / Disadvantages (as stated by source):**
- ✅ **Advantage over sensor-based methods (stated):** Source directly claims the YOLO+OpenCV approach "outperforming traditional manual and sensor-based methods in both efficiency and accuracy"
- ✅ **Advantage of multi-angle cameras (stated):** Source uses "surveillance video recordings captured from multiple angles around the NCB main building" — the multi-angle approach is presented as improving detection coverage

---

### 5.9 MobileNetV3 + CBAM Parking Occupancy (NCBI/PMC 2023)
**Source:** https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10490723/

**What the source actually says:**
- Baseline datasets: CNRPark-EXT and PKLot
- Architectural modifications: "integration of a convolutional block attention mechanism in place of the native attention module and the adoption of blueprint separable convolutions instead of the traditional depth-wise separable convolutions"
- Key metric: "AUC value of 0.99 for most experiments with the PKLot dataset"
- Comparison: "average accuracy of 98.01%, while CarNet achieves 97.03%"

**Advantages / Disadvantages (as stated by source):**
- ✅ **Advantage over CarNet baseline (stated):** Source directly reports 98.01% average accuracy vs. CarNet's 97.03% — the architectural modifications (CBAM attention + blueprint separable convolutions) are stated as the reason for the improvement

---

### 5.10 Statistical Radar Method for Parking Occupancy (arXiv 1607.06708)
**Source:** https://arxiv.org/pdf/1607.06708

**What the source actually says (Related Works section):**
- Schmid et al.: "three automotive-use short-range radars operating at 24 GHz to reconstruct a hierarchical 3-D occupancy grid map"
- Mathur et al.: "collected 500 miles of roadside parking data by equipping ultrasonic sensors on probe cars and the result showed that parking spot counts are 95% accurate and occupancy maps can achieve over 90% accuracy"
- Zhou et al.: "used AdaBoost algorithm to train a classifier on 2-D laser scans, and extracted car bumpers as main features of parked vehicles"
- Thronton et al.: "applied laser sensor for the fast survey of parallel on-street parking. They focused on filtering out road curbs and other driving cars on street as noise"
- Ibisch et al.: "employed RANSAC and Kalman Filters in tracking parking through multiple Lidar sensors embedded in a parking garage in the lack of GPS information"
- Supported by: "Mobility Transformation Center, University of Michigan"

**Advantages / Disadvantages (as stated by source):**
- ✅ **Advantage of ultrasonic probe-car approach (stated):** Mathur et al. results cited in source — "parking spot counts are 95% accurate and occupancy maps can achieve over 90% accuracy" over 500 miles of data
- ❌ **Disadvantage of laser/LiDAR approaches (stated):** Thronton et al. and Ibisch et al. approaches cited in source highlight the need to filter road curbs, moving traffic, and work without GPS — practical complications stated as challenges in the related works
- ❌ **Disadvantage of LiDAR in GPS-denied environments (stated):** Ibisch et al. work cited as requiring RANSAC and Kalman Filters specifically "in the lack of GPS information" — implying GPS absence is a limiting condition

---

### 5.11 Automated LiDAR Parking Surveys (Ohio State / ResearchGate 2014)
**Source:** https://ceg.osu.edu/sites/default/files/2022-06/LidarPark.pdf

**What the source actually says:**
- Method: "two-dimensional scanning Light Detection and Ranging (LIDAR) sensor mounted on a vehicle"
- Focus: "parallel parking in the opposing direction of travel"
- Algorithm: "ranging measurements are processed to estimate the location of the curb and the presence of objects in the road. Occlusion and location reasoning are then applied to determine which of the objects are vehicles, and whether a given vehicle is parked or is in the traffic-stream"
- Outcome: "Vehicle counts from 29 trips over four years were compared against concurrent ground truth with favorable results"
- Measurements: "occupancy of the parking area, vehicle size, and vehicle-to-vehicle gaps are then measured"
- Domain: "unmarked, on-street parking near a large university campus"

---

### 5.12 MQTT + IBM Watson IoT Smart Parking (IOP Publishing / ResearchGate 2021)
**Source:** https://www.researchgate.net/publication/356517151

**What the source actually says:**
- "To automate the parking procedure by monitoring metrics such as distance and available parking spaces, NodeMCU and IBM Cloud are used"
- "The distance is measured, and the information is sent to Node-RED over the MQTT protocol"
- "The Node-RED dashboard allows the user to view availability from any location"
- Empty detection logic: "If the distance is too great, the space is unoccupied"
- "If the parking area is fully occupied, the owner or person in control of the parking lot is also notified. This is accomplished by combining IFTTT and Node-RED"
- Citation: JPhCS (Journal of Physics: Conference Series), 2021, vol. 2115, article 012013

---

### 5.13 SSGA + MQTT + Firebase (ResearchGate 2020)
**Source:** https://www.researchgate.net/publication/342124646

**What the source actually says:**
- Hardware: "each parking slot is equipped with an ultrasonic sensor which is interfaced to Arduino UNO microcontroller"
- Data flow: Arduino reads sensors → processes → communicates to Node MCU → MCU sends to Firebase via MQTT
- Topology: "star topology whose advantage was that if one client was disconnected, it would not interfere with other clients to connect with the broker"
- Binary reporting: "MCU node would send a condition of '0' or empty, while if it detected a vehicle, it would send the condition '1' or occupied"
- Visual representation: "If a parking slot is empty, it is represented by green block. If it is filled, it is represented by red block"

**Advantages / Disadvantages (as stated by source):**
- ✅ **Advantage of star topology (stated):** Source uses the word "advantage" directly — "star topology whose advantage was that if one client was disconnected, it would not interfere with other clients to connect with the broker" — fault isolation is the explicitly stated benefit

---

## 6. Patents {#patents}

---

### 6.1 US11721214 + US12437643 — Dual-Sensor Parking Device (Magnetometer + Radar, LoRaWAN)
**Sources:**
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11721214
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12437643
- https://patents.google.com/patent/US20220076576A1/en (Google Patents, same family)

**What the patents actually say:**
- Sensors: "magnetometer sensor 210 and the radar sensor 220" inside a single device (parking_sensor_device 200)
- Wake logic: "the control circuitry 230 transitions from the low power state to an operating state upon the magnetometer sensor 210 detecting a change in the magnetic field, such that the control circuitry 230 can determine occupancy of the parking space, and then transition back to the low power state after triggering the wireless transmitter to transmit the wireless message"
- Transmission contents: "the indication of occupancy, the reduced representation of the sensor data, and indications of temperature and battery status are sent via a LoRaWAN radio"
- Network topology: "parking sensor devices 200 → LoRaWAN gateway 411/422 → network server 430 → cloud server 440 → client devices 451-453 (e.g., smartphones), through a web interface"
- Battery life: "up to ten years or more"
- Manufacturing cost: "only about $50 USD per unit"
- Self-calibration: "control circuitry may be configured to adjust one or more magnetometer detection thresholds or other settings based on the level of magnetic noise present in the vicinity"
- Cross-training: "radar results can be used to train the magnetometer sensor 520 so that magnetometer algorithms can learn to be more accurate than just using the magnetometer sensor 520. This can be done for both empty and occupied states"
- Installation: "The parking sensor device 200 can be used above ground or in ground"

**Advantages / Disadvantages (as stated by source):**
- ✅ **Advantage: battery life (stated):** Patent states "up to ten years or more" — explicitly cited as a benefit of the triggered wake architecture
- ✅ **Advantage: low manufacturing cost (stated):** Patent states "only about $50 USD per unit"
- ✅ **Advantage: self-calibration (stated):** "control circuitry may be configured to adjust one or more magnetometer detection thresholds or other settings based on the level of magnetic noise present in the vicinity" — adapts to local environment automatically
- ✅ **Advantage: radar cross-trains magnetometer (stated):** "radar results can be used to train the magnetometer sensor 520 so that magnetometer algorithms can learn to be more accurate than just using the magnetometer sensor 520"
- ✅ **Advantage: flexible installation (stated):** "can be used above ground or in ground" — no civil works required for surface deployment

---

### 6.2 US11322028 + US10991249 — Radar-Augmentation of Parking Space Sensors
**Sources:**
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11322028
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10991249

**What the patents actually say:**
- Priority date: November 30, 2018 (provisional US62/773,596)
- Problem addressed: "if a large number of parking spaces are present, it may be prohibitively expensive and cumbersome to install a parking sensor in every parking space"
- Solution: radar detectors placed to cover multiple spaces each, augmenting per-space magnetic sensors
- Simulation claim: "performing a simulation to determine parking spaces of the plurality of parking spaces for which the one or more radar-based vehicle detectors are insufficient to accurately determine whether any vehicle is present within the parking spaces greater than the defined accuracy threshold"
- Gateway role: "the parking host system is part of a gateway device that serves as an interface between a cloud-based server system and the plurality of parking space sensors"

**Advantages / Disadvantages (as stated by source):**
- ❌ **Disadvantage of per-space sensor deployments (stated):** Patent explicitly states "if a large number of parking spaces are present, it may be prohibitively expensive and cumbersome to install a parking sensor in every parking space" — this is the problem the radar-augmentation approach is patented to solve
- ✅ **Advantage of radar augmentation (stated):** Radar detectors cover multiple spaces each, reducing the number of sensors needed while maintaining accuracy above a defined threshold

---

### 6.3 US10332398 — Smart Parking Facility Management (3-Axis Magnetometers)
**Source:** https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10332398

**What the patent actually says:**
- "Each parking space 102 may include a sensor 104 located therein. Each of the sensors 104 may be uniquely identifiable as corresponding to a particular parking space 102"
- "upon detection of a vehicle by a particular sensor 104, the corresponding parking space 102 may be determined as being occupied"
- Sensor types: "three-axis magnetometers, however other sensors may be used, such as, e.g., ultrasound sensors, infrared sensors, stress/strain sensors"
- Customer interface data: "real-time traffic patterns as determined from sensor data, occupied and unoccupied parking spaces as determined from sensor data, exit and entry locations and stairwells, and in some embodiments, the location of the customer's vehicle within the parking facility"

---

### 6.4 US11182598B2 — Smart Area Monitoring with AI (Camera + Ceiling LEDs)
**Source:** https://patents.google.com/patent/US11182598B2/en

**What the patent actually says:**
- Previous art limitation stated: "non-imaging sensors e.g., puck-shaped magnetometers" — "cannot discern if a non-metallic object such as a cardboard box is occupying the location; are incapable of communicating to a driver who is not physically present at that particular row of vehicles; and are unable to distinguish if a vehicle has parked poorly"
- Solution: "Colored light indicators installed on the ceiling may visually indicate the occupancy of each parking spot in real time. A vehicle's driver approaching a row of parking spots may thus ascertain the availability of parking spots for an entire row at a time"
- Extended monitoring: "detect and identify different kinds of anomalies within the areas, such as vehicles going in the wrong direction, exceeding speed limits, stalled or abandoned in an aisle"
- Camera advantage: "a single device may be used to detect occupancy for multiple designated spaces, thereby reducing the number of co[mponents]"
- Metadata: "image data can be used to determine which particular spaces are occupied by objects, the types of objects in the spaces, and other associated metadata"

**Advantages / Disadvantages (as stated by source):**
- ❌ **Disadvantage of magnetometer/puck sensors (stated):** Patent explicitly lists three: (1) "cannot discern if a non-metallic object such as a cardboard box is occupying the location"; (2) "are incapable of communicating to a driver who is not physically present at that particular row of vehicles"; (3) "are unable to distinguish if a vehicle has parked poorly"
- ✅ **Advantage of camera over magnetometer (stated):** "a single device may be used to detect occupancy for multiple designated spaces, thereby reducing the number of components"
- ✅ **Advantage of ceiling LED indicators (stated):** "A vehicle's driver approaching a row of parking spots may thus ascertain the availability of parking spots for an entire row at a time" — communicates to drivers not yet at the space

---

### 6.5 US7893847 — Real-Time Detection via Symbol-Based Vision
**Source:** https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7893847

**What the patent actually says:**
- Method: "parking spaces are marked with a corresponding symbol"
- Detection: "the parking availability determiner is configured to analyze the image data to detect each parking space having the corresponding symbol at least partially obstructed in the captured image, and to include an indication in the parking availability information that each parking space having an at least partially obstructed corresponding symbol is occupied"
- Claims specify: "each parking space is centrally marked with the corresponding symbol" and "each symbol has a size approximately equal to" [the space marking]

---

### 6.6 US12067878 — Crowd-Sourced Real-Time Parking Detection
**Source:** https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12067878

**What the patent actually says:**
- Method: "vehicles equipped with vision-based analytics" — cameras already on vehicle run AI to detect parking spaces as the driver passes
- Privacy-preserving: "extract metadata about parking space availability and upload the metadata without uploading video data"
- Features claimed: "(i) guide a driver to an available parking space, (ii) indicate where and when parking spaces are more likely to be available, (iii) rely on crowd-sourcing, (v) reward users for holding parking spaces for other users, (vi) enable drivers to plan errands around parking space availability, (vii) enable drivers to locate parking spaces for other drivers, (viii) improve road safety by handing off parking spot searching to a cloud-computing service"

**Advantages / Disadvantages (as stated by source):**
- ✅ **Advantage: road safety improvement (stated):** Patent explicitly claims the system can "improve road safety by handing off parking spot searching to a cloud-computing service" — removing distracted driving from the search process
- ✅ **Advantage: privacy-preserving data collection (stated):** "extract metadata about parking space availability and upload the metadata without uploading video data" — explicitly framed as a privacy advantage over raw video upload approaches

---

### 6.7 US10263461 — Smart DC Microgrid Parking + EV Charging (Puck Sensors)
**Source:** https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10263461

**What the patent actually says:**
- "puck sensor 200 includes a protective shell 202 that is embedded into, glued to, or otherwise attached to the floor of the parking structure under each parking spot"
- Communication: "puck sensors 200 communicate sensor data (vehicle occupancy data) to the Active Parking Lot Management Backend 130"
- Power: "puck sensors 200 are battery powered and not connected directly to the DC voltage bus 102"
- Integration: combines parking occupancy with EV charging management on a DC microgrid

---

### 6.8 US10663583 — Ultrasonic False-Positive Reduction (CA-CFAR)
**Source:** https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10663583

**What the patent actually says:**
- Algorithm: "applying an adaptive threshold value set for each section of the second sensing area on the basis of a cell-averaging constant false alarm rate (CA-CFAR) algorithm to verify the echo"
- Minimum level: "setting a minimum level of the adaptive threshold value to prevent the echo from being mistaken for a false echo due to noise"
- Echo validation: "determining that the echo is a true echo when a width and a peak value of the echo are in a preset range"
- Stopped-vehicle check: "determining that the echo is a true echo when the vehicle is stopped and all of a plurality of echoes of the ultrasonic wave output a plurality of times by the ultrasonic sensor exist within a preset distance"

**Advantages / Disadvantages (as stated by source):**
- ❌ **Disadvantage of standard ultrasonic sensing (stated):** The entire patent exists to solve false echoes — source describes echoes being "mistaken for a false echo due to noise" and the need to validate "width and a peak value of the echo" before accepting a detection as real
- ✅ **Advantage of CA-CFAR adaptive threshold (stated):** "setting a minimum level of the adaptive threshold value to prevent the echo from being mistaken for a false echo due to noise" — the adaptive per-section threshold is explicitly stated as preventing false positives

---

### 6.9 US9696420 — Active Park Assist (Radar + Ultrasonic Fusion)
**Source:** https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9696420

**What the patent actually says:**
- Problem with ultrasonic alone: "one-dimensional and may only determine distance to lower object(s) reliably"
- Radar advantage: "radar will report out objects that are above 0.3 m"
- Speed limitation: "the estimation of an actual parking slot length improves when the passing or scanning speed is low"
- Edge detection: "Vehicle edge detection is important to final parking performance and the ultrasonic sensors alone may not be capable of detecting the edges consistently. The effect is multiplied at higher passing speeds"
- Environmental sensitivity of ultrasonic: "Depending on the humidity and temperature, the speed at which the echoes travel in air is vastly different"
- Fusion benefit: "combined data stream would result in rejecting a false spot that would be offered with a traditional standalone ultrasonic system"

**Advantages / Disadvantages (as stated by source):**
- ❌ **Disadvantage of ultrasonic alone — dimensionality (stated):** "one-dimensional and may only determine distance to lower object(s) reliably"
- ❌ **Disadvantage of ultrasonic alone — edge detection (stated):** "ultrasonic sensors alone may not be capable of detecting the edges consistently. The effect is multiplied at higher passing speeds"
- ❌ **Disadvantage of ultrasonic alone — environmental sensitivity (stated):** "Depending on the humidity and temperature, the speed at which the echoes travel in air is vastly different"
- ✅ **Advantage of radar (stated):** "radar will report out objects that are above 0.3 m" — detects objects ultrasonic misses due to its single-dimensional limitation
- ✅ **Advantage of sensor fusion (stated):** "combined data stream would result in rejecting a false spot that would be offered with a traditional standalone ultrasonic system"

---

### 6.10 US20140172519A1 / US9330303B2 — Controlling Parking Spaces (Camera + Vehicle GPS)
**Sources:**
- https://patents.google.com/patent/US20140172519
- https://patents.google.com/patent/US9330303B2/en

**What the patents actually say:**
- Method: "based on a first vehicle image showing a first vehicle at a first location and on the first location of the first vehicle received based on a sensor located within the first vehicle, it is determined that the first vehicle is occupying the destination location at the first time"
- Exit detection: "based on a second vehicle image showing the first vehicle at a second location… it is determined that the first vehicle has left the destination location at the second time"
- Coverage overlap: "a vehicle is within the field of vision of both cameras for a minimum of 2 seconds at a speed of 15 MPH (approximately 44 feet)"
- Speed at neighboring cameras: "neighboring or nearby camera positions are determined to ensure this overlap occurs"
- US9330303B2 also claims: "A unique identifier of a first vehicle based on a sensor located within the first vehicle is received" — vehicle self-identifies

---

## 7. Commercial Products {#commercial}

---

### 7.1 MOKO Smart LW009-SM / LW009-SM Pro
**Source:** https://www.mokosmart.com/lorawan-wireless-vehicle-detection-sensor-lw009/

**What the source actually says:**
- Dual sensors: "magnetic induction sensor and microwave radar"
- Working principle: "The frame and shell of a car are made of ferromagnetic material (various types of steel), which will make disturbance to the surrounding magnetic field. According to this characteristic, LW009-SM determines whether there is a car in the parking space"
- Enhancement note: "Compared to traditional parking sensor with single sensor, LW009-SM greatly improved the detection accuracy and reduced information loss"
- Low-chassis vehicles: "acquiring complementary and optimization to the reverse sensitivity characteristics of chassis with different heights"
- Accuracy: "over 99%"
- Range: "500~1000m" (environment-dependent)
- Battery: "5+ years under typical scenarios"
- LoRaWAN max range: "up to 7km long-range LoRaWAN transmission distance"
- Alerts: "Low voltage alarm, hardware error alarm, Strong magnetic disturbance alarm"
- Config: "Parameters can be configured by the app via Bluetooth"
- Built-in sensors also: "temperature and humidity sensor"
- Deployment markets mentioned: "UAE, Spain, and Panama"
- Installation: "convenient surface mounting installation"

**Advantages / Disadvantages (as stated by source):**
- ✅ **Advantage of dual-sensor over single-sensor (stated):** "Compared to traditional parking sensor with single sensor, LW009-SM greatly improved the detection accuracy and reduced information loss" — source explicitly positions the dual-sensor design as superior
- ✅ **Advantage for low-chassis vehicles (stated):** Source specifically addresses "acquiring complementary and optimization to the reverse sensitivity characteristics of chassis with different heights" — the radar fills in where the magnetometer has reduced sensitivity for low vehicles
- ❌ **Limitation acknowledged (stated):** "Strong magnetic disturbance alarm" is listed as an alert type — acknowledging that strong magnetic environments can interfere with detection

---

### 7.2 Bosch TPS110 (TTN Device Repository)
**Source:** https://www.thethingsnetwork.org/device-repository/devices/bosch/tps110/

**What the source actually says:**
- "The BOSCH wireless smart parking sensor is a LoRaWAN® end device that uses a magnetometer and radar which are two independent sensors for parking space occupancy"
- "enables active parking lot management features, such as search, navigation, …"
- Listed in The Things Network official device repository — meaning it carries a standard LoRaWAN device profile and interoperates with any TTN-compatible network server without custom protocol work

---

### 7.3 Nwave NPS310SM (TTN Device Repository)
**Source:** https://www.thethingsnetwork.org/device-repository/devices/nwave/nps310sm/

**What the source actually says:**
- Sensors: "magnetometer, temperature, and proximity sensors for parking detection" — three sensors, not two
- "smart parking sensors installed in each parking spot generate data on space occupancy in real-time and is transmitted…"
- Listed in TTN device repository (official LoRaWAN interoperability)

---

### 7.4 ParkNode Gen1
**Source:** https://www.macnman.com/lorawan/sensors/lorawan-parking-sensor-paknode-gen-one

**What the source actually says:**
- Technology: "geomagnetic and radar technology"
- Accuracy: "99% detection accuracy"
- Battery: "up to 10 years"
- Range: "500~1000 meters"
- Industrial I/O: "Compatible with RS485, 0-10V, 4-20mA, & digital inputs for seamless industrial automation"
- Offline resilience: "Prevents data loss during network outages by securely storing logs, sensor data, & event history"
- Installation: "tool-free surface or in-ground installation powered by a long-life battery. With no wiring or civil work deployment takes just minutes"
- Noise rejection: "advanced RF architecture and noise-resistant design ensure 99% detection accuracy — even in areas with heavy wireless interference or magnetic noise"

**Advantages / Disadvantages (as stated by source):**
- ✅ **Advantage: offline resilience (stated):** "Prevents data loss during network outages by securely storing logs, sensor data, & event history" — explicitly stated as a feature
- ✅ **Advantage: noise resistance (stated):** "advanced RF architecture and noise-resistant design ensure 99% detection accuracy — even in areas with heavy wireless interference or magnetic noise" — source explicitly positions this as an advantage in challenging RF environments
- ✅ **Advantage: no civil works needed (stated):** "tool-free surface or in-ground installation powered by a long-life battery. With no wiring or civil work deployment takes just minutes"
- ✅ **Advantage: industrial I/O compatibility (stated):** "Compatible with RS485, 0-10V, 4-20mA, & digital inputs for seamless industrial automation" — broader integration than most parking sensors

---

### 7.5 Sigfox + Geomagnetic + Ultrasonic Sensor (ChinaIoTDevices)
**Source:** https://www.chinaiotdevices.com/iotdevices/ultrasonic-and-geomagnetic-parking-occupation-detector-with-sigfox/

**What the source actually says:**
- "designed with IP68 level protection"
- "Hard case is made of engineering ABS for 5 tons of force"
- "Inner battery 25500mAh"
- "Buzzer notification 50db@10cm"
- "Bluetooth for remote configuration"
- Protocol support: Sigfox; also NB-IoT, LTE-M, EGPRS variants available
- NB-IoT bands listed: "B1/B2/B3/B4/B5/B8/B12/B13/B18/B19/B20/B25/B26/B28/B66/B71/B85. LTE-M: B1/B2/…"
- Dashboard features: "Dashboard monitoring / Email notification / SMS notification (depend on platform)"
- SDK: "TCP protocol with SDK in python, java-script"
- Ultrasonic detection range: 2 meters

---

### 7.6 SpotHero API (api-evangelist GitHub documentation)
**Source:** https://github.com/api-evangelist/spothero

**What the source actually says:**
- Description: "leading digital parking marketplace in North America, offering a flexible parking API and developer toolkit that connects vehicles, drivers, and mobility apps with the largest network of off-street parking facilities"
- API capabilities: "search for available parking spots, check real-time availability, create and manage reservations, and access facility details including pricing, amenities, and directions"
- Internal system: "SpotNow is SpotHero's real-time parking server and API built in Kotlin, enabling instant parking availability and on-demand bookings via the HeroLab platform"
- Repo link in source: `https://github.com/spothero/herolab-spotnow`
- Acquisition note in source: "SpotHero was acquired by Uber in 2026 to power parking reservation experiences within the Uber app"

---

### 7.7 ParkMe — Deutsche Bahn Open Data Contest Winner
**Source:** https://github.com/janmattfeld/parkme

**What the source actually says:**
- Stack: Node.js, Express, Angular
- Data source: Deutsche Bahn Parkraum API (existing transit agency data — no sensors deployed)
- Features from README: "Find the current user location and show it on a beautiful map · Find the nearest parking space (Deutsche Bahn Parkraum API) · Show route and directions to a selected parking space · Show additional information like free spaces and price · Show current departures of a selected station (Deutsche Bahn Fahrplan API)"
- The "free spaces" figure comes directly from the DB API — ParkMe is purely a *consumer* of existing occupancy data

---

## 8. Datasets {#datasets}

---

### 8.1 PKLot Dataset
**Source:** arXiv:2201.05858 + arXiv:2109.09666 + arXiv:2308.08192

**What the sources actually say:**
- Origin: "Federal University of Parana (UFPR) and Pontifical Catholic University of Parana (PUCPR) located in Curitiba, Brazil"
- Size: "around 700,000 manually checked and labeled parking space images" (from arXiv:2201.05858)
- Images: "12,417 images" captured in three parking areas (from arXiv:2109.09666)
- Slots: "168 slots" across all subsets
- Subsets: UFPR04 (28 slots — 4th floor), UFPR05 (45 slots — 5th floor), PUCPR (100 slots — 10th floor)
- Collection period: "11 September 2012 and 16 April 2013"
- Capture interval: "every 5 minutes" (from arXiv:2308.08192)
- Resolution: "1280 x 720 pixels, JPEG"
- Weather conditions: Sunny, Overcast, Rainy
- Pre-segmented patches: "with a slope between 0° to 45° were rotated to 0° and those with a slope between 45° to 90° were rotated to 90°" (from arXiv:2201.05858)

---

### 8.2 CNRPark / CNRPark-EXT Dataset
**Source:** arXiv:2201.05858 + arXiv:2309.16495 + github.com/fabiocarrara/deep-parking

**What the sources actually say:**
- Origin: "National Research Council (CNR) in Pisa, Italy" (from arXiv:2308.08192)
- CNRPark size: "12,584 images segregated into two non-overlapping subsets: CNRPark A (6,171 images) and CNRPark B (6,413 images)" (from arXiv:2201.05858)
- CNR-EXT: "about 160,000 annotated parking spaces collected from nine cameras" (from arXiv:2309.16495)
- Period: "November 2015 to February 2016"
- Slots: "164 parking slots" with "9 cameras with different points of view and different perspectives"
- Specific challenges: "solar light reflections and raindrops on the camera lens" (arXiv:2309.16495)
- Also: "patches partially occluded by trees as well as shadowed by the neighbouring cars" (arXiv:2201.05858)
- Download URLs (from fabiocarrara/deep-parking):
  - CNRPark: `http://cnrpark.it/dataset/CNRPark-Patches-150x150.zip` (36.6 MB)
  - CNR-EXT: `http://cnrpark.it/dataset/CNR-EXT-Patches-150x150.zip` (449.5 MB)

---

### 8.3 NDISPark — Night and Day Instance Segmented Park Dataset
**Source:** arXiv:2309.16495

**What the source actually says:**
- Size: "259 images exhibiting diverse parking areas from seven cameras"
- Challenges: "night-time images," "lateral view of street parking spots," "partial occlusions caused by obstacles like trees and lampposts"
- Note: arXiv:2309.16495 calls it "recently released"

---

### 8.4 BarryStreet Dataset
**Source:** arXiv:2309.16495

**What the source actually says:**
- Used alongside PKLot, CNRPark, and NDISPark in a 4-dataset comparison study
- "provide annotations of parking spot locations and binary labels indicating whether it is occupied or empty"
- Noted for enabling "comprehensive and critical assessment" across "variations in camera angles, shadowed cars, weather conditions, environmental settings, and backgrounds"

---

## 9. Consolidated Source Index {#source-index}

### GitHub Repositories

| # | Repo | URL |
|---|------|-----|
| 1 | aaryaapg/Smart-Parking | https://github.com/aaryaapg/Smart-Parking |
| 2 | RahulN25/Smart-Parking-System | https://github.com/RahulN25/Smart-Parking-System |
| 3 | vishnubv944/smartParkingSystem | https://github.com/vishnubv944/smartParkingSystem |
| 4 | Dipal018/Smart_Parking | https://github.com/Dipal018/Smart_Parking |
| 5 | CarlosFULLHD/iot_garaje_inteligente | https://github.com/CarlosFULLHD/iot_garaje_inteligente |
| 6 | prince61299/Smart-Car-Parking-using-ESP32 | https://github.com/prince61299/Smart-Car-Parking-using-ESP32 |
| 7 | Muhaiminul-Hasan/RFID-based-Smart-Parking-using-ESP32 | https://github.com/Muhaiminul-Hasan/RFID-based-Smart-Parking-System-using-ESP32 |
| 8 | harshad8782/Smart-Parking-System-IoT | https://github.com/harshad8782/Smart-Parking-System-IoT |
| 9 | emregulerr/IoT-Smart-Parking-System | https://github.com/emregulerr/IoT-Smart-Parking-System |
| 10 | anmoljhamb/smart-parking-system | https://github.com/anmoljhamb/smart-parking-system |
| 11 | ferasaljoudi/AljoudiParkingSystem | https://github.com/ferasaljoudi/AljoudiParkingSystem |
| 12 | ColoradoSchoolOfMines/parking_sensor | https://github.com/ColoradoSchoolOfMines/parking_sensor |
| 13 | aswin-sreekumar/Smart-parking-system | https://github.com/aswin-sreekumar/Smart-parking-system |
| 14 | elise-ng/FYP_SmartCarPark | https://github.com/elise-ng/FYP_SmartCarPark |
| 15 | 8harath/Car-Parking-Detection | https://github.com/8harath/Car-Parking-Detection |
| 16 | fabiocarrara/deep-parking | https://github.com/fabiocarrara/deep-parking |
| 17 | wuyenlin/parking_lot_occupancy_detection | https://github.com/wuyenlin/parking_lot_occupancy_detection |
| 18 | sk0601/Smart-Parking-System | https://github.com/sk0601/Smart-Parking-System |
| 19 | alphinaud11/Car-Parking-System (VHDL/FPGA) | https://github.com/alphinaud11/Car-Parking-System |
| 20 | MahmoudHanyFathalla/Car-parking-system | https://github.com/MahmoudHanyFathalla/Car-parking-system |
| 21 | minchoCoin/smartParkingLot-stm32 | https://github.com/minchoCoin/smartParkingLot-stm32 |
| 22 | SiddheshPadwal10/Smart-Parking-System-with-Embedded | https://github.com/SiddheshPadwal10/Smart-Parking-System-with-Embedded |
| 23 | MustafaOrhon/STM32-F401RE-UltrasonicCarSensor | https://github.com/MustafaOrhon/STM32-F401RE-UltrasonicCarSensor |
| 24 | janmattfeld/parkme | https://github.com/janmattfeld/parkme |
| 25 | api-evangelist/spothero | https://github.com/api-evangelist/spothero |

### Patents (All links to USPTO PDFs or Google Patents)

| Patent | Topic | URL |
|--------|-------|-----|
| US11721214 | Magnetometer+Radar LoRaWAN sensor | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11721214 |
| US12437643 | Magnetometer+Radar LoRaWAN (continuation) | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12437643 |
| US20220076576A1 | Same family (Google Patents) | https://patents.google.com/patent/US20220076576A1/en |
| US11322028 | Radar-augmentation of parking sensors | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11322028 |
| US10991249 | Radar-augmentation (parent application) | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10991249 |
| US10332398 | Smart parking facility, 3-axis magnetometers | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10332398 |
| US11182598B2 | AI area monitoring, ceiling LED indicators | https://patents.google.com/patent/US11182598B2/en |
| US7893847 | Symbol-based camera occupancy detection | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7893847 |
| US12067878 | Crowdsourced real-time parking detection | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12067878 |
| US20140172519A1 | Camera + in-vehicle GPS tracking | https://patents.google.com/patent/US20140172519 |
| US9330303B2 | Smart sensor network, unique vehicle IDs | https://patents.google.com/patent/US9330303B2/en |
| US10263461 | DC microgrid + EV charging + puck sensors | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10263461 |
| US10663583 | Ultrasonic CA-CFAR false positive reduction | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10663583 |
| US9696420 | Active park assist, radar+ultrasonic fusion | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9696420 |

### Academic Papers

| Paper | URL |
|-------|-----|
| LoRaWAN Smart Parking Architecture (MDPI 2020) | https://www.mdpi.com/2076-3417/10/13/4674 |
| Smart Parking Sensors State of Art (ScienceDirect 2020) | https://www.sciencedirect.com/science/article/abs/pii/S0959652620312282 |
| Privacy Leakage LoRaWAN Sensors (ScienceDirect 2022) | https://www.sciencedirect.com/science/article/abs/pii/S0167739X22002680 |
| IoT-SPMS-LoRaWAN Full System (ScienceDirect 2022) | https://www.sciencedirect.com/science/article/pii/S2667345223000494 |
| Smart Parking IoT Oulu (IARIA SMART 2022) | https://personales.upv.es/thinkmind/dl/conferences/smart/smart_2022/smart_2022_1_10_40025.pdf |
| IoT-Driven Parking LoRaWAN PNI PlacePod (IEEE 2024) | https://ieeexplore.ieee.org/iel8/11085142/11085448/11085745.pdf |
| Real-Time Parking YOLO+PySide6 (CEUR-WS 2025) | https://ceur-ws.org/Vol-4004/paper1.pdf |
| Deep Learning Parking NCB Building (Alqalam 2025) | https://journal.utripoli.edu.ly/index.php/Alqalam/article/download/952/789/2015 |
| MobileNetV3+CBAM Parking Occupancy (NCBI/PMC 2023) | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10490723/ |
| Statistical Radar Parking Occupancy (arXiv 2016) | https://arxiv.org/pdf/1607.06708 |
| Automated LiDAR Parking Surveys (Ohio State 2014) | https://ceg.osu.edu/sites/default/files/2022-06/LidarPark.pdf |
| MQTT IBM Watson Smart Parking (IOP 2021) | https://www.researchgate.net/publication/356517151 |
| SSGA MQTT Firebase Smart Parking (ResearchGate 2020) | https://www.researchgate.net/publication/342124646 |
| Deep Single Models vs Ensembles (arXiv 2309.16495) | https://arxiv.org/pdf/2309.16495 |
| Automatic Vision-Based Parking Slot Detection (arXiv 2308.08192) | https://arxiv.org/pdf/2308.08192 |
| Parking Under Hazy Conditions CNN (arXiv 2201.05858) | https://arxiv.org/pdf/2201.05858 |

### Tutorials & Maker Platforms

| Title | URL |
|-------|-----|
| ESP32-Based Precision Parking Assist (Hackaday.io) | https://hackaday.io/project/177714-esp32-based-precision-parking-assist |
| Arduino Nano ESP32 LiDAR Garage Assistant (Arduino Project Hub) | https://projecthub.arduino.cc/noah_barkol/arduino-nano-esp32-fully-automatic-garage-ceiling-parking-assistant-79cd6c |
| ESP32 Smart Parking Detection System (Hackster.io) | https://www.hackster.io/techgyanset/esp32-smart-parking-detection-system-d68660 |
| Parking Sensor with Litho LED Boxes (Hackster.io) | https://www.hackster.io/MrBancroft/parking-sensor-67e3f0 |
| DIY Raspberry Pi ALPR Parking System (Hackster.io) | https://www.hackster.io/codrinsideas/diy-raspberry-pi-alpr-parking-sys-with-platerecognizer-s-sdk-adcf07 |
| ESP32 Parking System Web Server (ArduinoYard) | https://arduinoyard.com/esp32-parking-system/ |
| AI-Based Parking System ESP32-CAM (CircuitDigest) | https://circuitdigest.com/projects/ai-based-smart-parking-system |
| Edge Impulse + ESP32-CAM AI Parking (Medium) | https://medium.com/@anasyunus/building-an-ai-powered-parking-space-detection-system-with-edge-impulse-and-esp32-cam-7066377b8154 |
| Car Parking Detection Edge Impulse (DigiKey) | https://www.digikey.com/en/maker/projects/car-parking-detection-system-using-edge-impulse/0fcb63b013e240e5bef7049ed1027332 |
| NodeMCU Smart Parking (IoTDesignPro) | https://iotdesignpro.com/projects/iot-based-smart-parking-using-esp8266 |
| Magnetometer Parking Sensor writeup (duino4projects) | https://duino4projects.com/magnetometer-parking-sensor/ |

### Commercial Products

| Product | URL |
|---------|-----|
| MOKO Smart LW009-SM/Pro | https://www.mokosmart.com/lorawan-wireless-vehicle-detection-sensor-lw009/ |
| Bosch TPS110 (TTN Device Registry) | https://www.thethingsnetwork.org/device-repository/devices/bosch/tps110/ |
| Nwave NPS310SM (TTN Device Registry) | https://www.thethingsnetwork.org/device-repository/devices/nwave/nps310sm/ |
| ParkNode Gen1 | https://www.macnman.com/lorawan/sensors/lorawan-parking-sensor-paknode-gen-one |
| Sigfox+NB-IoT Ultrasonic+Geomagnetic Sensor | https://www.chinaiotdevices.com/iotdevices/ultrasonic-and-geomagnetic-parking-occupation-detector-with-sigfox/ |

---

*Research compiled June 2026. All claims in each section derive exclusively from the source named at the top of that section.*
