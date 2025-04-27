ESP-8266
#include <ESP8266WiFi.h>  // Wi-Fi library ko include karo

const char* ssid = "V2027";    // WiFi SSID
const char* password = "pppppppp"; // WiFi Password

WiFiServer server(80); // HTTP server create karo (port 80)

const int buttonPin = D1; // Joystick button ko D1 pin se connect karna
bool buttonState = false;

void setup() {
  Serial.begin(115200);     // Serial monitor ko initialize karo
  pinMode(buttonPin, INPUT); // Joystick button ko input mode mein set karo

  WiFi.begin(ssid, password); // WiFi connect karo

  // Wi-Fi connection hone tak wait karo
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("WiFi connected!");
  
  // WiFi.localIP() ko print karo jab WiFi successfully connect ho jaye
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());  // Print the ESP8266's IP address

  server.begin(); // Server start karo
}

void loop() {
  WiFiClient client = server.available(); // Client ko accept karo

  if (client) {
    String request = client.readStringUntil('\r'); // Request read karo
    Serial.println(request);

    // Joystick button ka state check karo
    buttonState = digitalRead(buttonPin);
    
    // Agar button press ho to signal send karo
    if (buttonState == HIGH) {
      client.println("Button Pressed!"); // Raspberry Pi ko signal bhejo
      Serial.println("Button Pressed");
    } else {
      client.println("Button Not Pressed");
    }
    
    client.stop(); // Client ko stop karo
  }
}

Raspberry-Pi
import socket

host = '192.168.1.100'  # Replace with Raspberry Pi's actual local IP
port = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print("Server listening on %s:%d" % (host, port))

while True:
    client_socket, client_address = server_socket.accept()
    print("Connection from %s" % (client_address))

    message = client_socket.recv(1024).decode()
    print("Message received: %s" % (message))

    if "Button Pressed!" in message:
        print("Joystick Button Pressed! Perform action here.")
    else:
        print("Joystick Button Not Pressed.")

    client_socket.close()  # Close the connection
