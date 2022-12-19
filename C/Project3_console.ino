String topic = "Project3/Console";
String deviceNumber = "1";

int numbOfHours = 5;
//int numbOfHoursConv = Hours * 3600;
int conversionHours = 1000000;

#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "group4_IoT";
const char* password = "group4four";
const char* mqtt_server = "10.120.0.57";

const char* mqtt_user = "group4";
const char* mqtt_passwd = "group4four";

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (50)
char msg[MSG_BUFFER_SIZE];

#define bufferSize (50)
char topicArray[bufferSize];
char macArray[bufferSize];

#define button1 12
#define button2 13
#define button3 14
#define button4 15
#define led1 32
#define led2 33

#define sizeDisc (1000)
String disconnectArray[sizeDisc];
int arrayIndex = 0;
int index2 = 0;

void setup() {
  pinMode(button1, INPUT_PULLUP);
  pinMode(button2, INPUT_PULLUP);
  pinMode(button3, INPUT_PULLUP);
  pinMode(button4, INPUT_PULLUP);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);

  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
}

void loop() {
  digitalWrite(led1,HIGH);

  if (!client.connected()) {
     if (digitalRead(button1)==LOW){
      digitalWrite(led1,LOW);
      digitalWrite(led2,HIGH);
      String status1 = "3&";
      status1 += (String) WiFi.macAddress();
      status1 = status1 + "&" + deviceNumber;
      disconnectArray[arrayIndex] = status1;
      arrayIndex++;
      index2 = 1;
      delay(2200);
      reconnect();                        //tweaked this
      digitalWrite(led2,LOW);
      digitalWrite(led1,HIGH);
      
  }else if (digitalRead(button2)==LOW){
      digitalWrite(led1,LOW);
      digitalWrite(led2,HIGH);
      String status2 = "2&";
      status2 += (String) WiFi.macAddress();
      status2 = status2 + "&" + deviceNumber;
      disconnectArray[arrayIndex] = status2;
      arrayIndex++;
      delay(2200);
      reconnect();
      index2 = 1;
      digitalWrite(led2,LOW);
      digitalWrite(led1,HIGH);
      
  }else if  (digitalRead(button3)==LOW){
      digitalWrite(led1,LOW);
      digitalWrite(led2,HIGH);

      String status3 = "1&";
      status3 += (String) WiFi.macAddress();
      status3 = status3 + "&" + deviceNumber;
      disconnectArray[arrayIndex] = status3;
      arrayIndex++;
      delay(2200); 
      reconnect();
      index2 = 1;
      digitalWrite(led2,LOW);
      digitalWrite(led1,HIGH);
      
  } else if (digitalRead(button4)==LOW){
      Serial.println("sleep");
      esp_sleep_enable_timer_wakeup(numbOfHours * conversionHours);
      esp_deep_sleep_start();
  }
  
  }else {
    for(int i = 0; i < index2; i++){
      Offline_Handler();
    }
    if (digitalRead(button1)==LOW){
      digitalWrite(led1,LOW);
      digitalWrite(led2,HIGH);

      String status1 = "3&";
      status1 += (String) WiFi.macAddress();
      status1 = status1 + "&" + deviceNumber;
      status1.toCharArray(msg, MSG_BUFFER_SIZE);
      Serial.println(status1);
      topic.toCharArray(topicArray, bufferSize);
      client.publish(topicArray, msg);
      delay(3200);                         //tweaked this
      digitalWrite(led2,LOW);
      digitalWrite(led1,HIGH);
  
  } else if (digitalRead(button2)==LOW){
      digitalWrite(led1,LOW);
      digitalWrite(led2,HIGH);

      String status2 = "2&";
      status2 += (String) WiFi.macAddress();
      status2 = status2 + "&" + deviceNumber;
      status2.toCharArray(msg, MSG_BUFFER_SIZE);
      Serial.println(status2);
      topic.toCharArray(topicArray, bufferSize);
      client.publish(topicArray, msg);
      delay(3200); 
      digitalWrite(led2,LOW);
      digitalWrite(led1,HIGH);
  
  } else if  (digitalRead(button3)==LOW){
      digitalWrite(led1,LOW);
      digitalWrite(led2,HIGH);

      String status3 = "1&";
      status3 += (String) WiFi.macAddress();
      status3 = status3 + "&" + deviceNumber;
      status3.toCharArray(msg, MSG_BUFFER_SIZE);
      Serial.println(status3);
      topic.toCharArray(topicArray, bufferSize);
      client.publish(topicArray, msg);
      delay(3200);
      digitalWrite(led2,LOW);
      digitalWrite(led1,HIGH);
  }else if (digitalRead(button4)==LOW){
      Serial.println("sleep");
      esp_sleep_enable_timer_wakeup(numbOfHours * conversionHours);
      esp_deep_sleep_start();
  }
  }
  client.loop();

}

void Offline_Handler(){
  for(int i = 0; i <= arrayIndex; i++){
      String message = disconnectArray[i];
      Serial.println(message);
      message.toCharArray(msg, MSG_BUFFER_SIZE);
      topic.toCharArray(topicArray, bufferSize);
      client.publish(topicArray, msg);
    }
    memset(disconnectArray, 0, sizeDisc);
    arrayIndex = 0;
    index2 = 0;
}

void DeepSleepHandler(){
  Serial.println("sleep");
  esp_sleep_enable_timer_wakeup(3000);
  esp_deep_sleep_start();
}

void setup_wifi() {

  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");

  for (int i = 0; i < length; i++) {
    if((char)payload[i] == 's'){
      Serial.println("Data received");
      DeepSleepHandler();
    }
  }
  Serial.println();

}

void reconnect() {
  // Loop until we're reconnected
  //for (int i = 0; i < 1; i++) {
    Serial.println("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str(),mqtt_user,mqtt_passwd)) {  //the real magic
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("Project3/Setup", "console connected");
      // ... and resubscribe
      client.subscribe("Project3/Power");
      Serial.println("subscribed");
      //i = 1;
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      Serial.println("Storing data offline");
      // Wait 5 seconds before retrying
    }
}

