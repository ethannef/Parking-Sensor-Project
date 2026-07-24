# Parking Sensor Systems: An In-Depth Research Report
### Tracking Open Spaces, Reporting Occupancy, and Everything in Between

---

## Table of Contents

1. [Introduction & Scope](#introduction)
2. [Sensor Technology Taxonomy](#sensor-taxonomy)
3. [Communication Protocols & Network Architectures](#comm-protocols)
4. [Category A — Embedded Hardware / DIY Implementations](#category-a)
5. [Category B — Computer Vision & Deep Learning Systems](#category-b)
6. [Category C — Commercial & Industrial Deployments](#category-c)
7. [Category D — Cloud, MQTT & Dashboard Backends](#category-d)
8. [Category E — Patents](#patents)
9. [Research Datasets & Benchmarks](#datasets)
10. [Academic Papers & Literature](#papers)
11. [Comparative Analysis of Approaches](#comparison)
12. [Source Index](#sources)

---

## 1. Introduction & Scope {#introduction}

Parking sensor systems serve one primary goal: **determine which parking spaces are occupied and which are vacant, then report that status to someone who can act on it** — whether a driver looking for a spot, a city manager planning traffic flow, or a building owner billing for time-of-use.

The field spans an enormous range of sophistication, from a $3 HC-SR04 ultrasonic sensor wired to an Arduino and a local LED display, all the way to distributed LoRaWAN mesh networks of dual-mode magnetometer+radar pucks reporting to cloud backends with ML analytics. This report excavates implementations across GitHub repositories, patents, academic papers, benchmark datasets, DIY tutorials, and commercial deployments to give a complete picture of the state of the art.

---

## 2. Sensor Technology Taxonomy {#sensor-taxonomy}

Before diving into specific implementations, understanding the sensing modalities is essential, as each brings trade-offs in cost, accuracy, installation complexity, and susceptibility to environmental conditions.

### 2.1 Ultrasonic (HC-SR04, JSN-SR04T Waterproof)

**Principle:** Emit a 25–50 kHz ultrasonic pulse and time the echo return. Distance ≈ (time × speed of sound) / 2.

**Range:** Typically 2 cm – 4 m (HC-SR04); up to 7 m for industrial variants.

**Key weakness:** Speed of sound varies with temperature and humidity. Patent US10663583 addresses this with a CA-CFAR (Cell-Averaging Constant False Alarm Rate) algorithm to verify echoes, setting adaptive thresholds per sensing zone and cross-checking pulse width and peak values.

**Typical accuracy issue:** If a vehicle parks partially — or if a person walks between sensor and car — transient false-empty readings occur. IoT implementations that push to MQTT often add a debounce timer (e.g., 5–10 seconds of stable distance before reporting a state change).

**Common in:** Arduino/ESP8266/ESP32 DIY builds, early academic prototypes, in-vehicle parking assist (Ford, Toyota OEM systems).

### 2.2 Infrared (IR) Sensors

**Principle:** Active IR emits a beam; if the beam is broken or reflected, an object is present.

**Range:** Typically < 80 cm for passive reflection; break-beam configurations can span a lane.

**Key weakness:** Direct sunlight, glossy car surfaces, and rain interfere with readings. Best suited for indoor or covered garages.

**Common in:** NodeMCU/ESP32 garage systems, entry/exit gate counters.

### 2.3 Magnetometers / Geomagnetic Sensors

**Principle:** A car's steel body distorts the Earth's magnetic field. A three-axis magnetometer detects this anomaly with no moving parts, no emitted signals, and extremely low power draw.

**Why this matters:** Magnetometers are the workhorse of professional smart parking deployments. They require no line-of-sight, are unaffected by weather, and can run for 5–10 years on a single battery pack.

**Key challenge:** Environmental magnetic noise (nearby ferrous structures, underground pipes, tram rails) can cause false positives. Commercial products like the Bosch TPS110 and MOKO LW009-SM add a **microwave radar** second sensor to confirm detections, achieving stated accuracy above 99%.

**Key patent detail:** US11721214 and US12437643 describe a dual-sensor device that wakes the control circuitry only when the magnetometer detects a field change (triggered wake mode), then uses radar to confirm, then transmits via LoRaWAN — achieving 10-year battery life at ~$50/unit manufacturing cost.

### 2.4 Microwave / Radar (24 GHz, 77 GHz)

**Principle:** Doppler radar detects movement and ranging. For parked-vehicle detection, short-range 24 GHz FMCW (Frequency Modulated Continuous Wave) radar probes whether an object is present within a threshold distance.

**Advantage over ultrasonic:** Not affected by temperature or humidity. Works through light rain, snow, and direct sunlight.

**Advantage over pure magnetometer:** Detects non-ferrous objects (e.g., motorcycles, non-steel-bodied vehicles) and has no blind spot for low-chassis vehicles.

**Common in:** The Bosch TPS110 LoRaWAN sensor, MOKO LW009-SM Pro, NovaStar commercial systems, and patent US11322028 ("Radar-Augmentation of Parking Space Sensors").

### 2.5 Computer Vision (2D Camera + CV Pipeline)

**Principle:** One or more fixed cameras observe a parking lot. Software segments the image into per-space Regions of Interest (ROIs) and classifies each as occupied or vacant.

**Advantage:** One camera can cover many spaces; no per-space hardware installation.

**Key challenge:** Camera angle, lighting conditions, weather, occlusion between vehicles, and lens contamination all degrade accuracy. The standard response is to use deep learning (YOLO, CNNs, MobileNet) that generalizes across conditions.

**PKLot benchmark** showed this approach achieving 96–99% accuracy across SUNNY, OVERCAST, and RAINY conditions when trained and tested on similar domains.

### 2.6 LiDAR

**Principle:** Time-of-flight laser scanning generates a precise 3D point cloud of the environment. Parked vehicle profiles are extracted from the scan.

**Use cases:** Autonomous vehicle parking assist, mobile survey vehicles doing parking occupancy counting (probe vehicles with mounted LiDAR), and multi-LiDAR fixed installations in structured parking garages.

**Academic work:** Ohio State University's 2014 study used a 2D scanning LiDAR mounted to a vehicle to survey on-street parallel parking, comparing vehicle counts from 29 trips over 4 years against concurrent ground truth with favorable results.

### 2.7 Load Cells / Pressure Sensors

**Principle:** A weight-sensitive platform embedded in the parking space floor detects vehicle presence by mass.

**Rare but precise:** A GitHub topic project tagged `smart-parking-system` specifically uses NFC access (PN532) with HX711-based Load Cell measurement for a multithreaded architecture on Raspberry Pi 5 — one of the more unique approaches documented.

### 2.8 RFID / NFC

**Principle:** Vehicles carry an RFID tag; readers at entry/exit track which vehicle entered and which space it was assigned.

**Best for:** Access-controlled lots (hospital staff, university permit holders) where every vehicle is registered. Does not detect unauthorized parkers.

---

## 3. Communication Protocols & Network Architectures {#comm-protocols}

The sensor technology determines *what* you detect. The communication architecture determines *how* you report it, and at what cost, range, and power budget.

### 3.1 LPWAN — LoRaWAN

**Range:** 500 m – 7 km (environment-dependent).
**Power:** Ultra-low; enables 5–10 year battery life on a single cell.
**Bandwidth:** Very low (~250 bps – 50 kbps). Sufficient for occupancy events (a few bytes per transmission), but not video.
**Data flow:** Sensor → LoRaWAN Gateway → Network Server (e.g., TTN, Chirpstack) → Application Server → User App.
**Used by:** MOKO LW009-SM, Bosch TPS110, PNI PlacePod, Nwave NPS310SM, ParkNode Gen1, and academic implementations in University of Oulu (Finland) and LoRaWAN smart parking paper in MDPI Applied Sciences.

**Privacy note:** A 2022 ScienceDirect paper specifically flagged a privacy leakage vulnerability in LoRaWAN parking sensors, noting that traffic analysis of uplink packets (timing, frequency, device ID) can reveal a user's presence/absence patterns even without decrypting the payload.

### 3.2 LPWAN — NB-IoT and LTE-M (Cat-M)

**Range:** Nationwide cellular.
**Power:** Higher than LoRa but uses existing cellular infrastructure — no gateway needed.
**Used by:** Many Chinese commercial smart parking products (Chinaiotdevices.com Sigfox/NB-IoT hybrid sensor) and urban city deployments where city-wide cellular coverage already exists.

### 3.3 LPWAN — Sigfox

**Range:** Up to 40 km in ideal conditions.
**Bandwidth:** Extremely low (12 bytes per message, 140 messages/day max).
**Used by:** Sigfox ultrasonic+geomagnetic parking occupancy detectors (IP68, engineered ABS for 5-ton force tolerance), deployed in European smart city trials.

### 3.4 Wi-Fi (ESP8266, ESP32)

**Range:** ~50–150 m.
**Power:** High — requires regular charging or mains power.
**Best for:** Indoor garages with existing Wi-Fi infrastructure, or DIY prototypes.
**Common in:** NodeMCU and ESP32 projects posting to Adafruit IO, ThingSpeak, or Firebase.

### 3.5 MQTT Protocol

**What it is:** A lightweight pub/sub messaging protocol designed for constrained devices.
**Transport:** Runs over TCP/IP (Wi-Fi, Ethernet, cellular).
**Common brokers:** Mosquitto (self-hosted), HiveMQ, Adafruit IO, IBM Watson IoT.
**Typical flow:** ESP32/NodeMCU sensor publishes occupancy status to a topic (e.g., `parking/slot1/status`). A Node-RED dashboard or Firebase subscribes to that topic and updates the UI in real time.

### 3.6 REST API / HTTP

**Used when:** The application needs to support web browsers, mobile apps, and third-party integrations.
**Common in:** GitHub projects with Flask/Node.js/Spring Boot backends that expose `/slots`, `/available`, and `/reserve` endpoints.

---

## 4. Category A — Embedded Hardware / DIY Implementations {#category-a}

### 4.1 aaryaapg/Smart-Parking (GitHub)

**Source:** https://github.com/aaryaapg/Smart-Parking

**Stack:** STM32F103C microcontroller, ultrasonic sensors (entry/exit gates), IR sensors (per-slot occupancy), servo motors (gate control).

**Architecture:** Slots are individually monitored by IR sensors. Ultrasonic at the gate detects vehicle approaching. STM32 runs the control logic. Designed for multi-floor operation with simultaneous entry/exit on different floors.

**Notable feature:** Categorizes vehicles by size and weight — larger vehicles directed to ground floor. Pre-booking via mobile app integration planned.

**Scope:** Academic/institutional parking for Bangalore-area implementation.

---

### 4.2 vishnubv944/smartParkingSystem (GitHub)

**Source:** https://github.com/vishnubv944/smartParkingSystem

**Stack:** NodeMCU ESP8266, 5 IR sensors (2 at entry/exit gate, 3 for slot detection), 2 servo motors, AWS IoT Shadow, cloud server.

**Architecture:** IR sensors measure distance to the bottom of a parked car. AWS IoT Shadow stores sensor state. A cloud server reads shadow state and exposes parking availability to end users over the internet.

**Key detail:** "A sensor detects a parked car by measuring the distance to the nearest obstacle—in our case, to the bottom of the car." This framing is important — the sensor looks up at the car from below (embedded in floor or low on a bollard).

**Reporting:** Web interface accessible from anywhere; users can check slot availability before leaving home.

---

### 4.3 Dipal018/Smart_Parking (GitHub)

**Source:** https://github.com/Dipal018/Smart_Parking

**Stack:** ESP8266, proximity sensors, LED display, servo motor, Arduino IDE (C), Angular.js web interface, PhoneGap mobile app, Twilio SMS.

**Architecture:** A microcontroller-based sensor module pushes to a RESTful API middleware server. The web application reads from that API. Twilio fires SMS notifications when a parking time limit is about to expire.

**Key differentiator:** Time-limit enforcement via SMS — the system doesn't just detect occupancy; it tracks *how long* a space has been occupied and alerts the owner or the car's registered user.

---

### 4.4 CarlosFULLHD/iot_garaje_inteligente — SmartPark (GitHub)

**Source:** https://github.com/CarlosFULLHD/iot_garaje_inteligente

**Stack:** Raspberry Pi Pico W (MicroPython), presence sensors, motion sensors, keypad, servo motor, WiFi module, Spring Boot 3.0 (Java) backend, Flutter mobile app, Supabase/PostgreSQL 15.3 cloud database, Python admin dashboard.

**Architecture:** Full-stack: Pico W handles physical I/O and reports to Spring Boot API. Flutter app for users; Python dashboard for admin KPIs. Docker for the database.

**Reporting features:** Total hours occupied per spot, reservation usage stats, parking occupancy rate, space demand analytics, access control with keypad.

**Notable:** One of the more complete full-stack DIY implementations, approaching what a startup might build for a commercial product.

---

### 4.5 prince61299/Smart-Car-Parking-using-ESP32 (GitHub)

**Source:** https://github.com/prince61299/Smart-Car-Parking-using-ESP32

**Stack:** ESP32, IR sensor, servo motor, Arduino Cloud.

**Architecture:** ESP32 reads IR sensor and controls servo gate. Arduino Cloud dashboard shows real-time slot status and can be accessed from web or mobile app. Benefits from Arduino Cloud's built-in dashboard builder.

**Simplest production-viable path:** Because Arduino Cloud handles MQTT connectivity, device provisioning, and dashboard rendering, this requires minimal backend code.

---

### 4.6 prince61299 variant — ESP32 Web Server (ArduinoYard tutorial)

**Source:** https://arduinoyard.com/esp32-parking-system/

**Stack:** ESP32 DevKit, 3 IR sensors, ESPAsyncWebServer library, AsyncTCP library.

**Architecture:** ESP32 hosts an embedded web server. Sensor states update the HTML page dynamically (JavaScript polling or WebSocket). No cloud dependency — entirely local.

**Key library:** `ESPAsyncWebServer` — designed for non-blocking, concurrent web request handling on ESP32, which is critical because a blocking web server would miss sensor state changes.

---

### 4.7 ESP32-Based Precision Parking Assist — Hackaday.io

**Source:** https://hackaday.io/project/177714-esp32-based-precision-parking-assist

**Stack:** ESP32, HC-SR04 ultrasonic, WS2812B addressable LED strip (FastLED library), custom PCB in a standard plastic enclosure.

**Goal:** Single-space garage positioning assistant (helps the driver park at exactly the right distance from a wall).

**Architecture highlights:** State machine with distinct states: Approaching, InRange, Parked, TooClose. Transitions governed by configurable parameters (target_distance, approach_zone_depth). Ambient temperature measured to correct speed-of-sound calculation. NTP time server for RTC. mDNS for network discovery. ArduinoOTA for wireless firmware updates. WebSocket interface for live parameter delivery. Telnet debug interface.

**Why it stands out:** This is not a crude distance reader — it's engineered software with debounce, environmental calibration, and a proper web-based config UI.

---

### 4.8 Arduino Nano ESP32 — Garage Ceiling Parking Assistant (Arduino Project Hub)

**Source:** https://projecthub.arduino.cc/noah_barkol/arduino-nano-esp32-fully-automatic-garage-ceiling-parking-assistant-79cd6c

**Stack:** Arduino Nano ESP32, Benewake TFMini Plus LiDAR (UART, 12m range, 1000Hz, IP65), WS2812B LED strip (Adafruit NeoPixel library).

**Key code snippet (from source):**
```cpp
const int MIN_DISTANCE = 167.64;  // 66 inches — "perfect spot" (red LED)
const int MID_DISTANCE = 210.82;  // 83 inches — moderate approach (orange)
const int MAX_DISTANCE = 254;     // 100 inches — car not yet near (LEDs off)
```

**Why LiDAR over ultrasonic here:** The TFMini Plus runs at 1000 Hz with IP65 protection, far more robust than HC-SR04 for daily use. No temperature compensation needed since LiDAR uses light, not sound.

---

### 4.9 aswin-sreekumar/Smart-parking-system (GitHub)

**Source:** https://github.com/aswin-sreekumar/Smart-parking-system

**Stack:** ESP32-CAM (multiple), Raspberry Pi, cloud-deployed Node.js web server.

**Architecture:** ESP32-CAM units stream images to a Raspberry Pi. The Pi runs an Intersection over Union (IoU) algorithm — comparing predicted bounding boxes from object detection against manually drawn bounding box overlays that represent parking zones. Occupancy updates are pushed to a Node.js server.

**Key algorithmic detail:** IoU-based occupancy — if a detected car bounding box overlaps sufficiently with a predefined parking zone polygon, the space is marked occupied. This avoids per-space sensors entirely but requires careful zone calibration.

---

### 4.10 AI-Based Parking System with ESP32-CAM (CircuitDigest)

**Source:** https://circuitdigest.com/projects/ai-based-smart-parking-system

**Stack:** ESP32-CAM (AI Thinker board), Raspberry Pi, Tesseract OCR, Plate Recognizer SDK, IR sensors, servo motor (gate).

**Architecture:** IR sensors at the gate trigger the ESP32-CAM to capture an image. The image is sent to Raspberry Pi which runs OCR via Plate Recognizer's ALPR (Automatic License Plate Recognition) SDK. The plate number is cross-checked against a database. If authorized, the servo opens the gate.

**Reporting:** This is an *access control* system as much as a slot monitor — it knows not just that a car is present, but *which* car.

---

## 5. Category B — Computer Vision & Deep Learning Systems {#category-b}

### 5.1 8harath/Car-Parking-Detection (GitHub)

**Source:** https://github.com/8harath/Car-Parking-Detection

**Stack:** Python 3.8+, YOLOv8, OpenCV.

**Features:** Interactive region selection (draw parking slot polygons), real-time detection from video feed or static images, auto-generated analytics reports (charts), CSV output for data analysis.

**Example output:** "Input: Photo of parking lot with 50 spaces → Output: '35 spaces occupied, 15 available' + Visual map + Detailed report with charts."

**Suggested learning path (from README):**
- Week 1: image processing fundamentals, OpenCV
- Week 2: YOLO and object detection theory
- Week 3: Run project, experiment with parameters
- Week 4: Modify and add features
- Week 5: Create presentation/report

---

### 5.2 fabiocarrara/deep-parking (GitHub) — CNRPark Paper Reproduction

**Source:** https://github.com/fabiocarrara/deep-parking

**Paper:** "Deep Learning for Decentralized Parking Lot Occupancy Detection" (Amato et al., Expert Systems with Applications, 2017)

**Stack:** Caffe (PyCaffe), CNRPark dataset (36.6 MB patches, 150×150 px), CNR-EXT dataset (449.5 MB), PKLot dataset (4.6 GB).

**Architecture:** Decentralized CNN per camera — each camera runs its own small model that classifies individual parking space patches as occupied or vacant. No central server needed for inference.

**Cross-domain accuracy (from paper):**
- Trained on SUNNY, tested on OVERCAST: 97%
- Trained on SUNNY, tested on RAINY: 96%
- Trained on SUNNY, tested on PKLot: 85%

**Why this matters:** Training on one dataset and testing on another reveals how well a model generalizes. The 85% on cross-dataset PKLot reveals significant domain shift — motivating the need for fine-tuning on target-environment data.

---

### 5.3 wuyenlin/parking_lot_occupancy_detection (GitHub)

**Source:** https://github.com/wuyenlin/parking_lot_occupancy_detection

**Stack:** PyTorch (reproduces the Amato et al. 2017 paper in PyTorch vs. original Caffe).

**Notable:** Provides a direct comparison of paper-reported accuracy vs. PyTorch re-implementation accuracy, showing PyTorch slightly underperforms Caffe on some conditions (e.g., CNRParkOdd: paper 0.9240 vs. PyTorch 0.9071) — useful for understanding framework-level variance.

---

### 5.4 Real-Time Parking Space Monitoring — YOLO + PySide6 (CEUR-WS Paper 2025)

**Source:** https://ceur-ws.org/Vol-4004/paper1.pdf

**Stack:** Python, YOLO (detection backbone), OpenCV, PySide6 (Qt-based GUI framework), YAML configuration.

**Architecture:** Modular desktop application. ROI editor allows operators to draw and edit parking zone polygons interactively. YAML files persist configuration. Dynamic occupancy map updates in real time from video input. System architecture emphasizes modularity and scalability for integration with smart city infrastructure.

**From paper:** "Validation on test video data confirmed the system's ability to perform accurate and responsive detection under various conditions."

---

### 5.5 Deep Learning-Based Vehicle Parking Occupancy Detection (ResearchGate, 2025)

**Source:** https://www.researchgate.net/publication/393132053

**Paper origin:** Alqalam Journal (Libya), published June 2025.

**Stack:** Pre-trained YOLO + OpenCV, multi-angle surveillance cameras, no additional training.

**Key finding:** Using surveillance video from *four different angles* around the NCB parking area (a real building) substantially improves accuracy vs. single-view detection. Pre-segmented parking slot polygons are initialized manually via OpenCV coordinate overlays.

**Comparison vs. sensor-based methods:** Claims to outperform traditional ultrasonic/IR/geomagnetic sensor methods in *efficiency and accuracy* — the key argument being no per-space hardware needed.

---

### 5.6 MobileNetV3 Parking Occupancy (NCBI/PMC, 2023)

**Source:** https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10490723/

**Stack:** MobileNetV3 with custom attention mechanism (Convolutional Block Attention Module, CBAM) and Blueprint Separable Convolutions (BSConv), trained on CNRPark-EXT + PKLot.

**Key result:** AUC of 0.99 on PKLot, average accuracy of 98.01% on combined datasets — beating CarNet (97.03%) and mAlexNet baselines.

**Why MobileNetV3:** Designed for edge deployment. The authors specifically target *real-time applications* and promise the model is efficient enough to run on embedded hardware.

---

### 5.7 YOLOv7 + Flask Smart Parking (ResearchGate/Springer, 2024–2025)

**Source:** https://link.springer.com/article/10.1007/s10791-025-09789-7

**Stack:** YOLOv7, OpenCV, Flask web interface, SQLite database.

**Architecture:** YOLOv7 detects vehicles in CCTV frames. Flask backend exposes a web interface showing real-time occupancy. SQLite stores historical occupancy records for trend analysis.

**From paper:** Described as suitable for "intelligent and secure critical infrastructure" monitoring.

---

### 5.8 Edge Impulse + ESP32-CAM AI Parking (Medium, 2024)

**Source:** https://medium.com/@anasyunus/building-an-ai-powered-parking-space-detection-system-with-edge-impulse-and-esp32-cam-7066377b8154

**Stack:** ESP32-CAM, Edge Impulse (FOMO — Faster Objects, More Objects model), Roboflow dataset (~200 images).

**Architecture:** Dataset collected and annotated in Roboflow. Uploaded to Edge Impulse for training. FOMO model exported as C++ library for ESP32-CAM deployment. The camera captures images, runs inference locally, and reports occupied/vacant to a Wi-Fi-accessible web interface.

**Key insight:** This is full **edge AI** — no cloud inference needed. The model runs in ~50–100 KB on the ESP32 itself.

---

### 5.9 Smart Parking Space Detection (ResearchGate, 2025) — YOLOv11

**Source:** https://www.researchgate.net/publication/392064716

**Stack:** YOLO11 (Ultralytics, successor to YOLOv8), OpenCV, Node-RED for visualization.

**Key detail:** Even deployed on Raspberry Pi (limited hardware), this system "demonstrates a functional and scalable smart parking solution that is cost-effective and suitable for future urban deployment."

**Comparison included:** YOLOv5s_Ghost vs. standard YOLOv5 variants for parking efficiency — showing Ghost convolution variants improve accuracy with lower compute.

---

### 5.10 Statistical Radar Method for Parking Occupancy (arXiv 1607.06708)

**Source:** https://arxiv.org/pdf/1607.06708

**Approach:** Uses automotive radar (not infrastructure radar) on a probe vehicle to detect on-street parking occupancy while driving.

**Algorithm:** Statistical analysis of radar return amplitude and phase across multiple passes. Distinguishes parked vehicles from traffic-stream vehicles using clustering and Kalman filtering.

**Result (quoted from related work):** Ultrasonic-equipped probe car approach achieved 95% spot count accuracy and >90% occupancy map accuracy over 500 miles of roadside data (Mathur et al.).

---

## 6. Category C — Commercial & Industrial Deployments {#category-c}

### 6.1 MOKO Smart LW009-SM / LW009-SM Pro (LoRaWAN Dual-Mode Sensor)

**Source:** https://www.mokosmart.com/lorawan-wireless-vehicle-detection-sensor-lw009/

**Sensor combination:** Geomagnetic (magnetometer) + Microwave radar.

**Stated accuracy:** >99% (dual-mode redundancy).

**Range:** 500 m – 7 km LoRaWAN.

**Battery life:** 5+ years typical scenarios.

**Deployment markets:** UAE, Spain, Panama (mentioned in product case studies).

**Calibration via Bluetooth:** Parameters (sensitivity thresholds) can be tuned from a smartphone app over BLE.

**Alarms:** Low battery, hardware error, strong magnetic disturbance.

**Architecture:** Sensor → LoRaWAN Gateway → Network Server (decode payload) → Smart Parking Platform (real-time management).

---

### 6.2 Bosch TPS110 (LoRaWAN Parking Lot Sensor)

**Source:** https://www.thethingsnetwork.org/device-repository/devices/bosch/tps110/

**Stack:** Magnetometer + radar, LoRaWAN Class A.

**Key:** Registered in The Things Network device repository with official LoRaWAN device profile. This means it interoperates with any standard TTN/Chirpstack/Helium LoRaWAN network without custom protocol work.

**Context:** Bosch's TPS110 is the hardware underlying the patent family US20220076576A1 / US11721214 / US12437643 discussed in the patents section.

---

### 6.3 PNI PlacePod (Magnetic Sensor for Smart Parking)

**Source:** Referenced in IEEE paper (https://ieeexplore.ieee.org/iel8/11085142/11085448/11085745.pdf)

**Technology:** In-ground magnetometer.

**Cloud integration:** Things Mate application receives data and provides live occupancy dashboards.

**Academic validation:** Used in an IEEE study deploying PlacePods with LoRaWAN gateways, transmitting data via ThingsMate. Preferred for LoRaWAN's low power consumption and longer range vs. alternatives.

---

### 6.4 Nwave NPS310SM Smart Parking Sensor

**Source:** https://www.thethingsnetwork.org/device-repository/devices/nwave/nps310sm/

**Sensors:** Magnetometer + temperature + proximity (three sensors).

**Network:** LoRaWAN (listed in TTN device repo, indicating standards compliance).

**Differentiator:** Proximity sensor added alongside magnetometer — provides additional confirmation layer when magnetic anomaly is ambiguous (e.g., vehicle with very low steel content, or electric vehicles with composite bodies).

---

### 6.5 ParkNode Gen1 (LoRaWAN Smart Parking Sensor)

**Source:** https://www.macnman.com/lorawan/sensors/lorawan-parking-sensor-paknode-gen-one

**Specs:** 99% detection accuracy, up to 10 years battery life, LoRaWAN 500–1000 m, RS485/0-10V/4-20mA/digital input compatibility for industrial automation integration.

**Key feature:** Offline data storage — stores occupancy logs locally during network outages, then syncs when connectivity is restored. Prevents data loss in areas with intermittent LoRa coverage.

**Installation:** Surface mount with glue or bolts, no civil work.

---

### 6.6 Sigfox + Geomagnetic + Ultrasonic Sensor (ChinaIoTDevices)

**Source:** https://www.chinaiotdevices.com/iotdevices/ultrasonic-and-geomagnetic-parking-occupation-detector-with-sigfox/

**Specs:** IP68 waterproofing, ABS housing rated for 5 tonnes, internal battery 25,500 mAh, Bluetooth for configuration, buzzer notification, NB-IoT/LTE-M/EGPRS variants also available.

**Dashboard:** TCP protocol with SDK in Python and JavaScript. Email and SMS notification support.

**Key market:** European smart city projects using Sigfox network infrastructure.

---

### 6.7 SpotHero API — Commercial Parking Marketplace

**Source:** https://github.com/api-evangelist/spothero

**Architecture:** SpotHero aggregates off-street parking facility inventory across North America. Partners (navigation apps, rideshare services, connected cars) access the SpotHero Parking API to search available spots, check real-time availability, create reservations, and manage bookings.

**HeroLab SpotNow:** SpotHero's internal real-time parking server, built in Kotlin, powering instant availability checks and on-demand bookings.

**Note:** SpotHero was acquired by Uber in 2026 to power parking reservation experiences within the Uber app.

---

### 6.8 ParkMe — Deutsche Bahn Open Data Winner

**Source:** https://github.com/janmattfeld/parkme

**Stack:** Node.js, Express, Angular, Deutsche Bahn Parkraum API and Fahrplan API.

**Architecture:** Responsive web app that locates the user, finds nearest DB parking via API, shows route/directions, displays free space count and price, and integrates train departure information.

**Why interesting:** Uses an *existing transit agency API* as the parking data source — rather than deploying its own sensors. This is the reporting/consumer layer built on top of infrastructure that already has occupancy data.

---

## 7. Category D — Cloud, MQTT & Dashboard Backends {#category-d}

### 7.1 MQTT + IBM Watson IoT + Node-RED

**Source:** https://www.researchgate.net/publication/356517151

**Stack:** NodeMCU, ultrasonic sensors, IBM Watson IoT, Node-RED, IFTTT.

**Flow:** NodeMCU measures distance → sends status to IBM Watson IoT broker via MQTT → Node-RED flow receives and displays on dashboard → IFTTT fires email notification if lot is full.

**Key feature:** IFTTT integration means zero backend code needed for notifications — just a webhook trigger.

---

### 7.2 SSGA + MQTT + Firebase Realtime Database

**Source:** https://www.researchgate.net/publication/342124646

**Stack:** Arduino UNO, ultrasonic sensors, NodeMCU (Wi-Fi bridge), Firebase RTDB, MQTT broker (star topology).

**Architecture:** Arduino reads ultrasonic sensors and sends to NodeMCU. NodeMCU publishes to MQTT broker. Firebase subscribes and updates. Web app reads Firebase in real-time. Green = empty slot, Red = occupied slot.

**SSGA (Smart Sensor Gateway Agent):** A middleware process that bridges the MQTT world and Firebase — handling protocol translation and ensuring star topology (if one client drops, others continue).

---

### 7.3 ESP8266 + Adafruit IO + Node-RED (IoTDesignPro)

**Source:** https://iotdesignpro.com/projects/iot-based-smart-parking-using-esp8266

**Stack:** ESP8266, servo motors (gates), ultrasonic sensors, NTPClient (time tracking), Adafruit MQTT, Adafruit IO dashboard.

**Code detail (from source):**
```cpp
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"
#define MQTT_SERV "io.adafruit.com"
#define MQTT_PORT 1883
```

**Manual gate control:** Dashboard includes buttons to manually open entry/exit gates, overriding the sensor-triggered automation.

---

### 7.4 Node-RED + Metro Station Parking (OpenSourceForU)

**Source:** https://www.opensourceforu.com/2022/06/build-a-smart-parking-system-for-a-metro-station/

**Approach:** Node-RED flows handling HTTP endpoints for a metro parking application. Login/submission forms built directly in Node-RED using http-in, function, template, and http-response nodes. A lightweight solution for facilities that want browser-based management without deploying a separate web framework.

---

### 7.5 Tinkercad + ThingSpeak (Embedded System Design Course)

**Source:** GitHub topic — smart-parking-system

**Approach:** Hardware *simulated* in Tinkercad (browser-based Arduino simulator). Data pushed to ThingSpeak (MATLAB analytics IoT platform) for visualization. Useful for coursework where physical hardware isn't available — demonstrates the full data pipeline in simulation.

---

### 7.6 LoRa Dev-Boards + GPS + MQTT (GitHub topic)

**Source:** GitHub topic — smart-parking-system

**Stack:** LoRa development boards, GPS module, MQTT.

**Unique aspect:** The GPS module geo-tags each sensor's location, allowing a mapping layer to display *where* open spaces are, not just *that* spaces are open. Particularly relevant for on-street parking where the spatial component matters.

---

## 8. Category E — Patents {#patents}

### 8.1 US11721214 / US12437643 — Dual-Sensor Parking Sensor Device (LoRaWAN)

**USPTO PDF:** https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11721214
**Google Patents:** https://patents.google.com/patent/US20220076576A1/en

**Assignee:** (Bosch-related — the TPS110 product family)

**Claims summary:** A parking sensor device with magnetometer + radar, connected via LoRaWAN. The magnetometer triggers a wake from low-power state; radar confirms. Combined occupancy determination is transmitted to a LoRaWAN gateway → network server → cloud server → client devices (web interface, smartphone app). Battery life up to 10 years. Cost ~$50 manufacturing.

**Key technical claim:** The device can adjust magnetometer detection thresholds based on measured ambient magnetic noise — self-calibrating to local magnetic environment, which solves the interference problem near ferrous structures.

---

### 8.2 US11322028 — Radar-Augmentation of Parking Space Sensors

**USPTO PDF:** https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11322028

**Priority date:** November 30, 2018.

**Core claim:** A system where radar-based vehicle detectors are placed strategically to cover *multiple* parking spaces each, augmenting cheaper per-space magnetic sensors. A simulation determines which parking spaces are insufficiently covered by radar to meet an accuracy threshold, so operators know where additional sensors are needed.

---

### 8.3 US10332398 — Smart Parking Facility Management (Three-Axis Magnetometers)

**USPTO PDF:** https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10332398

**Claims:** Each parking space has a sensor with a unique ID. Detecting a vehicle → marks that specific space as occupied. Sensors include three-axis magnetometers, but also allows ultrasound, infrared, and stress/strain sensors. Customer interface displays real-time traffic patterns, occupied/unoccupied status, exit/entry locations, and the location of the customer's own vehicle.

---

### 8.4 US11182598B2 — Smart Area Monitoring with Artificial Intelligence (Google Patents)

**Source:** https://patents.google.com/patent/US11182598B2/en

**Innovation:** Camera-based system that goes beyond occupancy detection to detect anomalies: vehicles going in the wrong direction, speeding, stalled vehicles, abandoned vehicles in aisles.

**Key claim regarding non-imaging sensors:** Ceiling-mounted colored light indicators show occupancy of each parking spot in real time. However, patent argues that non-imaging sensors (magnetometers) can't detect non-metallic objects, can't communicate to drivers not physically present, and can't distinguish a poorly-parked vehicle. Cameras solve all three.

---

### 8.5 US7893847 — Real-Time Detection of Parking Space Availability (Symbol-Based Vision)

**USPTO PDF:** https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7893847

**Approach:** Parking spaces are marked with symbols. A camera detects whether a symbol is at least partially obstructed — if obstructed, space is occupied. Works even in low-resolution imagery where counting vehicles directly is difficult.

---

### 8.6 US12067878 — Crowd Sourced Real-Time Parking Space Detection

**USPTO PDF:** https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12067878

**Innovation:** Vehicles equipped with on-board camera systems run vision-based analytics as they drive. Each vehicle extracts *metadata* (space available/occupied) without uploading video. The metadata is crowd-sourced to a central cloud that builds an up-to-date occupancy map.

**Key features claimed:** Guides driver to free space; rewards users for holding spaces for other drivers; plans errands around parking availability; hands off parking search to cloud to improve road safety by reducing distracted driving.

---

### 8.7 US20140172519A1 / US9330303B2 — Controlling Use of Parking Spaces (Cameras + Smart Sensors)

**Source:** https://patents.google.com/patent/US20140172519
**Source:** https://patents.google.com/patent/US9330303B2/en

**Approach:** Tracks vehicles via both camera and on-vehicle GPS sensors. Determines *exactly* when a vehicle arrived at and departed from a parking space. Enables precise time-of-use billing and enforcement.

**USPC classification includes:** G08G1/0175 — detecting vehicles via photography; G08G1/123 — scheduled vehicle position indication.

---

### 8.8 US10263461 — Smart DC Microgrid Parking Structures (Power Line Communications)

**USPTO PDF:** https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10263461

**Unique angle:** Combines smart parking occupancy with EV charging infrastructure. "Puck sensors" (battery-powered, embedded in parking floor under each spot) communicate vehicle occupancy data to an Active Parking Lot Management Backend. The backend also manages the DC microgrid for EV charging allocation.

---

### 8.9 US10663583 — Parking Assistance System / Ultrasonic CA-CFAR Algorithm

**USPTO PDF:** https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10663583

**Key technical contribution:** When sensing in a second (extended) sensing area, applies a CA-CFAR (Cell-Averaging Constant False Alarm Rate) algorithm to set adaptive thresholds per section of the sensing area. Echo is validated by confirming both width and peak value fall within preset ranges. At vehicle stop, all echoes across multiple ultrasonic pulses must be within a preset distance — eliminates transient false detections.

---

## 9. Research Datasets & Benchmarks {#datasets}

### 9.1 PKLot Dataset

**Origin:** Federal University of Paraná (UFPR) and Pontifical Catholic University of Paraná (PUCPR), Curitiba, Brazil.

**Size:** ~700,000 manually labeled parking space images; 12,417 images total; 168 parking slots.

**Subsets:** UFPR04 (camera at UFPR 4th floor), UFPR05 (5th floor), PUCPR (10th floor administration building).

**Conditions:** SUNNY, OVERCAST, RAINY.

**Collection period:** September 2012 – April 2013 (images captured every 5 minutes).

**Resolution:** 1280×720 pixels, JPEG.

**Access:** Visit PKLot webpage (linked from fabiocarrara/deep-parking).

**Standard use:** Train/test splits across weather conditions and parking lots to measure domain generalization.

---

### 9.2 CNRPark / CNRPark-EXT Dataset

**Origin:** National Research Council (CNR), Pisa, Italy.

**Size:** CNRPark: 12,584 images (CNRPark-A: 6,171; CNRPark-B: 6,413). CNR-EXT: ~160,000 annotated spaces from 9 cameras, November 2015 – February 2016.

**Slots:** 164 parking slots, 9 different camera viewpoints.

**Conditions:** SUNNY, RAINY, OVERCAST. Includes partial occlusion by trees and neighboring car shadows.

**Download:**
- `http://cnrpark.it/dataset/CNRPark-Patches-150x150.zip` (36.6 MB)
- `http://cnrpark.it/dataset/CNR-EXT-Patches-150x150.zip` (449.5 MB)

---

### 9.3 NDISPark (Night and Day Instance Segmented Park Dataset)

**Size:** 259 images, 7 cameras.

**Unique challenge:** Includes night-time images, lateral (side-on) camera views, and partial occlusions from lampposts and trees. More realistic for street-level deployments than overhead PKLot.

---

### 9.4 BarryStreet Dataset

**Source:** Mentioned in arXiv:2309.16495 comparison study.

**Notable for:** Providing annotations of parking spot locations with binary labels — used alongside PKLot, CNRPark, and NDISPark to benchmark model generalization across wide-ranging conditions.

---

## 10. Academic Papers & Literature {#papers}

### Key Papers (chronological)

| Year | Title | Key Contribution | Source |
|------|-------|-----------------|--------|
| 2014 | Automated Parking Surveys from a LIDAR Equipped Vehicle | Mobile LiDAR survey of on-street parking; 29 trips over 4 years | ceg.osu.edu / ResearchGate |
| 2017 | Deep Learning for Decentralized Parking Lot Occupancy Detection (Amato et al.) | CNRPark dataset + decentralized CNN per camera; benchmarked cross-domain | Expert Systems with Applications |
| 2020 | Smart Parking Solutions Architecture Based on LoRaWAN and Kubernetes | End-to-end architecture: magnetometer sensors → LoRaWAN → Kubernetes-managed backend | MDPI Applied Sciences 10(13):4674 |
| 2020 | Smart Parking Sensors: State of the Art and Performance Evaluation | Comparison of photodiode / ultrasound / IR / magnetometer; power analysis of LoRa / Sigfox / NB-IoT | ScienceDirect (Journal of Cleaner Production) |
| 2020 | Implementation of a Magnetometer-Based Vehicle Detection for Smart Parking | In-depth analysis of real-scenario sensor performance; lowest power = LoRa | ResearchGate |
| 2022 | Privacy Leakage of LoRaWAN Smart Parking Occupancy Sensors | Traffic analysis attack on LoRaWAN parking sensors; reveals presence/absence patterns | ScienceDirect (Future Generation Computer Systems) |
| 2022 | Smart Parking System Using MQTT and IBM Cloud | NodeMCU + MQTT + Node-RED + IFTTT integration | JPhCS2115 (IOP Publishing) |
| 2022 | IoT-SPMS-LoRaWAN: Internet of Things Enabled Parking Using LoRaWAN | Full system with Arduino + triaxial magnetometer + waterproof ultrasonic + AllThingsTalk GUI | ScienceDirect |
| 2022 | Smart Parking System Based on IoT Architecture and Intelligent Sensors | 10 in-ground PlacePod sensors at University of Oulu; 5G network backhaul; REST API | IARIA SMART 2022 |
| 2023 | Parking Lot Occupancy Detection with Improved MobileNetV3 | CBAM attention + blueprint separable convolutions; 98.01% on CNRPark-EXT + PKLot | NCBI PMC |
| 2023 | Automatic Vision-Based Parking Slot Detection and Occupancy Classification | APSD-OC algorithm on PKLot + CNRPark-EXT | arXiv:2308.08192 |
| 2024 | Deep Learning Enabled Real Time Parking Monitoring Using YOLOv7 | YOLOv7 + Flask + SQLite; critical infrastructure focus | Discover Computing (Springer) |
| 2024 | IoT-Driven Smart Parking with LoRaWAN and PNI PlacePod | PNI PlacePod magnetic sensor + ThingsMate + LoRaWAN | IEEE Xplore |
| 2025 | Real-Time Parking Space Monitoring Based on Computer Vision | YOLO + PySide6 GUI + YAML config; modular desktop app | CEUR-WS Vol-4004 (MoMLeT-2025) |
| 2025 | Deep Learning-Based Vehicle Parking Occupancy Detection (NCB Building) | Pre-trained YOLO + OpenCV; four camera angles; no retraining | Alqalam Journal / ResearchGate |
| 2025 | Real-Time Smart Parking System Using YOLO11 and OpenCV | YOLO11 + Node-RED; Raspberry Pi deployment; YOLOv5s_Ghost comparison | ResearchGate |
| 2025 | Smart Parking Space Detection Under Hazy Conditions (arXiv:2201.05858) | CNN approach robust to haze; tested on CNRPark, CNRPark-EXT, PKLot | arXiv |

---

## 11. Comparative Analysis of Approaches {#comparison}

### 11.1 Detection Accuracy

| Method | Typical Accuracy | Conditions |
|--------|-----------------|-----------|
| Dual-mode magnetometer + radar (commercial) | >99% | All weather, outdoor |
| YOLO-based computer vision | 95–99% | Well-lit, moderate weather |
| Deep CNN (MobileNetV3 + CBAM) on PKLot | 98.01% | Mixed weather datasets |
| Single magnetometer | 90–97% | Degrades near ferrous interference |
| Ultrasonic (single sensor) | 85–95% | Degrades with temperature, rain, moving objects |
| IR sensor | 80–95% | Poor in direct sunlight, rain |
| Mobile LiDAR survey vehicle | >90% occupancy map accuracy | On-street parallel parking |

### 11.2 Cost Profile

| Approach | Per-Space Cost | Infrastructure Cost |
|----------|---------------|-------------------|
| IR/Ultrasonic + ESP32 (DIY) | ~$3–10 | Near-zero (Wi-Fi existing) |
| LoRaWAN magnetometer+radar (commercial) | ~$50–80 | LoRaWAN gateway $200–$2000+ |
| NB-IoT commercial sensor | ~$60–100 | Existing cellular (SIM cost) |
| Camera-based (1 camera per N spaces) | $0–5 per space | Camera $100–500 per 20–50 spaces |
| LiDAR fixed installation | $500–2000/unit | High |

### 11.3 Battery Life

| Sensor Type | Typical Battery Life |
|-------------|---------------------|
| LoRaWAN magnetometer+radar (commercial) | 5–10 years |
| NB-IoT sensor | 2–5 years |
| Sigfox sensor | 3–7 years |
| ESP32 Wi-Fi sensor | Days to weeks (needs charging or mains) |
| Camera system | Mains power required |

### 11.4 Reporting Mechanisms Found Across Implementations

| Reporting Type | Examples Found |
|---------------|----------------|
| Local LED display | HC-SR04 + Arduino/ESP32 + LED strip (Hackaday.io) |
| Local LCD display | ESP32 + IR sensors + I2C LCD (Cytron tutorial) |
| Local web server | ESP32 Async Web Server on local network (ArduinoYard) |
| MQTT → cloud dashboard | NodeMCU → Adafruit IO / IBM Watson IoT / HiveMQ |
| Firebase Realtime DB | ESP8266 → Firebase → browser UI (green/red slot display) |
| LoRaWAN → TTN → application | MOKO/Bosch/PNI PlacePod → ThingsMate/custom platform |
| REST API | Spring Boot backend; Flask; Node.js/Express |
| Mobile app | Flutter (SmartPark CarlosFULLHD), PhoneGap (Dipal018), Android/iOS |
| SMS notification | Twilio (Dipal018 time-limit alerts) |
| Email notification | Node-RED + IFTTT |
| LED ceiling indicators | Commercial smart garage (US11182598B2 patent) |
| Navigation app integration | SpotHero API, Deutsche Bahn ParkMe |
| Crowd-sourced map | US12067878 patent |

---

## 12. Source Index {#sources}

### GitHub Repositories

| Repo | URL | Tech Stack |
|------|-----|-----------|
| aaryaapg/Smart-Parking | https://github.com/aaryaapg/Smart-Parking | STM32, IR, Ultrasonic |
| RahulN25/Smart-Parking-System | https://github.com/RahulN25/Smart-Parking-System | Ultrasonic, IR, Camera, UPI payments |
| vishnubv944/smartParkingSystem | https://github.com/vishnubv944/smartParkingSystem | NodeMCU, IR, AWS IoT |
| Dipal018/Smart_Parking | https://github.com/Dipal018/Smart_Parking | ESP8266, REST API, Twilio, PhoneGap |
| CarlosFULLHD/iot_garaje_inteligente | https://github.com/CarlosFULLHD/iot_garaje_inteligente | Pico W, Spring Boot, Flutter, Supabase |
| 8harath/Car-Parking-Detection | https://github.com/8harath/Car-Parking-Detection | YOLOv8, OpenCV, Python |
| fabiocarrara/deep-parking | https://github.com/fabiocarrara/deep-parking | Caffe, CNRPark, PKLot |
| wuyenlin/parking_lot_occupancy_detection | https://github.com/wuyenlin/parking_lot_occupancy_detection | PyTorch, CNRPark |
| aswin-sreekumar/Smart-parking-system | https://github.com/aswin-sreekumar/Smart-parking-system | ESP32-CAM, Raspberry Pi, Node.js, IoU |
| prince61299/Smart-Car-Parking-using-ESP32 | https://github.com/prince61299/Smart-Car-Parking-using-ESP32 | ESP32, IR, Arduino Cloud |
| janmattfeld/parkme | https://github.com/janmattfeld/parkme | Node.js, Express, Angular, DB API |
| api-evangelist/spothero | https://github.com/api-evangelist/spothero | SpotHero API documentation |

### Patents

| Patent | URL | Key Topic |
|--------|-----|-----------|
| US11721214 | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11721214 | Magnetometer+radar LoRaWAN sensor |
| US12437643 | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12437643 | Magnetometer+radar LoRaWAN (continuation) |
| US20220076576A1 | https://patents.google.com/patent/US20220076576A1/en | Same family (Google Patents) |
| US11322028 | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11322028 | Radar-augmentation of parking sensors |
| US10991249 | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10991249 | Radar-augmentation (parent) |
| US10332398 | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10332398 | Smart parking facility, 3-axis magnetometers |
| US11182598B2 | https://patents.google.com/patent/US11182598B2/en | AI-based area monitoring, ceiling LEDs |
| US7893847 | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7893847 | Symbol-based camera occupancy detection |
| US12067878 | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12067878 | Crowdsourced real-time parking detection |
| US20140172519A1 | https://patents.google.com/patent/US20140172519 | Camera + vehicle GPS tracking |
| US9330303B2 | https://patents.google.com/patent/US9330303B2/en | Smart sensor network, unique vehicle IDs |
| US10263461 | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10263461 | DC microgrid + EV charging + puck sensors |
| US10663583 | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10663583 | Ultrasonic CA-CFAR false positive reduction |
| US9696420 | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9696420 | Active park assist, radar+ultrasonic fusion |

### Academic Papers & Research

| Title | URL |
|-------|-----|
| LoRaWAN Smart Parking (MDPI Applied Sciences) | https://www.mdpi.com/2076-3417/10/13/4674 |
| Smart Parking Sensors State of Art (ScienceDirect) | https://www.sciencedirect.com/science/article/abs/pii/S0959652620312282 |
| Privacy Leakage LoRaWAN (ScienceDirect) | https://www.sciencedirect.com/science/article/abs/pii/S0167739X22002680 |
| IoT-SPMS-LoRaWAN Full System (ScienceDirect) | https://www.sciencedirect.com/science/article/pii/S2667345223000494 |
| Smart Parking System IoT Architecture Oulu (IARIA) | https://personales.upv.es/thinkmind/dl/conferences/smart/smart_2022/smart_2022_1_10_40025.pdf |
| MobileNetV3 Parking Occupancy (NCBI/PMC) | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10490723/ |
| Real-Time Parking Monitoring YOLO+PySide6 (CEUR-WS 2025) | https://ceur-ws.org/Vol-4004/paper1.pdf |
| Deep Learning Parking Occupancy NCB (ResearchGate 2025) | https://www.researchgate.net/publication/393132053 |
| YOLO11 Smart Parking (ResearchGate 2025) | https://www.researchgate.net/publication/392064716 |
| YOLOv7 Critical Infrastructure (Springer) | https://link.springer.com/article/10.1007/s10791-025-09789-7 |
| Parking Under Hazy Conditions CNN (arXiv) | https://arxiv.org/pdf/2201.05858 |
| Statistical Radar Parking Occupancy (arXiv) | https://arxiv.org/pdf/1607.06708 |
| Automatic Vision-Based Parking Slot Detection (arXiv) | https://arxiv.org/pdf/2308.08192 |
| Deep Single Models vs Ensembles (arXiv) | https://arxiv.org/pdf/2309.16495 |
| Magnetometer Vehicle Detection (ResearchGate) | https://www.researchgate.net/publication/344103475 |
| IoT-Driven Smart Parking LoRaWAN PNI (IEEE Xplore) | https://ieeexplore.ieee.org/iel8/11085142/11085448/11085745.pdf |
| LiDAR SLAM Parking (PMC) | https://pmc.ncbi.nlm.nih.gov/articles/PMC6864444/ |
| Automated LiDAR Parking Surveys (Ohio State) | https://ceg.osu.edu/sites/default/files/2022-06/LidarPark.pdf |
| MQTT IBM Watson IoT Smart Parking | https://www.researchgate.net/publication/356517151 |
| SSGA MQTT Firebase Smart Parking | https://www.researchgate.net/publication/342124646 |

### Tutorials, DIY Projects & Maker Sources

| Source | URL |
|--------|-----|
| ESP32-Based Precision Parking Assist (Hackaday.io) | https://hackaday.io/project/177714-esp32-based-precision-parking-assist |
| Arduino Nano ESP32 Garage LiDAR (Arduino Project Hub) | https://projecthub.arduino.cc/noah_barkol/arduino-nano-esp32-fully-automatic-garage-ceiling-parking-assistant-79cd6c |
| ESP32 Smart Parking Detection (Hackster.io) | https://www.hackster.io/techgyanset/esp32-smart-parking-detection-system-d68660 |
| Parking Sensor LED Boxes (Hackster.io) | https://www.hackster.io/MrBancroft/parking-sensor-67e3f0 |
| ALPR Parking System Raspberry Pi (Hackster.io) | https://www.hackster.io/codrinsideas/diy-raspberry-pi-alpr-parking-sys-with-platerecognizer-s-sdk-adcf07 |
| ESP32 Parking Web Server (ArduinoYard) | https://arduinoyard.com/esp32-parking-system/ |
| AI Parking ESP32-CAM (CircuitDigest) | https://circuitdigest.com/projects/ai-based-smart-parking-system |
| Edge Impulse + ESP32-CAM AI (Medium) | https://medium.com/@anasyunus/building-an-ai-powered-parking-space-detection-system-with-edge-impulse-and-esp32-cam-7066377b8154 |
| Car Parking Detection Edge Impulse (DigiKey) | https://www.digikey.com/en/maker/projects/car-parking-detection-system-using-edge-impulse/0fcb63b013e240e5bef7049ed1027332 |
| IoT Smart Parking NodeMCU (IoTDesignPro) | https://iotdesignpro.com/projects/iot-based-smart-parking-using-esp8266 |
| Node-RED Metro Parking (OpenSourceForU) | https://www.opensourceforu.com/2022/06/build-a-smart-parking-system-for-a-metro-station/ |
| Firebase Portable Smart Parking (IJRASET) | https://www.ijraset.com/research-paper/portable-smart-parking-system-using-firebase |
| ESP32 Smart Parking System (Cytron) | https://www.cytron.io/tutorial/esp32-smart-parking-system |

### Commercial Product Sources

| Product | URL |
|---------|-----|
| MOKO LW009-SM LoRaWAN Sensor | https://www.mokosmart.com/lorawan-wireless-vehicle-detection-sensor-lw009/ |
| MOKO LW009-SM Geomagnetic Info | https://www.mokosmart.com/lorawan-geomagnetic-parking-sensor-lw005-ps/ |
| Bosch TPS110 (TTN Device Repo) | https://www.thethingsnetwork.org/device-repository/devices/bosch/tps110/ |
| Nwave NPS310SM (TTN Device Repo) | https://www.thethingsnetwork.org/device-repository/devices/nwave/nps310sm/ |
| ParkNode Gen1 LoRaWAN Sensor | https://www.macnman.com/lorawan/sensors/lorawan-parking-sensor-paknode-gen-one |
| Sigfox Ultrasonic+Geomagnetic Sensor | https://www.chinaiotdevices.com/iotdevices/ultrasonic-and-geomagnetic-parking-occupation-detector-with-sigfox/ |

---

*Report compiled June 2026. Sources retrieved and cross-referenced from USPTO, Google Patents, GitHub, IEEE Xplore, ResearchGate, arXiv, NCBI/PMC, Hackster.io, Hackaday.io, Arduino Project Hub, and commercial vendor documentation.*# Parking-Sensor-Project
