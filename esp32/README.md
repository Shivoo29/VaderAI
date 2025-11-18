# ESP32 Firmware for Vader AI

This directory contains the Arduino firmware for ESP32 to work with Vader AI Voice Assistant.

## Hardware Requirements

1. **ESP32 Development Board** (ESP32-WROOM or similar)
2. **I2S Microphone** (e.g., INMP441)
3. **I2S Amplifier + Speaker** (e.g., MAX98357A + 4Ω speaker)
4. **Push Button** (for voice activation)
5. **LED** (status indicator)
6. **Breadboard and jumper wires**

## Pin Configuration

### Microphone (I2S INMP441)
- **SCK (Clock)**: GPIO 26
- **WS (Word Select)**: GPIO 25
- **SD (Serial Data)**: GPIO 33
- **VDD**: 3.3V
- **GND**: GND

### Speaker (I2S MAX98357A)
- **BCLK (Bit Clock)**: GPIO 14
- **LRC (Word Select)**: GPIO 15
- **DIN (Data In)**: GPIO 22
- **VDD**: 5V (from USB)
- **GND**: GND

### Button and LED
- **Button**: GPIO 32 (with pull-up resistor)
- **LED**: GPIO 2 (built-in LED on most ESP32 boards)

## Installation

1. **Install Arduino IDE** (version 1.8.19 or newer)

2. **Add ESP32 Board Support**:
   - Open Arduino IDE
   - Go to File → Preferences
   - Add this URL to "Additional Board Manager URLs":
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Go to Tools → Board → Board Manager
   - Search for "esp32" and install "esp32 by Espressif Systems"

3. **Install Required Libraries**:
   - Go to Sketch → Include Library → Manage Libraries
   - Install:
     - `WebSockets` by Markus Sattler
     - `ArduinoJson` by Benoit Blanchon

4. **Configure the Code**:
   - Open `vader_ai_esp32.ino` in Arduino IDE
   - Update these settings:
     ```cpp
     const char* WIFI_SSID = "YOUR_WIFI_SSID";
     const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
     const char* SERVER_HOST = "192.168.1.100";  // Your server IP
     const char* API_KEY = "change-this-esp32-api-key";  // Match backend API key
     ```

5. **Upload to ESP32**:
   - Connect ESP32 via USB
   - Select: Tools → Board → ESP32 Dev Module
   - Select: Tools → Port → (your ESP32 port)
   - Click Upload

## Usage

1. Power on the ESP32
2. Wait for WiFi connection (LED will turn solid when connected)
3. Press and hold the button to record your command
4. Release the button to send the recording
5. Wait for Vader's response (LED blinks during processing)
6. Vader's voice will play through the speaker

## Troubleshooting

### WiFi Won't Connect
- Check SSID and password
- Ensure 2.4GHz WiFi (ESP32 doesn't support 5GHz)
- Move closer to router

### No Audio Recorded
- Check I2S microphone wiring
- Verify 3.3V power to microphone
- Check serial monitor for error messages

### No Audio Playback
- Check I2S amplifier wiring
- Verify speaker connections
- Ensure 5V power to amplifier
- Check volume (some amplifiers have gain control)

### WebSocket Connection Fails
- Verify server is running
- Check SERVER_HOST and SERVER_PORT
- Verify API_KEY matches backend configuration
- Check firewall settings

## Customization

### Change Recording Duration
Edit this line in `vader_ai_esp32.ino`:
```cpp
const unsigned long recordDuration = 3000; // 3 seconds
```

### Change Sample Rate
Edit microphone configuration:
```cpp
#define I2S_MIC_SAMPLE_RATE 16000  // Change to 8000 or 24000
```

### Add More Buttons
You can add additional buttons for:
- Volume control
- Pre-defined commands
- Emergency stop

## Schematic

```
ESP32                INMP441 (Microphone)
GPIO 26  ----------- SCK
GPIO 25  ----------- WS
GPIO 33  ----------- SD
3.3V     ----------- VDD
GND      ----------- GND

ESP32                MAX98357A (Amplifier)
GPIO 14  ----------- BCLK
GPIO 15  ----------- LRC
GPIO 22  ----------- DIN
5V       ----------- VIN
GND      ----------- GND

MAX98357A            Speaker
+ (OUT)  ----------- + (Speaker)
- (OUT)  ----------- - (Speaker)

ESP32                Button & LED
GPIO 32  ----------- Button (other side to GND)
GPIO 2   ----------- LED Anode (Cathode to GND via 220Ω resistor)
```

## License

MIT License - See main project LICENSE file
