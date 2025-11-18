/*
 * Vader AI ESP32 Firmware
 *
 * Darth Vader Voice Assistant - ESP32 Client
 *
 * Hardware Requirements:
 * - ESP32 Development Board
 * - I2S Microphone (e.g., INMP441)
 * - I2S Amplifier + Speaker (e.g., MAX98357A)
 *
 * Pin Configuration:
 * Microphone (I2S):
 *   - SCK: GPIO 26
 *   - WS:  GPIO 25
 *   - SD:  GPIO 33
 *
 * Speaker (I2S):
 *   - BCLK: GPIO 14
 *   - LRC:  GPIO 15
 *   - DIN:  GPIO 22
 */

#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include <driver/i2s.h>

// WiFi Configuration
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// Server Configuration
const char* SERVER_HOST = "192.168.1.100";  // Replace with your server IP
const int SERVER_PORT = 8000;
const char* DEVICE_ID = "ESP32_001";
const char* API_KEY = "change-this-esp32-api-key";

// I2S Microphone Configuration
#define I2S_MIC_PORT I2S_NUM_0
#define I2S_MIC_SCK 26
#define I2S_MIC_WS 25
#define I2S_MIC_SD 33
#define I2S_MIC_SAMPLE_RATE 16000
#define I2S_MIC_BUFFER_SIZE 1024

// I2S Speaker Configuration
#define I2S_SPK_PORT I2S_NUM_1
#define I2S_SPK_BCLK 14
#define I2S_SPK_LRC 15
#define I2S_SPK_DIN 22
#define I2S_SPK_SAMPLE_RATE 44100

// Button Configuration
#define BUTTON_PIN 32
#define LED_PIN 2

// WebSocket
WebSocketsClient webSocket;

// State
bool isConnected = false;
bool isRecording = false;
bool isProcessing = false;

// Audio buffers
int16_t micBuffer[I2S_MIC_BUFFER_SIZE];
size_t bytesRead = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("\n\nVader AI ESP32 Client");
  Serial.println("=====================");

  // Initialize pins
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // Initialize I2S for microphone
  initMicrophone();

  // Initialize I2S for speaker
  initSpeaker();

  // Connect to WiFi
  connectWiFi();

  // Connect to WebSocket
  connectWebSocket();
}

void loop() {
  webSocket.loop();

  // Check button press
  if (digitalRead(BUTTON_PIN) == LOW && !isRecording && !isProcessing && isConnected) {
    delay(50); // Debounce
    if (digitalRead(BUTTON_PIN) == LOW) {
      startRecording();
      while (digitalRead(BUTTON_PIN) == LOW) {
        delay(10);
      }
      stopRecording();
    }
  }
}

void initMicrophone() {
  Serial.println("Initializing microphone...");

  i2s_config_t i2s_mic_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = I2S_MIC_SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 4,
    .dma_buf_len = 1024,
    .use_apll = false,
    .tx_desc_auto_clear = false,
    .fixed_mclk = 0
  };

  i2s_pin_config_t pin_mic_config = {
    .bck_io_num = I2S_MIC_SCK,
    .ws_io_num = I2S_MIC_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_MIC_SD
  };

  i2s_driver_install(I2S_MIC_PORT, &i2s_mic_config, 0, NULL);
  i2s_set_pin(I2S_MIC_PORT, &pin_mic_config);
  i2s_zero_dma_buffer(I2S_MIC_PORT);

  Serial.println("Microphone initialized");
}

void initSpeaker() {
  Serial.println("Initializing speaker...");

  i2s_config_t i2s_spk_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX),
    .sample_rate = I2S_SPK_SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 4,
    .dma_buf_len = 1024,
    .use_apll = false,
    .tx_desc_auto_clear = true,
    .fixed_mclk = 0
  };

  i2s_pin_config_t pin_spk_config = {
    .bck_io_num = I2S_SPK_BCLK,
    .ws_io_num = I2S_SPK_LRC,
    .data_out_num = I2S_SPK_DIN,
    .data_in_num = I2S_PIN_NO_CHANGE
  };

  i2s_driver_install(I2S_SPK_PORT, &i2s_spk_config, 0, NULL);
  i2s_set_pin(I2S_SPK_PORT, &pin_spk_config);
  i2s_zero_dma_buffer(I2S_SPK_PORT);

  Serial.println("Speaker initialized");
}

void connectWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    digitalWrite(LED_PIN, HIGH);
  } else {
    Serial.println("\nWiFi connection failed!");
    digitalWrite(LED_PIN, LOW);
  }
}

void connectWebSocket() {
  Serial.println("Connecting to Vader AI server...");

  String path = "/ws/esp32/" + String(DEVICE_ID) + "?api_key=" + String(API_KEY);

  webSocket.begin(SERVER_HOST, SERVER_PORT, path);
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000);
}

void webSocketEvent(WStype_t type, uint8_t* payload, size_t length) {
  switch (type) {
    case WStype_DISCONNECTED:
      Serial.println("WebSocket Disconnected");
      isConnected = false;
      digitalWrite(LED_PIN, LOW);
      break;

    case WStype_CONNECTED:
      Serial.println("WebSocket Connected!");
      isConnected = true;
      digitalWrite(LED_PIN, HIGH);
      sendStatus();
      break;

    case WStype_TEXT: {
      Serial.printf("Received text: %s\n", payload);

      StaticJsonDocument<512> doc;
      DeserializationError error = deserializeJson(doc, payload);

      if (!error) {
        const char* msgType = doc["type"];

        if (strcmp(msgType, "connected") == 0) {
          Serial.println("Server confirmed connection");
        } else if (strcmp(msgType, "status") == 0) {
          Serial.println("Processing command...");
          isProcessing = true;
          blinkLED(3);
        } else if (strcmp(msgType, "transcription") == 0) {
          const char* text = doc["text"];
          Serial.print("You said: ");
          Serial.println(text);
        } else if (strcmp(msgType, "response") == 0) {
          const char* text = doc["text"];
          Serial.print("Vader: ");
          Serial.println(text);
        } else if (strcmp(msgType, "complete") == 0) {
          Serial.println("Processing complete");
          isProcessing = false;
        } else if (strcmp(msgType, "error") == 0) {
          const char* message = doc["message"];
          Serial.print("Error: ");
          Serial.println(message);
          isProcessing = false;
        }
      }
      break;
    }

    case WStype_BIN:
      Serial.printf("Received audio: %u bytes\n", length);
      playAudio(payload, length);
      break;

    case WStype_ERROR:
      Serial.println("WebSocket Error");
      break;

    case WStype_PING:
      Serial.println("WebSocket Ping");
      break;

    case WStype_PONG:
      Serial.println("WebSocket Pong");
      break;
  }
}

void startRecording() {
  Serial.println("Recording started...");
  isRecording = true;
  digitalWrite(LED_PIN, HIGH);

  // Clear buffer
  i2s_zero_dma_buffer(I2S_MIC_PORT);

  // Start recording for 3 seconds
  unsigned long startTime = millis();
  const unsigned long recordDuration = 3000; // 3 seconds

  while (millis() - startTime < recordDuration) {
    size_t bytesRead = 0;
    i2s_read(I2S_MIC_PORT, micBuffer, sizeof(micBuffer), &bytesRead, portMAX_DELAY);

    if (bytesRead > 0) {
      // Send audio data via WebSocket
      webSocket.sendBIN((uint8_t*)micBuffer, bytesRead);
    }

    // Blink LED while recording
    if ((millis() / 200) % 2 == 0) {
      digitalWrite(LED_PIN, HIGH);
    } else {
      digitalWrite(LED_PIN, LOW);
    }
  }
}

void stopRecording() {
  Serial.println("Recording stopped");
  isRecording = false;
  digitalWrite(LED_PIN, isConnected ? HIGH : LOW);
}

void playAudio(uint8_t* audioData, size_t length) {
  Serial.println("Playing Vader's response...");

  size_t bytesWritten = 0;
  i2s_write(I2S_SPK_PORT, audioData, length, &bytesWritten, portMAX_DELAY);

  Serial.printf("Played %u bytes\n", bytesWritten);
}

void sendStatus() {
  StaticJsonDocument<256> doc;
  doc["type"] = "status";
  doc["firmware_version"] = "1.0.0";
  doc["ip_address"] = WiFi.localIP().toString();

  String output;
  serializeJson(doc, output);
  webSocket.sendTXT(output);
}

void blinkLED(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(LED_PIN, LOW);
    delay(100);
    digitalWrite(LED_PIN, HIGH);
    delay(100);
  }
}
