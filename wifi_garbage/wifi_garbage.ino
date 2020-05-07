#include <NewPing.h>
#include "MedianFilter/MedianFilter.h"
#include "MedianFilter/MedianFilter.cpp"

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#include <EEPROM.h>

#define SERVER_IP "trash-system.herokuapp.com"

#ifndef STASSID
#define STASSID "MR150MacroSolutions_plus"
#define STAPSK  "Dachasamoizolation"
#endif


#define PIN_TRIG D0
#define PIN_ECHO D1
#define MAX_DISTANCE 200 // Константа для определения максимального расстояния, которое мы будем считать корректным.
// Создаем объект, методами которого будем затем пользоваться для получения расстояния.
// В качестве параметров передаем номера пинов, к которым подключены выходы ECHO и TRIG датчика
#define MAX_GARBAGE_IN_CM 59

NewPing sonar(PIN_TRIG, PIN_ECHO, MAX_DISTANCE);
MedianFilter filter(10, 1); 

int getIdFromMemory()
{
  EEPROM.begin(16);
  byte tmp;
  EEPROM.get(0, tmp);
  return static_cast<int>(tmp);
}

void setId2Memory(int id)
{
  EEPROM.begin(16);
  EEPROM.put(0, static_cast<byte>(id));
  EEPROM.commit();
}

float getLatitudeFromMemory()
{
  EEPROM.begin(16);
  float tmp;
  EEPROM.get(1, tmp);
  return tmp;
}

float getLongitudeFromMemory()
{
  EEPROM.begin(16);
  float tmp;
  EEPROM.get(5, tmp);
  return tmp;
}

int getSonar(NewPing &sonar)
{
  // Стартовая задержка, необходимая для корректной работы.
  delay(50);
  // Получаем значение от датчика расстояния и сохраняем его в переменную
  unsigned int distance = sonar.ping_cm();
  // Печатаем расстояние в мониторе порта
  Serial.print(distance);
  Serial.println("см");
  return distance;
}

void updateFullness(const int my_id, int value)
{
  if ((WiFi.status() == WL_CONNECTED))
  {
    WiFiClient client;
    HTTPClient http;

    Serial.print("[HTTP] begin...\n");
    http.begin(client, "http://" SERVER_IP "/update"); //HTTP
    http.addHeader("Content-Type", "application/json");

    Serial.print("[HTTP] POST...\n");

    int httpCode = http.POST("{\"id\": " + String(my_id) + ", \"fullness\": " + String(value) + "}");

    if (httpCode > 0)
    {
      Serial.printf("[HTTP] POST... code: %d\n", httpCode);

      if (httpCode == 202)
      {
        const String& answer = http.getString();
        Serial.println("received answer:\n<<");
        Serial.println(answer);
        Serial.println(">>");
      }
      else
      {
        Serial.println("CODE NO OK!!!!");
      }
    }
    else
    {
      Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
  }
}

int insertNewSensor(float lat, float longit)
{
  if ((WiFi.status() == WL_CONNECTED))
  {
    WiFiClient client;
    HTTPClient http;

    Serial.print("[HTTP] begin...\n");
    http.begin(client, "http://" SERVER_IP "/add"); //HTTP
    http.addHeader("Content-Type", "application/json");

    Serial.print("[HTTP] POST...\n");
    // start connection and send HTTP header and body
    int httpCode = http.POST("{\"latitude\": " + String(lat, 6) + ", \"longitude\": " + String(longit, 6) + "}");

    if (httpCode > 0)
    {
      Serial.printf("[HTTP] POST... code: %d\n", httpCode);

      if (httpCode == 201)
      {
        const String& id = http.getString();
        Serial.println("received answer:\n<<");
        Serial.println(id);
        Serial.println(">>");
        return id.toInt();
      }
      else
      {
        Serial.println("CODE NO OK!!!!");
      }
    }
    else
    {
      Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
    return 0;

  }
}


void setup()
{
  // Инициализируем взаимодействие по последовательному порту на скорости 9600
  Serial.begin(9600);
  
  WiFi.begin(STASSID, STAPSK);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());

  if (getIdFromMemory() == 0)
  {
    int my_id = insertNewSensor(getLatitudeFromMemory(), getLongitudeFromMemory());
    Serial.println("Returned ID:");
    Serial.println(my_id);
    setId2Memory(my_id);
  }
  Serial.println(getIdFromMemory());

}

int fullness = 0;
const int id = getIdFromMemory();

void loop()
{  
  for (int i = 0; i < 10; ++i)
  {
    filter.in(getSonar(sonar));
  }

  Serial.println(filter.out());
  
  fullness = 100 - int(float(filter.out()) / float(MAX_GARBAGE_IN_CM) * 100);
  Serial.println(fullness);
  updateFullness(id, fullness);

  delay(5000);

}
